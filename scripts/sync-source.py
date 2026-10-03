#!/usr/bin/env python3
"""WS0 source-sync runner (ADR-001 §12).

Fetches an allow-listed set of files from the TAPPaaS source repo (Codeberg —
the dev home since the Codeberg migration; see the code repo's
docs/codeberg-migration.md) at a pinned ref and transforms them into site
pages under docs/generated/:

  - prepends a "generated from source — edit upstream" banner,
  - injects front matter (title),
  - rewrites relative links/images to absolute Codeberg URLs at the pinned ref,
  - expands GLOB rules (e.g. every manager/controller README) and emits a
    SUMMARY.md per output directory for mkdocs-literate-nav, so new upstream
    managers/controllers appear in the nav with zero docs-repo changes,
  - FAILS the build if an expected exact file is missing (drift guard).

Run before `mkdocs build` (CI does; locally: python3 scripts/sync-source.py).
Local checkout instead of a clone: TAPPAAS_SOURCE_DIR=<path> (for trying a source
branch before it is pushed; the banner still names REPO@REF).
Pin override: TAPPAAS_SOURCE_REF env var. Default: main — since the ADR007→main
promotion, main is the 2.0 manager/controller line; flip to `stable` when the
tested 2.0 is promoted to stable (migration Phase 6).
"""

import fnmatch
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse

FORGE = "https://codeberg.org"
REPO = "TAPPaaS/TAPPaaS"
REF = os.environ.get("TAPPAAS_SOURCE_REF", "main")

# Exact files: (path in source repo, output under docs/, page title).
# Paths follow the pinned ref (ADR007); the build fails if one goes missing.
#
# "@<module>/<file>" names a file in a module's own directory wherever it sits:
# src/<dir>/<module>/<file> outside src/foundation, exactly one match. Modules
# are grouped by stack (TAPPaaS #421: src/apps/hass -> src/home/hass), so a
# module page must not depend on which directory its stack is.
ALLOW_LIST = [
    # Install
    ("INSTALL.md", "install/index.md", "Install Overview"),
    ("hardware-selection.md", "generated/hardware-selection.md", "Hardware Selection"),
    ("preparation.md", "generated/preparation.md", "Preparation"),
    ("src/foundation/INSTALL.md", "generated/install.md", "Install Foundation"),
    ("INSTALL-ENVIRONMENT.md", "generated/install-environment.md", "Install Environments"),
    ("src/foundation/satellite/INSTALL.md", "generated/satellite-install.md", "Satellite Install"),
    # What → Foundation: the computed module dependency graph
    # (regenerated upstream by src/generate-module-dependencies.sh)
    ("src/module-dependencies.md", "generated/module-dependencies.md", "Module Dependencies"),
    # Install → Add Stacks is not listed here: it is built from src/<stack>/ by
    # sync_stacks() below.
    # Operate references
    ("src/foundation/tappaas-cicd/manager/network-manager/ZONES.md", "generated/zones.md", "Network Zones"),
    ("src/foundation/tappaas-cicd/manager/network-manager/ADMIN-VPN.md", "generated/admin-vpn.md", "Admin VPN (WireGuard)"),
    ("src/foundation/backup/RESTORE.md", "generated/disaster-recovery.md", "Disaster Recovery"),
    ("src/foundation/tappaas-cicd/RELEASE-TRAIN.md", "generated/release-train.md", "Release Train"),
    # What / Develop references. (src/README.md and src/foundation/README.md were
    # evaluated and skipped — they are 2-line stubs pointing back at tappaas.org.)
    ("GLOSSARY.md", "generated/ontology.md", "Glossary"),
    ("docs/ADR/README.md", "generated/adrs.md", "Architecture Decision Records"),
    ("src/foundation/schemas/README.md", "generated/schemas.md", "Module Schemas"),
    ("@00-Template/DEVELOP.md", "generated/develop-a-module.md", "Develop a Module"),
    ("@00-Template/README.md", "generated/module-template.md", "Module Details"),
    ("src/foundation/tappaas-cicd/migrations/README.md", "generated/config-migrations.md", "Config Migrations"),
    ("BUILD.md", "generated/build.md", "TAPPaaS Build Process"),
    # What → Design: module design notes surfaced under the "Design" submenu
    ("src/foundation/cluster/DESIGN.md", "generated/design/cluster.md", "Cluster Design"),
    ("src/foundation/network/DESIGN.md", "generated/design/network.md", "Network Design"),
    ("src/foundation/backup/DESIGN.md", "generated/design/backup.md", "Backup Design"),
    ("src/foundation/tappaas-cicd/DESIGN.md", "generated/design/cicd-mothership.md", "CICD Mothership"),
    ("src/foundation/tappaas-cicd/DESIGN-GIT.md", "generated/design/cicd-git.md", "Git & Repository Topology"),
    ("src/foundation/DEPENDENCIES.md", "generated/design/foundation-dependencies.md", "Foundation Dependencies"),
]

