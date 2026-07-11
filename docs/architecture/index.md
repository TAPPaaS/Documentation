---
title: Develop — Build a TAPPaaS Module
description: >
  The Develop track: how modules are structured, how the CICD mothership installs,
  updates and tests them, and how to package your own app for TAPPaaS.
---

# Developing TAPPaaS

This is the **Develop** track: everything you need to extend TAPPaaS with your own
module. If you're *running* a system, you want [Operate](../manual/index.md); if you
want the platform's concepts and design, that's [What](../what/adrs.md) (capabilities,
principles, [taxonomy](https://github.com/TAPPaaS/TAPPaaS/blob/ADR007/docs/ADR/ADR-007%20-%20TAPPaaS%20Taxonomy.md), foundation design, ADRs).

## The one idea to hold on to

Everything deployable is a **module**: a directory with a json contract
(`<module>.json` — schema-checked, declares zones, sizing, `dependsOn` and the
services it `provides`), the scripts the platform calls (`install.sh`, `update.sh`,
`test.sh`), and its docs (README / INSTALL / DESIGN). In the
[taxonomy](https://github.com/TAPPaaS/TAPPaaS/blob/ADR007/docs/ADR/ADR-007%20-%20TAPPaaS%20Taxonomy.md), your module is an **App**; it runs
inside an **Environment**; managers operate it for the rest of its life.

## How the CICD works

The **CICD mothership** (`tappaas-cicd`) is the platform's control plane — a VM that
holds the TAPPaaS git checkout and runs everything:

1. **Install**: `install-module.sh <module>` stages and validates your json, resolves
   `dependsOn` (creating the VM via `cluster:vm` first), then runs your `install.sh`
   for the module-specific work.
2. **Update**: the module manager runs `update.sh` on schedule — modules keep
   themselves patched without operator attention.
3. **Test**: `test-module.sh <module>` runs your `test.sh` — the same tests gate
   regressions after updates.
4. Under the hood, **managers decide, controllers do** — your module talks to the
   platform through its json contract, never by hand-wiring firewalls or DNS. See
   [How the CICD works](cicd-design/index.md) for the full design (git structure,
   module structure, script contracts).

## Start here

1. **[Author a Module](author-a-module.md)** — the 5-step path from `00-Template`
   copy to a good platform citizen.
2. **[How the CICD works](cicd-design/index.md)** — what the automation does with
   your module.
3. **[Meta Model](meta-model.md)** — composition rules (ADR-009): what a deployable
   unit is, `<module>:<service>` coordinates.
4. **[ArchiMate Diagrams](../appendix/archimate/introduction.md)** — the formal
   architecture views, rendered from source.

## Decide in writing first

Structural changes start as an ADR in the source repo
([`docs/ADR/`](https://github.com/TAPPaaS/TAPPaaS/tree/ADR007/docs/ADR) — overview
[here](../what/adrs.md)) — write the decision before the code, and test the idea
against the [design principles](../intro/design-principles.md).
