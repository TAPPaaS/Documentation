---
title: FAQ
description: Frequently asked questions about TAPPaaS
---

# Frequently Asked Questions

Find answers to common questions about TAPPaaS.

---

## General

### What is TAPPaaS?

TAPPaaS (Trusted Automated Private Platform as a Service) is an open-source platform designed to simplify deploying and managing self-hosted applications on Proxmox virtualization. It provides enterprise-class capabilities with automated setup, security, backup, and identity management.

### Is TAPPaaS free to use?

Yes! TAPPaaS is open source software licensed under the [Mozilla Public License 2.0](../about/license.md). You can use, modify, and distribute it freely.

### How is TAPPaaS different from other PaaS solutions?

TAPPaaS differentiates itself by:

- **Open Source**: Full transparency and community-driven development
- **Self-Hosted**: Run on your own hardware with full control and privacy
- **Integrated**: Security, backup, identity management built-in
- **Automated**: Reduces weeks of manual setup to hours

See our [Architecture Overview](../docs/index.md) for more details.

### Who is TAPPaaS for?

TAPPaaS serves:

- **Families and Communities** - Data privacy and independence from big tech
- **Small-to-Medium Businesses** - Reliable infrastructure without a dedicated IT team
- **Organizations** - Government, NGOs, and critical infrastructure needing local resilience

---

## Installation

### What are the system requirements?

**Minimum (single node):**

- x86_64 server or PC
- 4 CPU cores
- 16GB RAM
- 2 disks: 256GB boot + 500GB tanka1 (data)
- Network interface

**Recommended (single node):**

- 8+ CPU cores
- 32GB+ RAM
- 1x 512GB SSD (boot)
- 2x 2TB mirrored (tanka - data with redundancy)
- 1x 12TB (tankb - backup)
- Dedicated network switch

See the [Hardware Selection Guide](../installation/hardware-selection.md) for details.

### Can I run TAPPaaS on my existing hardware?

Yes! TAPPaaS runs on standard x86_64 hardware. You can repurpose existing servers, use mini PCs, or purchase new hardware. See our [Installation Guide](../installation/index.md).

### How do I upgrade TAPPaaS?

TAPPaaS modules are updated through the CI/CD system. Updates are typically automated on a weekly basis with security patches applied automatically.

---

## Architecture

### What virtualization does TAPPaaS use?

TAPPaaS is built on **Proxmox VE**, an open-source virtualization platform. Each TAPPaaS module runs in its own virtual machine for isolation and security.

### What about high availability?

TAPPaaS supports:

- **Disk redundancy**: ZFS mirroring and RAIDz configurations
- **Node clustering**: 3+ node Proxmox clusters with failover
- **Backup**: Automated backups with Proxmox Backup Server

See the [Backup Design](../docs/solution-design/backup.md) for details.

### How does networking work?

TAPPaaS uses VLAN segmentation to isolate different parts of the platform:

- Management network
- DMZ for external access
- Service networks
- IoT networks

See the [Network Design](../docs/solution-design/network.md) for details.

---

## Operations

### How do I view logs?

Logs are available through the Proxmox web interface and within each module's VM. Centralized logging can be configured for easier management.

### How do I backup my data?

TAPPaaS follows the 3-2-1 backup principle:

- **3 copies** of data
- **2 different formats**
- **1 remote location**

Proxmox Backup Server handles automated daily backups. See [Backup Design](../docs/solution-design/backup.md).

### How do I access services remotely?

TAPPaaS uses a reverse proxy in the DMZ for secure external access. Services are exposed through the proxy with authentication via the Single Sign-On system.

---

## Community

### How can I contribute?

We welcome contributions! See our [Contributing Guide](contributing.md) for:

- Code contributions
- Documentation improvements
- Bug reports
- Feature requests

### Where can I get help?

- **Documentation**: You're already here!
- **GitHub Discussions**: [Ask questions](https://github.com/TAPPaaS/TAPPaaS/discussions)
- **GitHub Issues**: [Report bugs](https://github.com/TAPPaaS/TAPPaaS/issues)

See [Support](support.md) for more options.

---

## Still Have Questions?

If your question isn't answered here:

1. Search the [documentation](../index.md)
2. Check [GitHub Discussions](https://github.com/TAPPaaS/TAPPaaS/discussions)
3. Ask a new question in the community

[:octicons-comment-discussion-24: Ask the Community](https://github.com/TAPPaaS/TAPPaaS/discussions/new?category=q-a){ .md-button .md-button--primary }
