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
| [Productivity](productivity.md) | Files, collaboration, passwords, office |
| [Home](home.md) | Home automation and (planned) home media |
| [IoT](iot.md) | Device gateways, isolated in their own zones |
| [DevOps](devops.md) | Development and test capabilities (planned) |

Each stack page links the **module catalog entries** (the modules' own READMEs,
always current with the source). How modules depend on each other is computed from
the modules themselves: see the
[module dependency graph](../generated/module-dependencies.md).

Modules that serve every stack rather than one: **[NetBird Client](../generated/modules/netbird-client.md)**
(mesh connectivity) and **[Windows Server](../generated/modules/windows-server.md)**
(run Windows workloads as managed modules).

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
