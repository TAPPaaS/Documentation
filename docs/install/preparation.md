---
title: Preparation
description: >
  Everything to have ready before running the TAPPaaS install — network, domain,
  credentials, branch and naming — as one concise checklist.
---

# Preparation

Have these ready **before** you run the [install](../generated/install.md). Hardware
itself is the previous step — [Hardware Selection](hardware-selection.md).

## 1. Network

- [ ] An **existing network** (your home/office LAN) with working **DHCP and
  internet** — the install runs on it, and after cut-over it feeds the firewall's
  WAN via DHCP.
- [ ] A **free IP** on that network for the first node (the Proxmox installer does
  not use DHCP), plus its real gateway and DNS server addresses.
- [ ] Each node wired with **two NICs**: one towards the upstream router (WAN), one
  towards your downstream switch (LAN). Clusters need a switch between the nodes —
  **unmanaged works out of the box**; a **managed switch must have its inter-node
  ports configured as VLAN trunks before you add nodes**.
- [ ] Drive the install from a client that is **not** on `10.0.0.0/24` (that subnet
  becomes the management network during cut-over).

## 2. Domain and DNS

- [ ] A **registered domain** with **API-accessible DNS**. Not a hard requirement —
  you can even configure a domain you haven't registered yet — but needed for
  automatic public TLS certificates.
- [ ] An **API token** for your DNS provider (used for ACME DNS-01; ~120 providers
  supported — Cloudflare, deSEC, Hetzner, OVH, Route 53, …). For Cloudflare: a
  custom token with `Zone → Zone → Read` and `Zone → DNS → Edit`, restricted to
  your domain. You'll enter it after bootstrap, not before.

## 3. Credentials and contact

- [ ] A **strong password** for Proxmox and the firewall — you'll be asked for it
  several times during install.
- [ ] A **working email address you actually monitor** — Proxmox sends system and
  health notifications there, and TAPPaaS reuses it as the admin email.

## 4. Branch selection

The bootstrap command takes a branch (`BRANCH="..."` in the
[install guide](../generated/install.md)) — decide it now:

| Branch | What it is | Who should install it |
|--------|------------|-----------------------|
| **`stable`** | The released, supported version of TAPPaaS | Everyone running a real system |
| **`main`** | Ongoing development — moves fast, may break | Contributors, and evaluators who want the newest work |

**If in doubt, choose `stable`.** `stable` only moves when a release is cut and
tested; `main` moves with every merged change. A system tracks its branch through
the automated updates — the choice you make here is the risk profile you keep.

??? note "Transitional: migrating from ADR007 to 2.0"
    The next major release (**2.0** — the taxonomy and manager/controller platform)
    is being finished on the **`ADR007`** branch and will be promoted to `stable`
    per the [roadmap](../roadmap/index.md). Until that promotion:

    - **New 2.0 installs** use `BRANCH="ADR007"`. This site documents 2.0 — the
      synced pages here track `ADR007`.
    - **Existing 1.x/main systems** convert with the
      [ADR-007 migration runbook](https://codeberg.org/TAPPaaS/TAPPaaS/src/branch/main/docs/design/ADR-007-migration-runbook.md)
      maintained in the source repo.
    - **At promotion**, `stable` simply becomes 2.0 — and this note gets deleted.

## 5. Solution naming

Two names define your installation — pick them now:

- [ ] **Organisation name** (`--name`): lowercase, ≤15 characters. This **one name**
  becomes the Proxmox cluster, the site, the default environment and your
  organisation in the identity provider.
- [ ] **Public domain** (`--domain`): services are published as
  `<service>.yourdomain.com` by the reverse proxy (the domain from point 2).

**Done when** every box above is ticked — then proceed to
[Install Foundation](../generated/install.md).
