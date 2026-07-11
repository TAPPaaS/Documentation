---
title: Foundation Stack
description: >
  The modules the platform itself is made of — cluster, network, templates,
  automation, backup, identity, logging, satellite.
---

# Foundation Stack

The foundation is what makes TAPPaaS a *platform* rather than a pile of VMs. Its
design is described under [What → Foundation](../solution-design/index.md); here is
the module catalog:

| Module | Role |
|--------|------|
| [Cluster](../../generated/foundation/cluster.md) | Proxmox nodes, storage pools, HA — the ground everything stands on |
| [Network](../../generated/foundation/network.md) | OPNsense firewall: zones, DNS, DHCP, reverse proxy, rules |
| [Templates](../../generated/foundation/templates.md) | The prebuilt VM templates modules deploy from |
| [TAPPaaS CICD](../../generated/foundation/tappaas-cicd.md) | The mothership: managers and controllers that run the platform |
| [Backup](../../generated/foundation/backup.md) | Proxmox Backup Server: scheduled, verified, off-site capable |
| [Identity](../../generated/foundation/identity.md) | Authentik: SSO, users, groups, organisations |
| [Logging](../../generated/foundation/logging.md) | Loki / Grafana / Promtail: central logs |
| [Satellite](../../generated/foundation/satellite.md) | Optional VPS: public ingress, off-site backup, admin VPN |
