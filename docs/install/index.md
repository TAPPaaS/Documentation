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

Each stage is a menu item on the left — work through them in order.

| # | Stage | You'll need | Done when |
|---|-------|-------------|-----------|
| 1 | [Hardware Selection](#stage-1-hardware-selection) | An honest look at your needs | Hardware ordered/on the bench, sized by tier + options |
| 2 | [Preparation](#stage-2-preparation) | Network, domain, credentials, branch choice | The [preparation checklist](preparation.md) is all ticked |
| 3 | [Install Foundation](#stage-3-install-foundation) | Stages 1 + 2 complete | Foundation installed (all nodes); network cut over; you can log in everywhere |
| 4 | [Add Environment](#stage-4-add-environment-optional) *(optional)* | A running foundation | Each tenant/purpose has its own separated environment |
| 5 | [Add Satellite](#stage-5-add-satellite-optional) *(optional)* | A VPS, if you planned one | The satellite carries its roles (ingress / backup / VPN) |
| 6 | [Add Stacks](#stage-6-add-stacks) | A running foundation | The apps you chose are installed and reachable |
| 7 | [Operate](#stage-7-operate) | — | Updates, backup and health checks running on schedule |

---

## Stage 1 — Hardware Selection

Pick a **size tier** (Evaluation / Home / SMB / Scale-out), then toggle three
**capability options** — local AI, local backup, local public IP — independently.
The [hardware selection guide](hardware-selection.md) walks the decision in four steps
and gives per-tier sizing tables.

**Done when:** you know your tier, your options, and the machine(s) are in hand.

[:octicons-arrow-right-24: Hardware Selection](hardware-selection.md)

## Stage 2 — Preparation

One concise checklist: network facts, domain + DNS API token, credentials, admin
email — and the **[branch selection](preparation.md#4-branch-selection)** your system will track.

**Done when:** every box in [Preparation](preparation.md) is ticked.

[:octicons-arrow-right-24: Preparation](preparation.md)

## Stage 3 — Install Foundation

Four steps, mostly automated — first Proxmox node plus one command chain that
brings up the OPNsense firewall, the **network cut-over** (additive: the firewall
becomes your gateway without dropping your session or moving cables) and the CICD
mothership; additional nodes joining over the network, fully unattended; **DNS/TLS
setup** (wildcard certificates via your DNS provider's API) with **switch
management** where a managed switch carries the VLAN trunks; and the remaining
foundation modules (backup, identity, logging) with your organisation bootstrapped
in the identity provider.

The authoritative, always-current procedure is
**[Install Foundation](../generated/install.md)** — follow its steps top to bottom.

**Done when:** the install prints its "🎉 your TAPPaaS foundation is installed"
summary, and you can reach the Proxmox UI, the firewall UI and the CICD mothership.

[:octicons-arrow-right-24: Install Foundation](../generated/install.md)

## Stage 4 — Add Environment *(optional)*

Run more than one world on the same platform: production next to family, tenants
next to experiments — separated environments with network boundaries between them.

**Done when:** each environment exists with its own zones and domain.

[:octicons-arrow-right-24: Add Environment](../generated/install-environment.md)

## Stage 5 — Add Satellite *(optional)*

If you planned a **satellite** in stage 1 (public ingress without a public IP,
off-site backup, admin VPN — see the
[hardware guide](hardware-selection.md#the-satellite-the-gap-filler)), enrol the
VPS now.

**Done when:** the satellite carries its roles.

[:octicons-arrow-right-24: Add Satellite](../generated/satellite-install.md)

## Stage 6 — Add Stacks

Install the workloads you chose in stage 1. First-party modules install with
`install-module.sh <module>` from the module's directory; community module stores
register once with `repository.sh add <repo> --branch <branch>`, after which their
modules install the same way.

| Stack | What you get |
|-------|--------------|
| **[AI stack](ai-stack/index.md)** | Local AI: vLLM serving, LiteLLM gateway, OpenWebUI |
| **[Productivity stack](productivity-stack/index.md)** | Nextcloud (n8n, Karakeep planned) |
| **[Home stack](home-stack/index.md)** | Home Assistant (Jellyfin, Immich planned) |
| **[IoT stack](iot-stack/index.md)** | deCONZ Zigbee gateway |

Browse [what people run on TAPPaaS](../why/examples.md) for the full module gallery.

**Done when:** each installed app answers on its URL and is known to the
[Module Manager](../generated/managers/module-manager.md).

## Stage 7 — Operate

Hand over to day-to-day operation: the managers keep updating, backing up and
health-checking the platform. That's [Operate](../operate/index.md) — bookmark it.

[:octicons-arrow-right-24: Operate TAPPaaS](../operate/index.md)

---

## Need help?

- [FAQ](../community/faq.md) for common questions
- [Community support](../community/support.md) for assistance
