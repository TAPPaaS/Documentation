---
title: TAPPaaS Scripts
description: Utility scripts for TAPPaaS-CICD operations
---

# TAPPaaS-CICD Scripts

Utility scripts for TAPPaaS-CICD operations. These scripts are installed to `/home/tappaas/bin/` during setup.

## Module Lifecycle Scripts

- **[install-module.sh](install-module.md)** - Install a module with dependency validation
- **[update-module.sh](update-module.md)** - Update a module with dependency-aware service wiring
- **[delete-module.sh](delete-module.md)** - Delete a module with dependency-aware teardown

## Repository Management

- **[repository.sh](repository.md)** - Manage module repositories (add/remove/modify/list)

## VM Management

- **[install-vm.sh](install-vm.md)** - VM creation library (sourced by install.sh)
- **[update-os.sh](update-os.md)** - OS-specific update (NixOS/Debian)
- **[update-HA.sh](update-ha.md)** - Manage HA and replication for modules
- **[snapshot-vm.sh](snapshot-vm.md)** - VM snapshot management (create/list/cleanup/restore)
- **[migrate-vm.sh](migrate-vm.md)** - Migrate VMs between nodes (live or offline)
- **[migrate-node.sh](migrate-node.md)** - Evacuate or return all VMs on a node

## Cluster Inspection

- **[inspect-cluster.sh](inspect-cluster.md)** - Compare running VMs against module configurations
- **[inspect-vm.sh](inspect-vm.md)** - 3-column config/git/actual VM comparison

## Disk Management

- **[check-disk-threshold.sh](check-disk-threshold.md)** - Auto-expand disks when usage exceeds threshold
- **[resize-disk.sh](resize-disk.md)** - Resize VM disk in Proxmox and filesystem

## Configuration Scripts

- **[create-configuration.sh](create-configuration.md)** - Generate system configuration.json
- **[copy-update-json.sh](copy-update-json.md)** - Copy and modify module JSON configs
- **[common-install-routines.sh](common-install-routines.md)** - Shared library for install scripts

## System Scripts

- **[update-cron.sh](update-cron.md)** - Set up hourly update cron job
- **[test-config.sh](test-config.md)** - Validate installation
- **[setup-caddy.sh](setup-caddy.md)** - Install Caddy reverse proxy on firewall

## Installation

These scripts are automatically installed by `install2.sh`:
```bash
cp scripts/*.sh /home/tappaas/bin/
chmod +x /home/tappaas/bin/*.sh
```

Or symlinked via NixOS configuration.
