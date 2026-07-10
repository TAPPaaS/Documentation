---
title: Stable vs Main — and what 2.0 is
description: >
  Which TAPPaaS branch to install (stable = 1.x today, main = the 2.0 / ADR-007
  preview), what changes in 2.0, and how the cutover will happen.
---

# Stable vs Main — and what 2.0 is

TAPPaaS development runs on two branches of the
[source repository](https://github.com/TAPPaaS/TAPPaaS):

| Branch | What it is | Who should install it |
|--------|------------|-----------------------|
| **`stable`** | **TAPPaaS 1.x** — the current supported release | Everyone running a real system |
| **`ADR007`** | The **2.0 release branch** (manager/controller paradigm) — will be promoted to `stable` per the [roadmap](../roadmap/index.md) | Evaluators and contributors |

**If in doubt, install `stable`.** The synced pages on this site
(the [INSTALL.md](../generated/install.md), managers, controllers, …) track **`ADR007`**,
since this staging site documents 2.0.

---

## What 2.0 changes (the short version)

The heart of 2.0 is **ADR-007 — the TAPPaaS taxonomy**: one clear model for everything
on the platform, used identically in the product, the docs and the marketing story.

- One **Site** — the physical and administrative perimeter (one TAPPaaS = one Site).
- Three **classification domains** — every artifact is exactly one of:
  **People** (organizations, groups, users), **Apps** (what runs), and
  **Environments** (where apps run: zones, domains, update windows).
- One cross-cutting **Health** lens — status and observability over all of it.

If you've read [Why TAPPaaS](../intro/index.md): the front page's four building blocks
— *Site · Workloads · People · Environments* — are this same model; "Workloads" is the
everyday word for Apps. One mental model, two altitudes. The full detail is in the
[Architecture section](../architecture/index.md).

!!! note "Status honesty"
    ADR-007 is implemented on its feature branch and expected to become **release 2.0**
    on `stable`. Until that merge happens, 1.x semantics are what you get when you
    install `stable` — this page and the architecture docs describe where the platform
    is *going*, and this staging site previews it.

## How the cutover will happen

When 2.0 lands on `stable`:

1. This documentation (built and reviewed on staging) is promoted to **tappaas.org**
   in a one-time content flip — no period of dual 1.x/2.0 docs, no versioned archive.
2. The install flow drops the "which branch" question back to a footnote: `stable`
   simply *is* 2.0.
3. Existing 1.x systems follow the migration guidance that ships with the release.

Until then: **run `stable`**, and watch the [roadmap](../roadmap/index.md) for the 2.0
milestone.
