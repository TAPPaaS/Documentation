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

1. **[Develop a Module](develop-a-module.md)** — the path from `00-Template` copy to a
   shipped module: quick start, the contract, debugging, contributing.
2. **[Module Template](../generated/module-template.md)** — the annotated template every
   module starts from (synced from source).

## Decide in writing first

Structural changes start as an ADR in the source repo
([overview](../generated/adrs.md)) — write the decision before the code, and test the
idea against the [design principles](../what/principles.md).
