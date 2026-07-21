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
Pin override: TAPPAAS_SOURCE_REF env var. Default: main — since the ADR007→main
promotion, main is the 2.0 manager/controller line; flip to `stable` when the
tested 2.0 is promoted to stable (migration Phase 6).
"""

import fnmatch
import io
import os
import posixpath
import re
import sys
import tarfile
import urllib.parse
import urllib.request

FORGE = "https://codeberg.org"
REPO = "TAPPaaS/TAPPaaS"
REF = os.environ.get("TAPPAAS_SOURCE_REF", "main")

# Exact files: (path in source repo, output under docs/, page title).
# Paths follow the pinned ref (ADR007); the build fails if one goes missing.
ALLOW_LIST = [
    # Install
    ("INSTALL.md", "generated/install-overview.md", "Install Overview"),
    ("hardware-selection.md", "generated/hardware-selection.md", "Hardware Selection"),
    ("preparation.md", "generated/preparation.md", "Preparation"),
    ("src/foundation/INSTALL.md", "generated/install.md", "Install Foundation"),
    ("INSTALL-ENVIRONMENT.md", "generated/install-environment.md", "Add an Environment"),
    ("src/foundation/satellite/INSTALL.md", "generated/satellite-install.md", "Satellite Install"),
    # What → Foundation: the computed module dependency graph
    # (regenerated upstream by src/generate-module-dependencies.sh)
    ("src/module-dependencies.md", "generated/module-dependencies.md", "Module Dependencies"),
    # Stack module installs (Add Stacks — each stack item is the module's INSTALL.md)
    ("src/apps/openwebui/INSTALL.md", "generated/apps/openwebui.md", "OpenWebUI"),
    ("src/apps/litellm/INSTALL.md", "generated/apps/litellm.md", "LiteLLM"),
    ("src/apps/vllm-amd/INSTALL.md", "generated/apps/vllm-amd.md", "vLLM (AMD)"),
    ("src/apps/nextcloud/INSTALL.md", "generated/apps/nextcloud.md", "Nextcloud"),
    ("src/apps/n8n/INSTALL.md", "generated/apps/n8n.md", "n8n"),
    ("src/apps/hass/INSTALL.md", "generated/apps/hass.md", "Home Assistant"),
    ("src/apps/deconz/INSTALL.md", "generated/apps/deconz.md", "deCONZ"),
    # Operate references
    ("src/foundation/tappaas-cicd/manager/network-manager/ZONES.md", "generated/zones.md", "Network Zones"),
    # What / Develop references. (src/README.md and src/foundation/README.md were
    # evaluated and skipped — they are 2-line stubs pointing back at tappaas.org.)
    ("GLOSSARY.md", "generated/ontology.md", "Glossary"),
    ("docs/ADR/README.md", "generated/adrs.md", "Architecture Decision Records"),
    ("src/foundation/schemas/README.md", "generated/schemas.md", "Module Schemas"),
    ("src/apps/00-Template/README.md", "generated/module-template.md", "Module Template"),
    # What → Design: module design notes surfaced under the "Design" submenu
    ("src/foundation/cluster/DESIGN.md", "generated/design/cluster.md", "Cluster Design"),
    ("src/foundation/network/DESIGN.md", "generated/design/network.md", "Network Design"),
    ("src/foundation/backup/DESIGN.md", "generated/design/backup.md", "Backup Design"),
    ("src/foundation/tappaas-cicd/DESIGN.md", "generated/design/cicd-mothership.md", "CICD Mothership"),
    ("src/foundation/tappaas-cicd/DESIGN-GIT.md", "generated/design/cicd-git.md", "Git & Repository Topology"),
    ("src/foundation/DEPENDENCIES.md", "generated/design/foundation-dependencies.md", "Foundation Dependencies"),
]

# Glob rules: (pattern, output dir under docs/, excluded component dirs).
# Every match becomes generated/<outdir>/<name>.md, and each output dir gets
# a SUMMARY.md for mkdocs-literate-nav.
GLOB_RULES = [
    ("src/foundation/tappaas-cicd/manager/*/README.md", "generated/managers", set()),
    ("src/foundation/tappaas-cicd/controller/*/README.md", "generated/controllers", set()),
    # Module catalog entries (the Stacks section points at these).
    # schemas has its own synced page; Deprecated must never publish;
    # 00-Template is synced separately as the Module Template.
    ("src/foundation/*/README.md", "generated/foundation", {"schemas", "Deprecated"}),
    ("src/apps/*/README.md", "generated/modules", {"00-Template"}),
]

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


def main():
    # Forgejo archive endpoint (top-level dir name in the tarball is stripped
    # generically below, so its exact shape does not matter).
    url = "{}/{}/archive/{}.tar.gz".format(FORGE, REPO, urllib.parse.quote(REF))
    print("WS0 sync: fetching {}@{} ...".format(REPO, REF))
    with urllib.request.urlopen(url, timeout=60) as resp:
        blob = resp.read()

    wanted = {src: (out, title) for src, out, title in ALLOW_LIST}
    found = {}
    globbed = {outdir: {} for _, outdir, _ in GLOB_RULES}

    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tar:
        for member in tar:
            if not member.isfile():
                continue
            rel = member.name.split("/", 1)[1] if "/" in member.name else ""
            if rel in wanted:
                found[rel] = tar.extractfile(member).read().decode("utf-8")
                continue
            for pattern, outdir, excluded in GLOB_RULES:
                # fnmatch's * spans '/', so also require equal path depth —
                # keeps nested files (e.g. opnsense-controller/patches/README.md) out.
                if fnmatch.fnmatch(rel, pattern) and rel.count("/") == pattern.count("/"):
                    component = rel.split("/")[-2]  # the dir holding README.md
                    if component in excluded:
                        continue
                    globbed[outdir][component] = (rel, tar.extractfile(member).read().decode("utf-8"))

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
    syncmap = {src: out for src, out, title in ALLOW_LIST}
    for _, outdir, _ in GLOB_RULES:
        for component, (rel, _content) in globbed[outdir].items():
            syncmap[rel] = "{}/{}.md".format(outdir, component)

    for src, (out, title) in wanted.items():
        write_page(src, out, title, found[src], syncmap)

    for pattern, outdir, _ in GLOB_RULES:
        components = globbed[outdir]
        if not components:
            sys.exit("WS0 sync FAILED: glob '{}' matched nothing in {}@{}".format(pattern, REPO, REF))
        summary_lines = []
        for component in sorted(components):
            src, content = components[component]
            title = pretty_name(component)
            write_page(src, "{}/{}.md".format(outdir, component), title, content, syncmap)
            summary_lines.append("* [{}]({}.md)".format(pretty_name(component), component))
        # Nav for this directory (consumed by mkdocs-literate-nav).
        summary_path = os.path.join(DOCS_DIR, outdir, "SUMMARY.md")
        with open(summary_path, "w") as fh:
            fh.write("\n".join(summary_lines) + "\n")
        print("WS0 sync: {} pages + SUMMARY.md -> docs/{}/".format(len(components), outdir))

    print("WS0 sync: OK ({}@{})".format(REPO, REF))


if __name__ == "__main__":
    main()
