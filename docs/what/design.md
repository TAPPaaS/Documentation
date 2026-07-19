---
title: Design
description: How TAPPaaS is designed, module by module
---

# Design

How TAPPaaS is designed, module by module. The module pages below are kept in sync from the source
repository; the security design is cross-cutting and maintained here.

- **[Security](security-design.md)** — secrets, access control, network segmentation, ingress,
  monitoring, and breach resilience.
- **[Cluster](../generated/design/cluster.md)** — the Proxmox/ZFS foundation: storage tiers,
  high availability, adding nodes.
- **[Network](../generated/design/network.md)** — OPNsense firewall, security zones, DNS, the
  reverse proxy, and resilience (including public ingress without a public IP).
- **[Backup](../generated/design/backup.md)** — the 3-2-1 strategy, PBS placement, off-site
  replication, and disaster recovery.
