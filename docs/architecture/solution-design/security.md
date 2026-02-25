---
title: Security
description: TAPPaaS security architecture
---

# Security Design

A high security standard for the TAPPaaS solution is essential for TAPPaaS to compete with cloud providers.

There are many aspects to security. What we have considered in TAPPaaS:

- Secrets and password management
- Root and Management access to Virtual machines
- Network segmentation
- Inbound Internet access security
- Supply chain security
- Monitoring of the TAPPaaS solution
- Resiliency in case of breach

---

## Secrets and Password Management

Having a well established password manager that can be trusted is essential, and the choice is **BitWarden/VaultWarden**. This is the only true open source password manager that can be self-hosted. VaultWarden is a rewrite of the server part in Rust. It is audited.

For secrets used in integration we chose to also use VaultWarden. This simplifies setup.

The server part runs as a service under Pangolin reverse proxy so available everywhere. Secrets are stored encrypted so even a hack of the server is not going to compromise the passwords. For that reason we host the vault in the DMZ to assist with uptime, and the possibility to host in a VPS.

---

## Root and Management Access to VMs

General setup is:

- Every management is done either from the root account of the TAPPaaS node itself
- Or it is done from the tappaas account on the tappaas-cicd VM
- Every VM has a "tappaas" user with "sudo" rights
- The tappaas user defined in cloud-init will have no password login access
- Root will not have password login
- There will be an SSH Authorized list configured to allow login from the tappaas@tappaas-cicd user and from root at the TAPPaaS node

---

## Network Segmentation

See [Network Design](network.md) for details on network segmentation.

---

## Inbound Internet Access Security

There are 3 main components in the external access security setup:

1. **Reverse Proxy** - Use a reverse proxy with access control, served in a separate DMZ network segment
2. **Blocking Firewall** - Use a blocking firewall that filters DNS and IP based on public block lists
3. **CrowdSec** - Participate in the CrowdSec network for collaborative threat intelligence

---

## Supply Chain Security

- Only use software from major open source organizations with a good history on security
- Monitor CVE publications on all TAPPaaS packages
- Keep software patched on a weekly basis (automated)

---

## Monitoring

*To be designed*

---

## Resiliency

The two main design principles for resiliency in TAPPaaS:

### Network Segmentation

Segmentation of TAPPaaS network ensures breach of one service or one VM does not immediately lead to breach of other VMs. Importantly, the root access accounts for management reside on a segment that cannot be accessed from other segments.

### Extensive Backups

Including backups to external sites that have completely different security setups. See [Backup Design](backup.md) for details.
