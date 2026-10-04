---
title: Stacks
description: >
  TAPPaaS capabilities come in stacks — containers of related modules. What each
  stack delivers, with every module's catalog entry one click away.
---

# Stacks

A **stack** is a container of related capabilities, delivered by **modules** — the
smallest deployable units in TAPPaaS (see the
[Capabilities](../what/capabilities.md) overview and the
[Meta Model](../what/meta-model.md) for how this is modeled).

| Stack | What it delivers |
|-------|------------------|
| [Foundation](foundation.md) | The platform itself: cluster, network, identity, backup, logging, automation |
| [AI](ai.md) | Private AI: model serving, gateway, chat UI |
| [Collaboration](collaboration.md) | Files, office documents and calls |
| [Home](home.md) | Home automation, its device gateways, and (planned) home media |
| [Security](security.md) | Secrets and secure access |
| [Miscellaneous](misc.md) | Modules with no natural stack yet |
| DevOps | Development and test capabilities — **planned, no modules yet** (see below) |

Each stack page is the stack's own README in the source, followed by its **module catalog
entries** (the modules' own READMEs) — always current with the source. How to install a
stack is under [Install → Add Workloads](../generated/install/ai/index.md). How modules depend on each other is computed from
the modules themselves: see the
[module dependency graph](../generated/module-dependencies.md).

Every module declares exactly one stack, in its own JSON — the list lives in
`schemas/module-fields.json` and this page follows it. A module with no natural stack
yet is [`misc`](misc.md) — a waiting room, not a description.

**DevOps (planned).** The capabilities needed to develop, test and deploy software on
TAPPaaS. The platform's own automation (the
[TAPPaaS CICD](../generated/foundation/tappaas-cicd.md) mothership) covers module
lifecycle today; developer-facing modules (forge, CI runners, registries) are on the
[roadmap](../roadmap/index.md). The stack gets its page once it has a module.

## Module deployment pattern

Every module follows the same deployment pattern — one json contract, the platform
scripts, a VM provisioned via `cluster:vm`, exposure via `network:proxy`, protection
via `backup:vm`:

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title TAPPaaS Module Deployment Pattern

' Module artifacts
Technology_Artifact(config, "module.json")
Technology_Artifact(install, "install.sh")
Technology_Artifact(update, "update.sh")
Technology_Artifact(test, "test.sh")

' Infrastructure Technology Services
Technology_Service(vmSvc, "cluster:vm")
Technology_Service(haSvc, "cluster:ha")
Technology_Service(proxySvc, "network:proxy")

' Technology Node (VM)
Technology_Node(vm, "NixOS VM")

' Application running on VM
Application_Component(app, "Application")

' Backup
Technology_Service(snapshot, "backup:vm (PBS)")

' Configuration flow
Rel_Association(config, install, "configures")

' Install uses VM service
Rel_Access(install, vmSvc, "provisions")

' VM service creates node
Rel_Realization(vmSvc, vm)

' Application assigned to VM
Rel_Assignment(vm, app)

' HA and proxy serve VM
Rel_Serving(haSvc, vm, "failover")
Rel_Serving(proxySvc, vm, "exposes")

' Snapshot protects VM
Rel_Serving(snapshot, vm, "protects")

@enduml
```
