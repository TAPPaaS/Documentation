---
title: Branch Selection
description: >
  Which TAPPaaS branch to install from — stable or main — and where the 2.0
  transition currently stands.
---

# Branch Selection

The bootstrap command takes a branch (`BRANCH="..."` in the
[install guide](../generated/install.md)). Choose it here, before you start.

| Branch | What it is | Who should install it |
|--------|------------|-----------------------|
| **`stable`** | The released, supported version of TAPPaaS | Everyone running a real system |
| **`main`** | Ongoing development — moves fast, may break | Contributors, and evaluators who want the newest work |

**If in doubt, choose `stable`.** The difference in practice: `stable` only moves
when a release is cut and tested; `main` moves with every merged change. A system
installed from one branch tracks that branch through the automated updates — so the
choice you make here is the risk profile you keep.

## Migrating from ADR007 to 2.0

*(Transitional note — this section disappears once the transition is complete.)*

The next major release (**2.0** — the taxonomy and manager/controller platform) is
being finished on the **`ADR007`** branch and will be promoted to `stable` per the
[roadmap](../roadmap/index.md). Until that promotion:

- **New 2.0 installs** use `BRANCH="ADR007"` in the bootstrap command. This site
  documents 2.0 — the synced pages here track `ADR007`.
- **Existing 1.x/main systems** convert with the migration runbook maintained in the
  source repo:
  [ADR-007 migration runbook](https://github.com/TAPPaaS/TAPPaaS/blob/ADR007/docs/design/ADR-007-migration-runbook.md).
- **At promotion**, `stable` simply becomes 2.0: new installs go back to the default,
  and this section gets deleted.
