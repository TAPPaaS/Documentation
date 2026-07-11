---
title: Architecture Decision Records
description: >
  Every significant TAPPaaS decision is written down before it is built — the
  ADRs are the authoritative record. Overview and pointers.
---

# Architecture Decision Records

Significant decisions in TAPPaaS are made in writing, **before the code**: each one is
an ADR (Architecture Decision Record) in the source repository, and it stays there
forever — superseded ADRs are marked, never deleted. If you want to know *why* the
platform is the way it is, this is the trail.

**The authoritative list lives in the source repo:
[`docs/ADR/`](https://github.com/TAPPaaS/TAPPaaS/tree/ADR007/docs/ADR).**

## The 2.0 spine — the taxonomy family

| ADR | Decides |
|-----|---------|
| [ADR-007 — TAPPaaS Taxonomy](../generated/adr-007-taxonomy.md) | The model everything hangs on: one **Site**, three classification domains (**People · Apps · Environments**), **Health** as a cross-cutting lens. Detailed per domain in sub-ADRs 007a–007e, realization (managers/controllers) in 007f. *(Synced on this site — the sub-ADRs are linked from it.)* |
| [ADR-009 — Composition Meta-Model](https://github.com/TAPPaaS/TAPPaaS/blob/ADR007/docs/ADR/ADR-009%20-%20Composition%20Meta-Model.md) | How a deployable unit is *built* (module = atomic deployable unit; `<module>:<service>` coordinates) — composition, as distinct from ADR-007's classification. |

## Platform decisions

| ADR | Decides |
|-----|---------|
| [ADR-001 — Trunk-mode VLAN connectivity](https://github.com/TAPPaaS/TAPPaaS/blob/ADR007/docs/ADR/ADR-001%20-%20Use%20Trunk%20Mode%20for%20TAPPaaS%20VM%20VLAN%20Connectivity.md) | VMs attach on trunk ports; zones are VLANs. |
| [ADR-002 — Dynamic VLAN configuration](https://github.com/TAPPaaS/TAPPaaS/blob/ADR007/docs/ADR/ADR-002-Dynamic%20VLAN%20Configuration%20for%20TAPPaaS%20VM%20Deployment.md) | Zone/VLAN wiring happens at deploy time, driven by module config. |
| [ADR-003 — Dependency management](https://github.com/TAPPaaS/TAPPaaS/blob/ADR007/docs/ADR/ADR-003%20-%20Dependency%20management%20in%20TAPPaaS.md) | Modules declare `dependsOn`; install order is derived, never hardcoded. |
| [ADR-004 — Module catalog & config cascade](https://github.com/TAPPaaS/TAPPaaS/blob/ADR007/docs/ADR/ADR-004-module-catalog-config-cascade.md) | Where module configuration comes from and how overrides cascade. |
| [ADR-005 — Variant domain architecture](https://github.com/TAPPaaS/TAPPaaS/blob/ADR007/docs/ADR/ADR-005-variant-domain-architecture.md) | *Superseded in practice by the ADR-007 Environments model (variants → environments).* |
| [ADR-006 — Identity: users and roles](https://github.com/TAPPaaS/TAPPaaS/blob/ADR007/docs/ADR/ADR-006-identity-users-and-roles.md) | The identity model behind SSO (Authentik) — users, groups, roles. |
| [ADR-008 — Switch module / network infrastructure](https://github.com/TAPPaaS/TAPPaaS/blob/ADR007/docs/ADR/ADR-008-switch-module-network-infrastructure.md) | Physical switches and APs become managed parts of the platform. |
| [ADR-010 — VPS satellite](https://github.com/TAPPaaS/TAPPaaS/blob/ADR007/docs/ADR/ADR-010-vps-satellite-reverse-proxy-backup.md) | The optional off-premises satellite: public ingress, off-site backup, admin VPN. |
| [ADR-012 — Backup enhancement](https://github.com/TAPPaaS/TAPPaaS/blob/ADR007/docs/ADR/ADR-012-backup-enhancement.md) | The managed backup-policy model (site → environment → module cascade). |

## Governance

| ADR | Decides |
|-----|---------|
| [ADR-011 — SBOM Governance](https://github.com/TAPPaaS/TAPPaaS/blob/ADR007/docs/ADR/ADR-011%20-%20SBOM%20Governance.md) | Per-module software bill of materials (CycloneDX) for CVE tracking. |
| [ADR-013 — Documentation Structure and Standards](https://github.com/TAPPaaS/TAPPaaS/blob/ADR007/docs/ADR/ADR-013%20-%20Documentation%20Structure%20and%20Standards.md) | Where documentation lives, which artifact serves which audience, and how this site syncs from source. |

---

Writing a new ADR is part of [developing TAPPaaS](../architecture/index.md) — decide in
writing first, test the idea against the [design principles](../intro/design-principles.md).
