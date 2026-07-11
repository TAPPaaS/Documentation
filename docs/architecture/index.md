---
title: Develop — Architecture Overview
description: >
  How TAPPaaS is built: the ADR-007 taxonomy (Site · People · Apps · Environments ·
  Health) as the architecture spine, plus solution design, CICD and module authoring.
---

# Architecture Overview

This is the **Develop** track: how TAPPaaS is designed, for contributors and module
authors. If you're *running* a system, you want [Operate](../manual/index.md) instead.

## The spine: one taxonomy for everything

The architecture of TAPPaaS 2.0 is organised by **ADR-007 — the TAPPaaS taxonomy**.
One **Site** (the physical and administrative perimeter — one TAPPaaS = one Site)
contains **three classification domains**, with one cross-cutting lens:

```
┌─────────────────────────────────────────────────────────────┐
│ 🏢 SITE  (the physical + admin perimeter — one TAPPaaS)     │
│   ┌───────────────────────────────────────────────────────┐ │
│   │ 👥 PEOPLE          📦 APPS          🏠 ENVIRONMENTS   │ │
│   │ Org→Group→User     what runs        where apps run    │ │
│   └───────────────────────────────────────────────────────┘ │
│   🩺 HEALTH  (lens — observability over all of the above)   │
└─────────────────────────────────────────────────────────────┘
```

- **People** — organizations, groups, users: identity and access.
- **Apps** — everything that runs, classified by tier and source.
- **Environments** — where apps run: zones, domains, update windows.
- **Health** — not a domain but a *lens*: status and observability overlaid on all of it.

Every artifact on the platform is exactly one of People / Apps / Environments (the
model is MECE); *how* a deployable unit is composed is a separate concern (ADR-009,
see the [meta model](meta-model.md)).

This is the same model the [front page](../intro/index.md) tells as *Site · Workloads ·
People · Environments* — "Workloads" is the everyday word for Apps. One mental model,
two altitudes.

!!! note "2.0 status"
    ADR-007 is the accepted basis for **TAPPaaS 2.0** and is being implemented now;
    1.x (today's `stable`) predates it. See
    [Stable vs Main](../installation/versions.md) for what that means when installing.
    The full ADR text is synced from source:
    [ADR-007 — TAPPaaS Taxonomy](../generated/adr-007-taxonomy.md).

## The sections

- **[Taxonomy (ADR-007, source)](../generated/adr-007-taxonomy.md)** — the model, its
  decision tree, and the sub-ADRs per domain.
- **[Capabilities](capabilities.md)** — what the platform can do, top-level structure.
- **[Solution Design](solution-design/index.md)** — the concrete design: software
  selection, network, storage, security, SSO, backup.
- **[CICD Design](cicd-design/index.md)** — the automation that installs, updates and
  heals everything: git structure, module structure, scripts.
- **[Module Designs](module-designs/index.md)** — per-stack module specifications.
- **[Meta Model](meta-model.md)** — the general concepts (composition, ADR-009).
- **[Author a Module](author-a-module.md)** — the contributor path: package your own
  app for TAPPaaS.
- **[ArchiMate Diagrams](../appendix/archimate/introduction.md)** — the enterprise
  architecture views, rendered from source with Kroki.

## Where decisions live

Architecture decisions are recorded as ADRs in the source repository:
[`docs/ADR/`](https://github.com/TAPPaaS/TAPPaaS/tree/ADR007/docs/ADR). If you're about
to change something structural, start there — write the ADR before the code, and test
the idea against the [design principles](../intro/design-principles.md).