# Glob rules: (pattern, output dir under docs/, excluded component dirs, naming,
# excluded top-level dirs under src/ — "*" in the pattern's second part matches
# any of them otherwise).
# Every match becomes generated/<outdir>/<name>.md, and each output dir gets
# a SUMMARY.md for mkdocs-literate-nav. `naming` picks the page name/title:
#   "dir"            -> the README's own dir (e.g. network-manager); title = pretty_name.
#   "module-service" -> <module>-<service> (e.g. network-proxy), because service
#                       dir names collide across modules (cluster/backup both have
#                       a `vm`); title = the `module:service` coordinate.
GLOB_RULES = [
    ("src/foundation/tappaas-cicd/manager/*/README.md", "generated/managers", set(), "dir", set()),
    ("src/foundation/tappaas-cicd/controller/*/README.md", "generated/controllers", set(), "dir", set()),
    # Foundation service contracts — the provider:service pairs modules depend on.
    ("src/foundation/*/services/*/README.md", "generated/services", set(), "module-service", set()),
    # Module catalog entries (the Stacks section points at these).
    # schemas has its own synced page; Deprecated must never publish;
    # 00-Template is synced separately as the Module Template.
    ("src/foundation/*/README.md", "generated/foundation", {"schemas", "Deprecated"}, "dir", set()),
    # Every other module, in whichever stack directory it lives (src/apps/<m>
    # before TAPPaaS #421, src/<stack>/<m> after).
    ("src/*/*/README.md", "generated/modules", {"00-Template"}, "dir", {"foundation"}),
]


def glob_component(rel, naming):
    """Page name (without .md) for a globbed match under its output dir."""
    parts = rel.split("/")
    if naming == "module-service":
        return "{}-{}".format(parts[-4], parts[-2])  # <module>-<service>
    return parts[-2]  # the dir holding README.md


def glob_title(rel, naming):
    """Front-matter title / nav label for a globbed match."""
    parts = rel.split("/")
    if naming == "module-service":
        return "{}:{}".format(parts[-4], parts[-2])  # the module:service coordinate
    return pretty_name(parts[-2])

# Nicer titles for globbed component names.
TITLE_OVERRIDES = {
    "vllm-amd": "vLLM (AMD)",
    "nextcloud-hpb": "Nextcloud HPB",
    "hass": "Home Assistant",
    "deconz": "deCONZ",
    "euro-office": "EURO Office",
    "litellm": "LiteLLM",
    "openwebui": "OpenWebUI",
    "n8n": "n8n",
    "netbird-client": "NetBird Client",
    "tappaas-cicd": "TAPPaaS CICD",
    "opnsense-controller": "OPNsense Controller",
    "ap-controller": "AP Controller",
}

