---
title: Install TAPPaaS
description: >
  Installing TAPPaaS in seven clear stages — from choosing hardware to handing
  over to day-to-day operation.
---

# Install TAPPaaS

TAPPaaS installs as a set of interlinked foundation modules and platform services,
built and configured to work together. The process is **seven stages**; each one tells
you what it needs, and what "done" looks like before you move on.

!!! warning "Which version to install: `stable` (1.x) vs `main` (2.0 preview)"
    The supported install today is **TAPPaaS 1.x from the `stable` branch**. The next
    major release (**2.0**, built around the ADR-007 taxonomy) is under active
    development on `main` — the right choice only if you are evaluating or
    contributing. **[Full guidance: stable vs main, and what 2.0 is](versions.md).**

    The exact, always-current procedure is synced from the source repo:
    [INSTALL.md (source)](../generated/install.md).

## The seven stages

| # | Stage | You'll need | Done when |
|---|-------|-------------|-----------|
| 1 | [Choose hardware](#stage-1-choose-hardware) | An honest look at your needs | Hardware ordered/on the bench, sized by tier + options |
| 2 | [Prepare](#stage-2-prepare) | Domain, DNS access, wired network | Network plan, credentials and DNS records ready |
| 3 | [Bootstrap the foundation](#stage-3-bootstrap-the-foundation) | Stage 1 + 2 complete | First node, firewall and CICD mothership up; you can log in |
| 4 | [Grow the cluster](#stage-4-grow-the-cluster-optional) *(optional)* | Additional nodes | All nodes joined; HA where intended |
| 5 | [Add stacks](#stage-5-add-stacks) | A running foundation | The apps you chose are installed and reachable |
| 6 | [Cut over the network](#stage-6-cut-over-the-network) | A maintenance window | TAPPaaS firewall is your network's edge |
| 7 | [Operate](#stage-7-operate) | — | Updates, backup and health checks running on schedule |

---

## Stage 1 — Choose hardware

Pick a **size tier** (Evaluation / Home / SMB / Scale-out), then toggle three
**capability options** — local AI, local backup, local public IP — independently.
The [hardware selection guide](hardware-selection.md) walks the decision in four steps
and gives per-tier sizing tables.

**Done when:** you know your tier, your options, and the machine(s) are in hand.

[:octicons-arrow-right-24: Hardware selection](hardware-selection.md)

## Stage 2 — Prepare

Plan the network, register/point your domain, and gather credentials before touching
any installer. See the [preparation guide](preparation.md), and the prerequisites
section of the synced [INSTALL.md](../generated/install.md).

**You'll need:** a reliable wired connection, a registered domain with DNS management,
and a strong root password policy for hypervisor and firewall.

**Done when:** the checklist in [preparation](preparation.md) is complete.

[:octicons-arrow-right-24: Preparation](preparation.md)

## Stage 3 — Bootstrap the foundation

Install the first Proxmox node, the OPNsense firewall and the **CICD mothership** —
the automation that installs, updates and heals everything else. The bootstrap
scripts chain together; the authoritative commands are in the synced
[INSTALL.md](../generated/install.md).

The [foundation section](foundation/index.md) covers each piece:
[cluster](foundation/cluster.md) · [firewall](foundation/firewall.md) ·
[VM templates](foundation/vm-templates.md) · [CICD](foundation/cicd.md) ·
[identity](foundation/identity.md) · [backup](foundation/backup.md) ·
[security](foundation/security.md).

**Done when:** you can reach the Proxmox UI, the firewall UI and the CICD mothership,
and the foundation health checks pass.

[:octicons-arrow-right-24: Foundation](foundation/index.md)

## Stage 4 — Grow the cluster *(optional)*

Single-node tiers skip this. For SMB/Scale-out, join the remaining nodes and enable
high availability.

**Done when:** every node shows in the cluster and HA-marked services migrate cleanly.

[:octicons-arrow-right-24: Expanding the cluster](foundation/expanding-cluster.md)

## Stage 5 — Add stacks

Install the workloads you chose in stage 1:

| Stack | What you get |
|-------|--------------|
| **[AI stack](ai-stack/index.md)** | Local AI: OpenWebUI, LiteLLM, vLLM/Ollama |
| **[Productivity stack](productivity-stack/index.md)** | Nextcloud, n8n, Karakeep |
| **[Home stack](home-stack/index.md)** | Home Assistant (+ deCONZ for Zigbee) |

Browse [what people run on TAPPaaS](../intro/examples.md) for the full module gallery.

**Done when:** each installed app answers on its URL and shows up in the update scheduler.

## Stage 6 — Cut over the network

Make the TAPPaaS firewall the edge of your network — the step that turns "a lab in the
corner" into *your platform*. Plan a maintenance window; the procedure and rollback are
described in the synced [INSTALL.md](../generated/install.md) (network cut-over section)
and the [firewall page](foundation/firewall.md).

**Done when:** clients get addresses from the TAPPaaS firewall, ingress flows through
it, and the old router is retired or bridged.

## Stage 7 — Operate

Hand over to day-to-day operation: scheduled updates, backup verification, health
monitoring. That's the [Manual](../manual/index.md) — bookmark it.

[:octicons-arrow-right-24: Operate TAPPaaS](../manual/index.md)

---

## Beyond one tenant, beyond one site

- **Multiple environments / tenants** (Scale-out): run separated environments —
  production, family, tenants, experiments — on one platform. Worked example:
  [INSTALL-VARIANT.md (source)](../generated/install-variant.md).
- **No public IP, or no local backup?** A small **satellite** VPS can carry public
  ingress, off-site backup and admin VPN — see the
  [satellite option](hardware-selection.md#the-satellite-the-gap-filler) in the
  hardware guide *(upstream design in progress)*.

## Need help?

- [FAQ](../community/faq.md) for common questions
- [Community support](../community/support.md) for assistance
