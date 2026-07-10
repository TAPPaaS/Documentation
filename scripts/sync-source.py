#!/usr/bin/env python3
"""WS0 source-sync runner (ADR-001 §12).

Fetches an allow-listed set of files from the TAPPaaS source repo (GitHub,
cross-forge — see ADR-001 open decision #7) at a pinned ref and transforms
them into site pages under docs/generated/:

  - prepends a "generated from source — edit upstream" banner,
  - injects front matter (title),
  - rewrites relative links/images to absolute GitHub URLs at the pinned ref,
  - expands GLOB rules (e.g. every manager/controller README) and emits a
    SUMMARY.md per output directory for mkdocs-literate-nav, so new upstream
    managers/controllers appear in the nav with zero docs-repo changes,
  - FAILS the build if an expected exact file is missing (drift guard).

Run before `mkdocs build` (CI does; locally: python3 scripts/sync-source.py).
Pin override: TAPPAAS_SOURCE_REF env var. Default: ADR007 — the docs describe
the 2.0 manager/controller paradigm (ADR-001 §8/§12.1); flip to `stable` when
ADR007 is promoted.
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

REPO = "TAPPaaS/TAPPaaS"
REF = os.environ.get("TAPPAAS_SOURCE_REF", "ADR007")

# Exact files: (path in source repo, output under docs/, page title).
# Paths follow the pinned ref (ADR007); the build fails if one goes missing.
ALLOW_LIST = [
    # Install (WS3)
    ("INSTALL.md", "generated/install.md", "INSTALL.md (source)"),
    ("INSTALL-ENVIRONMENT.md", "generated/install-environment.md", "INSTALL-ENVIRONMENT.md (source)"),
    ("src/foundation/satellite/README.md", "generated/satellite.md", "Satellite (source)"),
    ("src/foundation/satellite/INSTALL.md", "generated/satellite-install.md", "Satellite INSTALL (source)"),
    # Operate references (WS4)
    ("src/foundation/tappaas-cicd/manager/network-manager/ZONES.md", "generated/zones.md", "Network zones (source)"),
    # Develop references (WS4)
    ("docs/ADR/ADR-007 - TAPPaaS Taxonomy.md", "generated/adr-007-taxonomy.md", "ADR-007 — TAPPaaS Taxonomy (source)"),
    ("src/foundation/schemas/README.md", "generated/schemas.md", "Schemas — the module contract (source)"),
    ("src/apps/00-Template/README.md", "generated/module-template.md", "Module template — 00-Template (source)"),
]

# Glob rules: (pattern, output dir under docs/, name = capture between prefix
# and suffix). Every match becomes generated/<outdir>/<name>.md, and each
# output dir gets a SUMMARY.md for mkdocs-literate-nav.
GLOB_RULES = [
    ("src/foundation/tappaas-cicd/manager/*/README.md", "generated/managers"),
    ("src/foundation/tappaas-cicd/controller/*/README.md", "generated/controllers"),
]

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

BANNER = """---
title: "{title}"
---

!!! info "Generated from source — do not edit here"
    This page is synced at build time from
    [`{src}`](https://github.com/{repo}/blob/{ref}/{src_quoted}) in **`{repo}@{ref}`**.
    Changes belong upstream; edits to this page will be overwritten.

"""

# Matches [text](target), ![alt](target), and the angle-bracket form
# [text](<target with spaces>) used by some upstream ADRs.
LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(\s*(?:<([^>]+)>|([^)\s]+))((?:\s+\"[^\"]*\")?)\s*\)")


def rewrite_links(markdown, src_path):
    """Point relative links/images at GitHub (blob/raw) at the pinned ref."""
    src_dir = posixpath.dirname(src_path)

    def repl(m):
        bang, text, target_angled, target_plain, title = m.groups()
        target = target_angled or target_plain
        if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith(("#", "/")):
            return m.group(0)  # absolute URL, anchor or site-absolute — leave alone
        path, _, frag = target.partition("#")
        resolved = posixpath.normpath(posixpath.join(src_dir, path)) if path else src_path
        quoted = urllib.parse.quote(resolved, safe="/")
        base = (
            "https://raw.githubusercontent.com/{}/{}/{}".format(REPO, REF, quoted)
            if bang
            else "https://github.com/{}/blob/{}/{}".format(REPO, REF, quoted)
        )
        if frag:
            base += "#" + frag
        return "{}[{}]({}{})".format(bang, text, base, title)

    return LINK_RE.sub(repl, markdown)


def pretty_name(component):
    """'backup-manager' -> 'Backup Manager'."""
    return " ".join(w.capitalize() for w in component.split("-"))


def write_page(src, out, title, content):
    banner = BANNER.format(
        title=title, src=src, repo=REPO, ref=REF,
        src_quoted=urllib.parse.quote(src, safe="/"),
    )
    out_path = os.path.join(DOCS_DIR, out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as fh:
        fh.write(banner + rewrite_links(content, src))
    print("WS0 sync: {} -> docs/{}".format(src, out))


def main():
    url = "https://codeload.github.com/{}/tar.gz/refs/heads/{}".format(REPO, urllib.parse.quote(REF))
    print("WS0 sync: fetching {}@{} ...".format(REPO, REF))
    with urllib.request.urlopen(url, timeout=60) as resp:
        blob = resp.read()

    wanted = {src: (out, title) for src, out, title in ALLOW_LIST}
    found = {}
    globbed = {outdir: {} for _, outdir in GLOB_RULES}

    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tar:
        for member in tar:
            if not member.isfile():
                continue
            rel = member.name.split("/", 1)[1] if "/" in member.name else ""
            if rel in wanted:
                found[rel] = tar.extractfile(member).read().decode("utf-8")
                continue
            for pattern, outdir in GLOB_RULES:
                # fnmatch's * spans '/', so also require equal path depth —
                # keeps nested files (e.g. opnsense-controller/patches/README.md) out.
                if fnmatch.fnmatch(rel, pattern) and rel.count("/") == pattern.count("/"):
                    component = rel.split("/")[-2]  # the dir holding README.md
                    globbed[outdir][component] = (rel, tar.extractfile(member).read().decode("utf-8"))

    missing = sorted(set(wanted) - set(found))
    if missing:
        sys.exit(
            "WS0 sync FAILED: expected file(s) missing in {}@{}: {} "
            "(source moved? update the allow-list in scripts/sync-source.py)".format(
                REPO, REF, ", ".join(missing)
            )
        )

    for src, (out, title) in wanted.items():
        write_page(src, out, title, found[src])

    for pattern, outdir in GLOB_RULES:
        components = globbed[outdir]
        if not components:
            sys.exit("WS0 sync FAILED: glob '{}' matched nothing in {}@{}".format(pattern, REPO, REF))
        summary_lines = []
        for component in sorted(components):
            src, content = components[component]
            title = "{} (source)".format(pretty_name(component))
            write_page(src, "{}/{}.md".format(outdir, component), title, content)
            summary_lines.append("* [{}]({}.md)".format(pretty_name(component), component))
        # Nav for this directory (consumed by mkdocs-literate-nav).
        summary_path = os.path.join(DOCS_DIR, outdir, "SUMMARY.md")
        with open(summary_path, "w") as fh:
            fh.write("\n".join(summary_lines) + "\n")
        print("WS0 sync: {} pages + SUMMARY.md -> docs/{}/".format(len(components), outdir))

    print("WS0 sync: OK ({}@{})".format(REPO, REF))


if __name__ == "__main__":
    main()
