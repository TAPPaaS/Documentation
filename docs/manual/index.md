---
title: Operate TAPPaaS
description: >
  Run a live TAPPaaS system day to day — the manager/controller operating model,
  with reference pages that are always current with the source code.
---

# Operate TAPPaaS

TAPPaaS 2.0 is operated through a small set of **managers** and **controllers**,
running on the CICD mothership:

- **Managers** own a *domain* of the platform — one per part of the
  [taxonomy](https://github.com/TAPPaaS/TAPPaaS/blob/ADR007/docs/ADR/ADR-007%20-%20TAPPaaS%20Taxonomy.md): Site, People, Module (Apps),
  Environment, Network, Backup, Health, and Satellite. When you install, update or
  reconfigure something, you talk to a manager.
- **Controllers** wrap a *concrete system* — OPNsense, Proxmox, the identity stack,
  backup, access points, switches, node provisioning — and expose it to the managers.
  You rarely call a controller directly, but they're where the system-specific
  knowledge (and troubleshooting detail) lives.

So: **managers decide, controllers do.** A day-to-day operation like "update all
modules" is a manager conversation; "why didn't the VLAN get created" is a controller
page.

## Reference

These pages are always current with the source code (new managers and controllers
appear here automatically):

- **Managers** — see the *Managers* section in the sidebar: one page per manager
  (site, people, module, environment, network, backup, health, satellite).
- **Controllers** — see the *Controllers* section: one page per controller
  (opnsense, proxmox, identity, backup, ap, switch, node-provisioner).
- **[Network Zones](../generated/zones.md)** — the zone model the network manager
  maintains and the firewall enforces.

## Related

- [Install TAPPaaS](../installation/index.md) — getting to a running system.
- [Branch Selection](../installation/preparation.md#4-branch-selection) — the 2.0 status of what is described here.
- [Develop](../architecture/index.md) — how the managers/controllers are designed.
