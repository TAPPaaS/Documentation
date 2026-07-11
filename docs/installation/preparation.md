---
title: Preparation
description: >
  Everything to have ready before running the TAPPaaS install — network, domain,
  credentials, branch — as one concise checklist.
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

## 4. Decisions to make now

- [ ] **[Branch selection](branch-selection.md)** — which branch the system will
  install from and track.
- [ ] **Organisation name** (`--name`): lowercase, ≤15 characters. This one name
  becomes the Proxmox cluster, the site, the default environment and your
  organisation in the identity provider.
- [ ] **Your public domain** (`--domain`), used by the reverse proxy as
  `<service>.yourdomain.com`.

**Done when** every box above is ticked — then proceed to
[Install Foundation](../generated/install.md).
