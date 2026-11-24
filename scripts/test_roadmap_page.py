#!/usr/bin/env python3
"""test_roadmap_page.py — the Roadmap page's parser and links (scripts/roadmap_page.py).

    python3 scripts/test_roadmap_page.py [--file <ROADMAP.md or ROADMAP.public.md>]

On a small roadmap in the published layout: `Roadmap#N` rows link to the public list, `#N` and
`<Repo>#N` rows (and references in prose) to Codeberg, both base URLs follow their environment
variables, a published copy gets the published wording; with --file, that file builds too.
Stdlib only, no network. Exit 0 when all pass.
"""

import argparse
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

SAMPLE = """# TAPPaaS Roadmap

## Wave 7 — enhance the stacks

New modules.

### G7.1 DevOps stack — Ease H · Risk M · released: 1 · open: 2

The devops stack, see Roadmap#3 and #415.

| # | Issue | Ease | Risk | Note |
|---|-------|:-:|:-:|------|
| Roadmap#3 | Backlog board | M | L | in test |
| ✅ #415 | Image builds off GitHub | M | L | done |
| Community#36 | unifi-os auto-upgrade | L | L | open |

## Next release

<!-- next-release summary -->
<!-- /next-release summary -->

## Release 2.5 — staging 2026-11-24 · production at the next boundary

Tag `v2.5`. What it delivered: things.

The rows below are what it carried, by the wave and group they came from.

### Wave 7 — enhance the stacks

#### G7.1 DevOps stack — Ease H · Risk M

| # | Issue | Ease | Risk | Note |
|---|-------|:-:|:-:|------|
| ✅ #900 | Vikunja | M | L | released |
"""

fails = []


def check(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + ("" if cond or not detail else "\n     " + str(detail)[:400]))
    if not cond:
        fails.append(name)


def load(**env):
    for k in ("TAPPAAS_ROADMAP_PUBLIC_REPO", "TAPPAAS_ROADMAP_ARCHIVE_ORG"):
        os.environ.pop(k, None)
    os.environ.update(env)
    import roadmap_page
    return importlib.reload(roadmap_page)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file")
    a = ap.parse_args()

    rp = load()
    page = rp.build(SAMPLE, published=True)
    check("Roadmap#N links to the public list on forgejo.tappaas.org",
          '<a href="https://forgejo.tappaas.org/TAPPaaS/Roadmap/issues/3">Roadmap#3</a>' in page, page)
    check("#N links to Codeberg's TAPPaaS/TAPPaaS",
          '<a href="https://codeberg.org/TAPPaaS/TAPPaaS/issues/415">#415</a>' in page
          and '<a href="https://codeberg.org/TAPPaaS/TAPPaaS/issues/900">#900</a>' in page)
    check("<Repo>#N links to Codeberg's TAPPaaS/<Repo>",
          '<a href="https://codeberg.org/TAPPaaS/Community/issues/36">Community#36</a>' in page)
    check("references in prose are linked the same way",
          page.count("https://forgejo.tappaas.org/TAPPaaS/Roadmap/issues/3") >= 2)
    check("the published copy says so", "roadmap/ROADMAP.public.md in this repository" in page
          and "public roadmap list" in page and "ROADMAP.md in TAPPaaS/TAPPaaS" not in page)
    waves, releases = rp.parse(SAMPLE)
    check("every row is read, whatever it cites", len(waves[0]["groups"][0]["issues"]) == 3
          and releases[0]["groups"][0]["issues"][0]["num"] == "900")

    rp = load(TAPPAAS_ROADMAP_PUBLIC_REPO="https://forge.example/TAPPaaS/Roadmap/",
              TAPPAAS_ROADMAP_ARCHIVE_ORG="https://archive.example/TAPPaaS")
    page = rp.build(SAMPLE)
    check("the base URLs follow their environment variables",
          "https://forge.example/TAPPaaS/Roadmap/issues/3" in page
          and "https://archive.example/TAPPaaS/TAPPaaS/issues/415" in page)
    check("ROADMAP.md keeps today's wording", "ROADMAP.md in TAPPaaS/TAPPaaS" in page
          and "The details live on Codeberg" in page)

    if a.file:
        rp = load()
        text = open(a.file, encoding="utf-8").read()
        try:
            page = rp.build(text, published=a.file.endswith(".public.md"))
            check("{} builds".format(os.path.basename(a.file)), "tap-rm" in page)
        except ValueError as e:
            check("{} builds".format(os.path.basename(a.file)), False, e)

    print("FAILED: {}".format(fails) if fails else "ALL PASSED")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
