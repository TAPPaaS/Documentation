# The published roadmap

`ROADMAP.public.md` here is the TAPPaaS roadmap as it is published: generated from the project's
Vikunja by TAPPaaS's `release/roadmap-generate.py --public` (ADR-053 D11), with private rows left
out and open rows citing their item in the public list (`Roadmap#N`). It is not edited by hand:
change the roadmap in Vikunja (`release/roadmap-edit.py`), generate again and commit the file.

`scripts/sync-source.py` builds the Roadmap page from it when it is here, and from the source
repository's `ROADMAP.md` when it is not (before the self-hosting cut-over). BUILD.md, *The
roadmap*, has the commands and the link settings.

This directory is outside `docs/`, so the file itself is not a page of the site.
