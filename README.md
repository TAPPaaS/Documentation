# TAPPaaS Documentation

Documentation site for TAPPaaS - Trusted Automated Private Platform as a (selfhosted) Service.

| Environment | URL | Built from |
|-------------|-----|------------|
| **Production (1.x)** | <https://tappaas.org> | GitHub mirror, push to `main` (GitHub Actions) — untouched until the 2.0 cutover |
| **Staging (2.0 work)** | <https://staging.tappaas.org> | **This repo (Codeberg)**, push to `main` (Woodpecker CI → Codeberg Pages). Root = Astro landing (`landing/`); docs under `/docs/` |
| Staging fallback URL | <https://tappaas.codeberg.page/Documentation/> | same as staging |
| Branch previews | `https://tappaas.codeberg.page/Documentation/spikes/<branch>/` | any `spike-*` branch |

**This Codeberg repo is the primary home** — all 2.0 upgrade work happens here (see
[`ADR/ADR001-rearchitect.md`](ADR/ADR001-rearchitect.md)). The GitHub copy only keeps publishing
the live 1.x site until the one-time cutover (ADR-001 §10.1).

## Making Changes

Edit the markdown files in the `docs/` folder.

- **Small edits** (typos, small content fixes): commit straight to `main` and push — staging
  redeploys automatically (allow up to ~10 minutes for the Pages edge cache).
- **Substantial changes**: use a `spike-*` (or feature) branch → the pipeline publishes a preview
  under `…/Documentation/spikes/<branch>/` → review → merge to `main`.

Pages under *Installation → From Source (synced)* are **generated at build time** from the TAPPaaS
source repo by [`scripts/sync-source.py`](scripts/sync-source.py) (WS0) — edit them **upstream** in
[TAPPaaS/TAPPaaS](https://github.com/TAPPaaS/TAPPaaS), not here.

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
