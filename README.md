# TAPPaaS Documentation

Documentation site for TAPPaaS - Trusted Automated Private Platform as a (selfhosted) Service.

| Environment | URL | Built from |
|-------------|-----|------------|
| **Production** | <https://tappaas.org> / <https://www.tappaas.org> | **This repo (Codeberg)**, push to `main` (Woodpecker CI → Codeberg Pages). One MkDocs site; the landing is the home page (`overrides/home.html`) |
| **Staging** | <https://staging.tappaas.org> | This repo (Codeberg), push to `main` or the `staging` branch — same build/pipeline as production |
| Fallback URL | <https://tappaas.codeberg.page/Documentation/> | same build |
| Branch previews | `https://tappaas.codeberg.page/Documentation/spikes/<branch>/` | any `spike-*` branch |

**This Codeberg repo is the primary and sole home of the site** (see
[`ADR/ADR001-rearchitect.md`](ADR/ADR001-rearchitect.md)). The 2.0 cutover is complete —
<https://tappaas.org> is now served from here via Codeberg Pages; the previous GitHub-Actions
publish path is retired.

## Making Changes

Edit the markdown files in the `docs/` folder.

- **Small edits** (typos, small content fixes): commit straight to `main` and push — staging
  redeploys automatically (allow up to ~10 minutes for the Pages edge cache).
- **Substantial changes**: use a `spike-*` (or feature) branch → the pipeline publishes a preview
  under `…/Documentation/spikes/<branch>/` → review → merge to `main`.

Pages marked *(source)* — synced INSTALL docs, all *Managers*/*Controllers* pages, zones, schemas,
the taxonomy — are **generated at build time** from the TAPPaaS source repo (Codeberg, branch
`main` by default; override with the `TAPPAAS_SOURCE_REF` env) by
[`scripts/sync-source.py`](scripts/sync-source.py) (WS0) — edit them **upstream** in
[TAPPaaS/TAPPaaS](https://codeberg.org/TAPPaaS/TAPPaaS), not here. New manager/controller READMEs
upstream appear automatically (glob + generated SUMMARY.md + literate-nav); other new files need an
allow-list line. See ADR-001 §12.2 — including the one-time Woodpecker cron for nightly freshness.

## Local Development

```bash
pip install -r requirements.txt   # needs Python >= 3.10 for the Kroki plugin
docker-compose up -d              # self-hosted Kroki for diagram rendering
python3 scripts/sync-source.py    # generate the synced source pages
mkdocs serve                      # http://127.0.0.1:8000
```

Verify before pushing:

```bash
mkdocs build --strict
```

## CI / hosting notes

The Woodpecker pipeline ([`.woodpecker.yml`](.woodpecker.yml)) builds MkDocs with a Kroki service
container and publishes the single `pages` branch, which Codeberg's git-pages server serves. The
hard-earned details (webhook self-notify, custom-domain DNS, edge cache, preview sub-directories)
are documented in ADR-001 §11a.5 — read that before touching the pages setup.
