---
title: Author a Module
description: >
  Package your own application as a TAPPaaS module — from copying the 00-Template
  to passing install, update and backup like every built-in module.
---

# Author a Module

A TAPPaaS **module** is the unit everything else revolves around: it typically runs in
its own VM, and the platform installs, updates, backs up and health-checks it like any
other. If your favourite app isn't in the [gallery](../intro/examples.md) yet, this is
how you add it.

## The short version

1. **Copy the template.** The
   [`00-Template`](https://github.com/TAPPaaS/TAPPaaS/tree/ADR007/src/apps/00-Template)
   app is the canonical starting point — its synced README is here:
   [Module template (source)](../generated/module-template.md). The module name you
   choose becomes the VM name, hostname and DNS name.
2. **Fill in the module contract.** Configuration and metadata are schema-checked —
   the field definitions per taxonomy domain (module, environment, organization,
   group, role, satellite) live in
   [`src/foundation/schemas/`](https://github.com/TAPPaaS/TAPPaaS/tree/ADR007/src/foundation/schemas),
   described in the synced [Schemas reference](../generated/schemas.md).
3. **Understand where your module runs.** Modules live inside **Environments** —
   zones with firewall boundaries; see [Network Zones (source)](../generated/zones.md)
   and the [taxonomy](../generated/adr-007-taxonomy.md) for how your module is
   classified (it's an **App**).
4. **Install and iterate with the Module Manager** — the manager that installs,
   updates and tests modules (the old standalone scripts now live inside it). See
   [Module Manager (source)](../generated/managers/module-manager.md).
5. **Make it a good citizen.** A finished module updates unattended via the
   [Module Manager](../generated/managers/module-manager.md), is covered by the
   [Backup Manager](../generated/managers/backup-manager.md), and reports into the
   [Health Manager](../generated/managers/health-manager.md).

## The deeper reference

- [Module Structure](cicd-design/module-structure.md) — what a module consists of.
- [CICD Script Structure](cicd-design/script-structure.md) — how the automation calls
  into your module.
- [Git Structure](cicd-design/git-structure.md) — where your module lives in the repo.
- [Meta Model](meta-model.md) — how deployable units compose (ADR-009).

## Contributing your module

Modules are contributed via pull request to the
[TAPPaaS source repo](https://github.com/TAPPaaS/TAPPaaS) — see the
[contribution guide](../community/contributing.md). Good first check before you start:
open an issue describing the app; someone may already be packaging it.
