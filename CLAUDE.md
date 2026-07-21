# Claude Code Instructions

## Repo layout & environments

- **This Codeberg repo is the primary** (`origin` = codeberg.org/TAPPaaS/Documentation).
  **Pushing `main` deploys PRODUCTION** — <https://tappaas.org> (plus `www`, `staging.tappaas.org`
  and `tappaas.codeberg.page/Documentation/`, all serving the same build) via Woodpecker CI +
  Codeberg git-pages. Cutover from GitHub completed 2026-07-21 (ADR-001 §10.1).
- The `github` remote is a **retired archive** of the pre-2.0 site — Pages and its workflow are
  removed. Do **not** push there.
- The upgrade plan and all infrastructure learnings live in `ADR/ADR001-rearchitect.md`;
  read §11a.5 and §10.1 before changing anything about CI, Pages, or DNS.

## Publishing Changes

`main` is live — treat every push as a production deploy:

1. **Small edits** (typo, link, wording): commit directly to `main`, `git push` — production
   deploys automatically (git-pages edge cache can delay visibility up to ~10 minutes).
2. **Substantial changes**: use a `spike-*` branch; the pipeline publishes a preview at
   `https://tappaas.codeberg.page/Documentation/spikes/<branch>/` — review there **before**
   merging to `main`.
3. Do **not** create pull requests unless asked.

## Gotchas

- `docs/generated/` is build-time output of `scripts/sync-source.py` (WS0) — never edit or commit
  it; content changes belong upstream in codeberg.org/TAPPaaS/TAPPaaS.
- git-pages deployments are **per-domain**: the deploy step must `notify()` every served hostname
  (see `.woodpecker.yml`). A domain that is routed but never deployed gets **no TLS cert**
  (ADR-001 §11a.5 gotcha 9).
- Custom-domain DNS lives in Cloudflare, **grey cloud (DNS-only) always**; the apex additionally
  needs the `_git-pages-repository` TXT record (ADR-001 §10.1).
- Local `mkdocs build --strict` needs Python ≥ 3.10 (Kroki plugin) and a Kroki server
  (`docker-compose up -d`, or strip the kroki plugin from a temp config copy).
- CI logs on ci.codeberg.org are not publicly readable; debug via commit statuses or by having a
  step publish diagnostics.
