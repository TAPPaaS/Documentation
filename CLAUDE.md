# Claude Code Instructions

## Repo layout & environments

- **This Codeberg repo is the primary** (`origin` = codeberg.org/TAPPaaS/Documentation). Pushing
  `main` deploys **staging** at <https://staging.tappaas.org> via Woodpecker CI.
- The `github` remote publishes **production 1.x** (tappaas.org). Do **not** push there unless
  explicitly asked — production stays frozen until the 2.0 cutover (ADR-001 §10.1).
- The upgrade plan and all infrastructure learnings live in `ADR/ADR001-rearchitect.md`;
  read §11a.5 before changing anything about CI, Pages, or DNS.

## Publishing Changes

When asked to publish or push changes:

1. **Small edits**: commit directly to `main`, `git push` — staging deploys automatically
   (Pages edge cache can delay visibility up to ~10 minutes).
2. **Substantial changes**: use a `spike-*`/feature branch; the pipeline publishes a preview at
   `https://tappaas.codeberg.page/Documentation/spikes/<branch>/` for review before merging.
3. Do **not** create pull requests unless asked.

## Gotchas

- `docs/generated/` is build-time output of `scripts/sync-source.py` (WS0) — never edit or commit
  it; content changes belong upstream in codeberg.org/TAPPaaS/TAPPaaS.
- Local `mkdocs build --strict` needs Python ≥ 3.10 (Kroki plugin) and a Kroki server
  (`docker-compose up -d`, or strip the kroki plugin from a temp config copy).
- CI logs on ci.codeberg.org are not publicly readable; debug via commit statuses or by having a
  step publish diagnostics.
