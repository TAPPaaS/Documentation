---
title: Stacks
description: >
  TAPPaaS capabilities come in stacks — containers of related modules. What each
  stack delivers, with every module's catalog entry one click away.
---

# Stacks

A **stack** is a container of related capabilities, delivered by **modules** — the
smallest deployable units in TAPPaaS (see the
[Capabilities](../capabilities.md) overview and the
[Meta Model](../meta-model.md) for how this is modeled).

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
[module dependency graph](../../generated/module-dependencies.md).

Modules that serve every stack rather than one: **[NetBird Client](../../generated/modules/netbird-client.md)**
(mesh connectivity) and **[Windows Server](../../generated/modules/windows-server.md)**
(run Windows workloads as managed modules).
