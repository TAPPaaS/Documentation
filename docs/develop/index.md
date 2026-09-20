---
title: Develop — Build a TAPPaaS Module
description: >
  The Develop track: port your application to TAPPaaS as a module the platform
  installs, updates, backs up and health-checks like any built-in.
---

# Developing TAPPaaS

This is the **Develop** track: everything you need to bring your own application onto
TAPPaaS. If you're *running* a system, you want [Operate](../operate/index.md); if you
want the platform's concepts and design, that's What ([capabilities](../what/capabilities.md),
[principles](../what/principles.md), [design](../what/design.md), [ADRs](../generated/adrs.md)).

If instead you want to understand how TAPPaaS *itself* is built — the release process,
images and CI behind the platform — see [TAPPaaS Build Process](../generated/build.md).

## The one idea to hold on to

Everything deployable is a **module**: a directory with a json contract
(`<module>.json` — schema-checked, declares zones, sizing, `dependsOn` and the
services it `provides`), the scripts the platform calls (`install.sh`, `update.sh`,
`test.sh`), and its docs (README / INSTALL). In the
[taxonomy](../generated/adrs.md), your module is an **App**; it runs inside an
**Environment**; managers operate it for the rest of its life.

## What the platform does with it

The **CICD mothership** (`tappaas-cicd`) is the control plane — a VM that holds the
git checkout and drives every module through the same lifecycle, fronted by the
[Module Manager](../generated/managers/module-manager.md):

```bash
module-manager module add myapp        # create the VM, resolve dependsOn, run install.sh
module-manager module modify myapp     # release update: snapshot + test + merge
module-manager module test myapp       # run your test.sh — the same tests gate updates
```

Updates then run unattended on the platform's schedule. Under the hood **managers
decide, controllers do** — your module talks to the platform only through its json
contract, never by hand-wiring firewalls or DNS. The full design is under What → Design:
[CICD Mothership](../generated/design/cicd-mothership.md) and
[Git & Repository Topology](../generated/design/cicd-git.md).

## Start here

1. **[Develop a Module](../generated/develop-a-module.md)** — the quick start: from
   `00-Template` copy to a shipped module.
2. **[Module Details](../generated/module-template.md)** — the reference behind it:
   every file, field and convention of a module.

Both are maintained with the template itself in the source repo
(`src/apps/00-Template/`) and synced here at build time.

## Changing the shape of a config

A module's own config is yours to change with
[`module-manager module modify`](../generated/managers/module-manager.md). Changing the
*shape* every site's `config/` is written in — a renamed field, a changed type, a module
that moves to another repository — is a **migration**, and it ships with the release that
needs it: see **[Config Migrations](../generated/config-migrations.md)** for how to write
one, the contract it meets, the fixture test it ships with, and `move-module.sh` for moving
a module without writing one by hand.
