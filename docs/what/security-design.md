---
title: Security
description: TAPPaaS security design — secrets, access, segmentation, ingress, monitoring, resilience
---

# Security design

A high security standard is essential for TAPPaaS to compete with cloud providers. TAPPaaS
addresses security across seven areas:

- Secrets and password management
- Root and management access to virtual machines
- Network segmentation
- Inbound internet access security
- Supply chain security
- Monitoring of the TAPPaaS solution
- Resiliency in case of breach

## Secrets and password management

A trusted, self-hostable password manager is essential; the choice is **Bitwarden/VaultWarden** —
a Rust reimplementation of the Bitwarden server, audited, and the only true open-source
self-hostable option. The same vault also holds integration secrets, which simplifies setup.

The server runs behind the TAPPaaS reverse proxy, so it is reachable everywhere; secrets are stored
encrypted, so even a server compromise does not expose the passwords.

VaultWarden complements the **Authentik** SSO provided by the
[`identity`](../generated/foundation/identity.md) foundation module — together they form the
complete TAPPaaS identity and credential strategy:

- **Authentik** ([`identity`](../generated/foundation/identity.md)) manages single sign-on for every
  application that supports it (OIDC or forward-auth).
- **VaultWarden** ([`vaultwarden`](../generated/modules/vaultwarden.md)) securely stores credentials
  for legacy systems and external services that cannot yet use SSO.

## Root and management access to VMs

- Management is performed either from the **root** account of the TAPPaaS node itself, or from the
  **`tappaas`** account on the [`tappaas-cicd`](../generated/foundation/tappaas-cicd.md) VM.
- Every VM has a `tappaas` user with `sudo` rights; the cloud-init `tappaas` user has no password
  login, and root has no password login.
- An SSH authorized-keys allow-list permits login only from `tappaas@tappaas-cicd` and from root on
  the TAPPaaS node.

Public administrative access with **no public IP** is delivered by the satellite `admin-vpn` role —
see [`satellite`](../generated/foundation/satellite.md).

## Network segmentation

TAPPaaS segments the network into security **zones** so that a breach of one service or VM does not
immediately reach the others. The zone model — trust tiers, the isolation invariant, and the VLAN
bands — is the [`network`](../generated/design/network.md) module's design, with the operational
definitions the single source of truth in [Network Zones](../generated/zones.md). VLAN tags map to
zones by band — **Service 2xx, IoT 4xx, DMZ 6xx** (management is untagged):

![TAPPaaS network switching](../assets/network-switching.svg)

## Inbound internet access security

External access is controlled by three components:

- A **reverse proxy** with access control — Caddy terminating TLS on the OPNsense firewall (the
  [`network`](../generated/design/network.md) `network:proxy` capability). For sites without a public
  IP, the [`satellite`](../generated/foundation/satellite.md) blind reverse-proxy publishes services
  over a WireGuard tunnel (ADR-010).
- A **blocking firewall** filtering DNS and IPs against public block lists (Unbound DNSBL).
- Participation in the **CrowdSec** network (planned).

## Supply chain security

- Use software only from major open-source organisations with a good security history.
- Monitor CVE publications across all TAPPaaS packages.
- Keep software patched weekly (automated).

## Monitoring

Observability is delivered by the **Health** lens — the
[`logging`](../generated/foundation/logging.md) foundation module (Loki / Grafana / Promtail) with
the [health-manager](../generated/managers/health-manager.md) aggregating module and VM health.

## Resiliency in case of breach

Two design principles:

- **Network segmentation** — a breach of one service or VM does not immediately reach the others;
  in particular the root/management accounts live in a zone that cannot be reached from the others.
- **Extensive backups**, including off-site copies with a completely different security setup — see
  the [backup](../generated/design/backup.md) design.