# Install → Add Stacks, one section per stack directory src/<stack>/ (TAPPaaS #421):
# the stack's README.md is the section overview, each src/<stack>/<module>/INSTALL.md
# a page under it, in the install order the README's generated table lists.
# A new stack or module appears in the nav with zero docs-repo changes.
STACKS_OUTDIR = "generated/install"
STACKS_EXCLUDED = {"foundation"}            # has its own Install Foundation pages
STACK_MODULES_EXCLUDED = {"00-Template"}    # copied, never installed
STACKS_LAST = ["misc"]                      # the leftovers go at the end of the nav

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

# The provenance note is an HTML comment — visible to editors viewing the
# source, invisible to readers of the page (per the 2026-07-11 review).
BANNER = """---
title: "{title}"
---

<!--
  GENERATED FROM SOURCE - do not edit here.
  Synced at build time from {src} in {repo}@{ref}
  (https://codeberg.org/{repo}/src/branch/{ref}/{src_quoted}).
  Changes belong upstream; edits to this page will be overwritten.
-->

"""

# Matches [text](target), ![alt](target), and the angle-bracket form
# [text](<target with spaces>) used by some upstream ADRs.
LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(\s*(?:<([^>]+)>|([^)\s]+))((?:\s+\"[^\"]*\")?)\s*\)")


def rewrite_links(markdown, src_path, out_path, syncmap):
    """Rewrite relative links. A link to another **synced** page is repointed at that
    page's on-site location (so the site cross-links internally); everything else points
    at Codeberg (src/raw) at the pinned ref."""
    src_dir = posixpath.dirname(src_path)
    out_dir = posixpath.dirname(out_path)

    def repl(m):
        bang, text, target_angled, target_plain, title = m.groups()
        target = target_angled or target_plain
        if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith(("#", "/")):
            return m.group(0)  # absolute URL, anchor or site-absolute — leave alone
        path, _, frag = target.partition("#")
        resolved = posixpath.normpath(posixpath.join(src_dir, path)) if path else src_path
        # Cross-link to another synced page → link within the site (relative to this page).
        if not bang and resolved in syncmap:
            target_out = posixpath.relpath(syncmap[resolved], out_dir) if out_dir else syncmap[resolved]
            return "{}[{}]({}{}{})".format(bang, text, target_out, ("#" + frag) if frag else "", title)
        quoted = urllib.parse.quote(resolved, safe="/")
        base = (
            "{}/{}/raw/branch/{}/{}".format(FORGE, REPO, REF, quoted)
            if bang
            else "{}/{}/src/branch/{}/{}".format(FORGE, REPO, REF, quoted)
        )
        if frag:
            base += "#" + frag
        return "{}[{}]({}{})".format(bang, text, base, title)

    return LINK_RE.sub(repl, markdown)


def pretty_name(component):
    """'backup-manager' -> 'Backup Manager' (with overrides for brand names)."""
    if component in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[component]
    return " ".join(w.capitalize() for w in component.split("-"))


def write_page(src, out, title, content, syncmap):
    banner = BANNER.format(
        title=title, src=src, repo=REPO, ref=REF,
        src_quoted=urllib.parse.quote(src, safe="/"),
    )
    out_path = os.path.join(DOCS_DIR, out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as fh:
        fh.write(banner + rewrite_links(content, src, out, syncmap))
    print("WS0 sync: {} -> docs/{}".format(src, out))


def clone_source(dest):
    """Shallow-clone the source repo at REF into dest.

    Replaces the previous on-demand tarball download (…/archive/REF.tar.gz):
    Codeberg regenerates that tarball per request and it repeatedly exceeded the
    socket timeout for this large repo, failing the whole build (pipelines
    #76/#77). A shallow clone transfers a git pack instead — seconds, not
    minutes — and is far more reliable.
    """
    url = "{}/{}.git".format(FORGE, REPO)
    print("WS0 sync: shallow-cloning {}@{} ...".format(REPO, REF))
    subprocess.run(
        ["git", "clone", "--depth", "1", "--branch", REF, url, dest],
        check=True,
    )


def resolve_module_paths(paths):
    """ALLOW_LIST with every "@<module>/<file>" replaced by the one path that holds
    it (src/<dir>/<module>/<file>, <dir> not foundation). Fails the build on none or
    several — the drift guard, applied to a module that moved."""
    out = []
    for src, page, title in ALLOW_LIST:
        if src.startswith("@"):
            module, _, name = src[1:].partition("/")
            hits = sorted(p for p in paths
                          if p.count("/") == 3 and p.startswith("src/") and not p.startswith("src/foundation/")
                          and p.split("/")[2] == module and p.split("/")[3] == name)
            if len(hits) != 1:
                sys.exit("WS0 sync FAILED: {} matched {} file(s) in {}@{}: {}".format(
                    src, len(hits), REPO, REF, ", ".join(hits) or "none"))
            src = hits[0]
        out.append((src, page, title))
    return out


def find_stacks(paths):
    """{stack: (readme, [(module, install), ...] in install order)} for every
    src/<stack>/ holding a README.md and at least one module INSTALL.md."""
    stacks = {}
    for p in paths:
        parts = p.split("/")
        if (len(parts) == 4 and parts[0] == "src" and parts[3] == "INSTALL.md"
                and parts[1] not in STACKS_EXCLUDED and parts[2] not in STACK_MODULES_EXCLUDED):
            stacks.setdefault(parts[1], []).append((parts[2], p))
    out = {}
    for stack, modules in stacks.items():
        readme = "src/{}/README.md".format(stack)
        if readme not in paths:
            sys.exit("WS0 sync FAILED: stack src/{}/ has modules but no README.md in {}@{}".format(
                stack, REPO, REF))
        out[stack] = (readme, modules)
    if not out:
        sys.exit("WS0 sync FAILED: no stack directories src/<stack>/<module>/INSTALL.md in {}@{}".format(
            REPO, REF))
    return out


def stack_title(readme_text, stack):
    """'# AI stack' -> 'AI Stack' (the site writes Stack with a capital)."""
    m = re.search(r"^#\s+(.+?)\s*$", readme_text, re.M)
    title = m.group(1) if m else pretty_name(stack)
    return re.sub(r"\bstack$", "Stack", title)


def install_order(readme_text, modules):
    """Modules in the order the stack README links them (its generated install-order
    table); any it does not mention follow alphabetically."""
    listed = re.findall(r"\]\(([^)/\s]+)/README\.md\)", readme_text)
    rank = {m: i for i, m in enumerate(dict.fromkeys(listed))}
    return sorted(modules, key=lambda mi: (rank.get(mi[0], len(rank)), mi[0]))


def stack_sort_key(stack):
    return (stack in STACKS_LAST, STACKS_LAST.index(stack) if stack in STACKS_LAST else 0, stack)


def main():
    found = {}
    globbed = {outdir: {} for _, outdir, _, _, _ in GLOB_RULES}

    local = os.environ.get("TAPPAAS_SOURCE_DIR")
    tmp = local or tempfile.mkdtemp(prefix="tappaas-src-")
    try:
        if not local:
            clone_source(tmp)
        paths = []
        for root, dirs, filenames in os.walk(tmp):
            if ".git" in dirs:
                dirs.remove(".git")
            paths += [os.path.relpath(os.path.join(root, fn), tmp) for fn in filenames]
        allow = resolve_module_paths(paths)
        stacks = find_stacks(set(paths))
        stack_pages = {}  # src -> (out, title, text); text filled below
        for stack, (readme, modules) in stacks.items():
            with open(os.path.join(tmp, readme), encoding="utf-8") as fh:
                readme_text = fh.read()
            stack_pages[readme] = ["{}/{}/index.md".format(STACKS_OUTDIR, stack),
                                   stack_title(readme_text, stack), readme_text]
            for module, install in modules:
                with open(os.path.join(tmp, install), encoding="utf-8") as fh:
                    stack_pages[install] = ["{}/{}/{}.md".format(STACKS_OUTDIR, stack, module),
                                            pretty_name(module), fh.read()]
        wanted = {src: (out, title) for src, out, title in allow}
        for root, dirs, filenames in os.walk(tmp):
            if ".git" in dirs:
                dirs.remove(".git")  # never descend into git metadata
            for fn in filenames:
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, tmp)  # repo-relative path (POSIX on Linux/macOS)
                if rel in wanted:
                    with open(full, encoding="utf-8") as fh:
                        found[rel] = fh.read()
                    continue
                for pattern, outdir, excluded, naming, tops in GLOB_RULES:
                    # fnmatch's * spans '/', so also require equal path depth —
                    # keeps nested files (e.g. opnsense-controller/patches/README.md) out.
                    if fnmatch.fnmatch(rel, pattern) and rel.count("/") == pattern.count("/"):
                        if rel.split("/")[-2] in excluded or rel.split("/")[1] in tops:
                            continue
                        component = glob_component(rel, naming)
                        with open(full, encoding="utf-8") as fh:
                            globbed[outdir][component] = (rel, fh.read())
    finally:
        if not local:
            shutil.rmtree(tmp, ignore_errors=True)

    missing = sorted(set(wanted) - set(found))
    if missing:
        sys.exit(
            "WS0 sync FAILED: expected file(s) missing in {}@{}: {} "
            "(source moved? update the allow-list in scripts/sync-source.py)".format(
                REPO, REF, ", ".join(missing)
            )
        )

    # Map every synced source path to its on-site output, so links between synced
    # pages resolve within the site instead of bouncing out to Codeberg.
    syncmap = {src: out for src, out, title in allow}
    syncmap.update({src: page[0] for src, page in stack_pages.items()})
    for _, outdir, _, _, _ in GLOB_RULES:
        for component, (rel, _content) in globbed[outdir].items():
            syncmap[rel] = "{}/{}.md".format(outdir, component)

    for src, (out, title) in wanted.items():
        write_page(src, out, title, found[src], syncmap)

    for pattern, outdir, _, naming, _ in GLOB_RULES:
        components = globbed[outdir]
        if not components:
            sys.exit("WS0 sync FAILED: glob '{}' matched nothing in {}@{}".format(pattern, REPO, REF))
        summary_lines = []
        for component in sorted(components):
            src, content = components[component]
            title = glob_title(src, naming)
            write_page(src, "{}/{}.md".format(outdir, component), title, content, syncmap)
            summary_lines.append("* [{}]({}.md)".format(title, component))
        # Nav for this directory (consumed by mkdocs-literate-nav).
        summary_path = os.path.join(DOCS_DIR, outdir, "SUMMARY.md")
        with open(summary_path, "w") as fh:
            fh.write("\n".join(summary_lines) + "\n")
        print("WS0 sync: {} pages + SUMMARY.md -> docs/{}/".format(len(components), outdir))

    summary_lines = []
    for stack in sorted(stacks, key=stack_sort_key):
        readme, modules = stacks[stack]
        out, title, text = stack_pages[readme]
        write_page(readme, out, title, text, syncmap)
        summary_lines += ["* {}".format(title), "    * [Overview]({}/index.md)".format(stack)]
        for module, install in install_order(text, modules):
            out, mtitle, mtext = stack_pages[install]
            write_page(install, out, mtitle, mtext, syncmap)
            summary_lines.append("    * [{}]({}/{}.md)".format(mtitle, stack, module))
    with open(os.path.join(DOCS_DIR, STACKS_OUTDIR, "SUMMARY.md"), "w") as fh:
        fh.write("\n".join(summary_lines) + "\n")
    print("WS0 sync: {} stacks, {} module installs + SUMMARY.md -> docs/{}/".format(
        len(stacks), sum(len(m) for _, m in stacks.values()), STACKS_OUTDIR))

    print("WS0 sync: OK ({}@{})".format(REPO, REF))


if __name__ == "__main__":
    main()
