#!/usr/bin/env python3
"""WS0 source-sync runner (ADR-001 §12).

Fetches an allow-listed set of files from the TAPPaaS source repo (GitHub,
cross-forge — see ADR-001 open decision #7) at a pinned ref and transforms
them into site pages under docs/generated/:

  - prepends a "generated from source — edit upstream" banner,
  - injects front matter (title),
  - rewrites relative links/images to absolute GitHub URLs at the pinned ref,
  - FAILS the build if an expected source file is missing (drift guard).

Run before `mkdocs build` (CI does; for local builds: python3 scripts/sync-source.py).
Pin override: TAPPAAS_SOURCE_REF env var (default: main — the staging surface
tracks upstream main; switch the production build to `stable` at the 2.0
cutover, once INSTALL.md exists on stable).
"""

import io
import os
import posixpath
import re
import sys
import tarfile
import urllib.request

REPO = "TAPPaaS/TAPPaaS"
REF = os.environ.get("TAPPAAS_SOURCE_REF", "main")

# (path in source repo, output under docs/, page title)
ALLOW_LIST = [
    ("INSTALL.md", "generated/install.md", "INSTALL.md (source)"),
    ("INSTALL-VARIANT.md", "generated/install-variant.md", "INSTALL-VARIANT.md (source)"),
]

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

BANNER = """---
title: "{title}"
---

!!! info "Generated from source — do not edit here"
    This page is synced at build time from
    [`{src}`](https://github.com/{repo}/blob/{ref}/{src}) in **`{repo}@{ref}`**.
    Changes belong upstream; edits to this page will be overwritten.

"""

LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)((?:\s+\"[^\"]*\")?)\)")


def rewrite_links(markdown, src_path):
    """Point relative links/images at GitHub (blob/raw) at the pinned ref."""
    src_dir = posixpath.dirname(src_path)

    def repl(m):
        bang, text, target, title = m.groups()
        if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith(("#", "/")):
            return m.group(0)  # absolute URL, anchor or site-absolute — leave alone
        path, _, frag = target.partition("#")
        resolved = posixpath.normpath(posixpath.join(src_dir, path)) if path else src_path
        kind = "raw" if bang else "blob"
        base = (
            "https://raw.githubusercontent.com/{}/{}/{}".format(REPO, REF, resolved)
            if bang
            else "https://github.com/{}/{}/{}/{}".format(REPO, kind, REF, resolved)
        )
        if frag:
            base += "#" + frag
        return "{}[{}]({}{})".format(bang, text, base, title)

    return LINK_RE.sub(repl, markdown)


def main():
    url = "https://codeload.github.com/{}/tar.gz/refs/heads/{}".format(REPO, REF)
    print("WS0 sync: fetching {}@{} ...".format(REPO, REF))
    with urllib.request.urlopen(url, timeout=60) as resp:
        blob = resp.read()

    wanted = {src: (out, title) for src, out, title in ALLOW_LIST}
    found = {}
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tar:
        for member in tar:
            # strip the tarball's top-level "<repo>-<ref>/" directory
            rel = member.name.split("/", 1)[1] if "/" in member.name else ""
            if rel in wanted and member.isfile():
                found[rel] = tar.extractfile(member).read().decode("utf-8")

    missing = sorted(set(wanted) - set(found))
    if missing:
        sys.exit(
            "WS0 sync FAILED: expected file(s) missing in {}@{}: {} "
            "(source moved? update the allow-list in scripts/sync-source.py)".format(
                REPO, REF, ", ".join(missing)
            )
        )

    for src, (out, title) in wanted.items():
        content = rewrite_links(found[src], src)
        banner = BANNER.format(title=title, src=src, repo=REPO, ref=REF)
        out_path = os.path.join(DOCS_DIR, out)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w") as fh:
            fh.write(banner + content)
        print("WS0 sync: {} -> docs/{} ({} chars)".format(src, out, len(content)))

    print("WS0 sync: OK ({} file(s) from {}@{})".format(len(wanted), REPO, REF))


if __name__ == "__main__":
    main()
