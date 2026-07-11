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

## The seven stages

| # | Stage | You'll need | Done when |
|---|-------|-------------|-----------|
| 1 | [Choose hardware](#stage-1-choose-hardware) | An honest look at your needs | Hardware ordered/on the bench, sized by tier + options |
| 2 | [Prepare](#stage-2-prepare) | Network, domain, credentials, branch choice | The [preparation checklist](preparation.md) is all ticked |
| 3 | [Bootstrap the foundation](#stage-3-bootstrap-the-foundation) | Stages 1 + 2 complete | Foundation installed; network cut over; you can log in everywhere |
| 4 | [Grow the cluster](#stage-4-grow-the-cluster-optional) *(optional)* | Additional nodes | All nodes joined; HA where intended |
| 5 | [Add environments](#stage-5-add-environments) *(optional)* | A running foundation | Each tenant/purpose has its own separated environment |
| 6 | [Add stacks](#stage-6-add-stacks) | A running foundation | The apps you chose are installed and reachable |
| 7 | [Operate](#stage-7-operate) | — | Updates, backup and health checks running on schedule |

---

## Stage 1 — Choose hardware

Pick a **size tier** (Evaluation / Home / SMB / Scale-out), then toggle three
**capability options** — local AI, local backup, local public IP — independently.
The [hardware selection guide](hardware-selection.md) walks the decision in four steps
and gives per-tier sizing tables.

**Done when:** you know your tier, your options, and the machine(s) are in hand.

[:octicons-arrow-right-24: Hardware Selection](hardware-selection.md)

## Stage 2 — Prepare

One concise checklist: network facts, domain + DNS API token, credentials, admin
email — and the **[branch selection](branch-selection.md)** your system will track.

**Done when:** every box in [Preparation](preparation.md) is ticked.

[:octicons-arrow-right-24: Preparation](preparation.md)

## Stage 3 — Bootstrap the foundation

One command chain does the heavy lifting — first Proxmox node, the OPNsense
firewall, the **network cut-over** (additive: the firewall becomes your gateway
without dropping your session or moving cables), the CICD mothership, **DNS/TLS
setup** (wildcard certificates via your DNS provider's API), **switch management**
where a managed switch carries the VLAN trunks, and then the remaining foundation
modules (backup, identity, logging) with your organisation bootstrapped in the
identity provider.

The authoritative, always-current procedure is
**[Install Foundation](../generated/install.md)** — follow it top to bottom.

**Done when:** the install prints its "🎉 your TAPPaaS foundation is installed"
summary, and you can reach the Proxmox UI, the firewall UI and the CICD mothership.

[:octicons-arrow-right-24: Install Foundation](../generated/install.md)

## Stage 4 — Grow the cluster *(optional)*

Single-node tiers skip this. Additional nodes install over the network, fully
unattended — one command per node (`site-manager node add tappaasN --pxe`), covered
in [Install Foundation](../generated/install.md).

**Done when:** every node shows in the cluster and HA-marked services migrate cleanly.

## Stage 5 — Add environments *(optional)*

Run more than one world on the same platform: production next to family, tenants
next to experiments — separated environments with network boundaries between them.
This is also where a **[satellite](../generated/satellite.md)** joins the site if
you planned one (public ingress, off-site backup, admin VPN —
[Satellite Install](../generated/satellite-install.md)).

**Done when:** each environment exists with its own zones/domain, and the satellite
(if any) carries its roles.

[:octicons-arrow-right-24: Add an Environment](../generated/install-environment.md)

## Stage 6 — Add stacks

Install the workloads you chose in stage 1:

| Stack | What you get |
|-------|--------------|
| **[AI stack](ai-stack/index.md)** | Local AI: OpenWebUI, LiteLLM, vLLM/Ollama |
| **[Productivity stack](productivity-stack/index.md)** | Nextcloud, n8n, Karakeep |
| **[Home stack](home-stack/index.md)** | Home Assistant (+ deCONZ for Zigbee) |

Browse [what people run on TAPPaaS](../intro/examples.md) for the full module gallery.

**Done when:** each installed app answers on its URL and is known to the
[Module Manager](../generated/managers/module-manager.md).

## Stage 7 — Operate

Hand over to day-to-day operation: the managers keep updating, backing up and
health-checking the platform. That's [Operate](../manual/index.md) — bookmark it.

[:octicons-arrow-right-24: Operate TAPPaaS](../manual/index.md)

---

## Need help?

- [FAQ](../community/faq.md) for common questions
- [Community support](../community/support.md) for assistance
