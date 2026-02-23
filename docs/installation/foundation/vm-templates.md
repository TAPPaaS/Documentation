---
title: VM Templates
description: Create VM templates for TAPPaaS services
---

# VM Templates

This guide covers creating a NixOS virtual machine template on Proxmox that serves as the base for many TAPPaaS service VMs.

## Overview

The setup involves three phases:

1. Create a minimal NixOS installation with cloud-init
2. Configure the system for TAPPaaS
3. Convert to a reusable template

## Prerequisites

- [ ] Proxmox cluster operational
- [ ] [Firewall](firewall.md) configured
- [ ] Network connectivity verified

## Create Base VM

### Run NixOS Installation

From the Proxmox console as root:

```bash
BRANCH="main"
REPO="https://raw.githubusercontent.com/TAPPaaS/TAPPaaS/"
curl -fsSL  ${REPO}${BRANCH}/src/foundation/20-tappaas-nixos/tappaas-nixos.json >~/tappaas/tappaas-nixos.json
~/tappaas/Create-TAPPaaS-VM.sh tappaas-nixos
```

This creates VM 8080 for the template installation.

Access the VM console and follow the NixOS installer:

1. **Username**: `tappaas`
2. **Password**: Use a strong password
3. **Desktop Environment**: None (server installation)
4. **Unfree Software**: Allow
5. **Disk Configuration**: Erase disk, no encryption, no swap

!!! note "Installation Timing"
    The installation may appear to stall at times.
    it may appear to be stalled at 46% for minutes - be patient!
    toggle log to see detailed progress


When installation completes:

1. **Do not restart immediately**
2. keep 'Restart now' UNchecked
3. select Done at lower right bottom to finish installation without reboot
4. Shut down the VM 8080 properly form the proxmox GUI
5. Detach the installation media in Proxmox: In PVE console, select Hardware -> CD/DVD Drive (IDE3)
  - Edit --> select 'Do not use any media' to detach the iso


## System Configuration

### Boot and Configure

Start the VM and login as `tappaas`, then switch to root:

```bash
sudo -i
```

### Download TAPPaaS Configuration

```bash
REPO="https://raw.githubusercontent.com/TAPPaaS/TAPPaaS/"
BRANCH="main"
curl -fsSL ${REPO}${BRANCH}/src/foundation/templates/tappaas-nixos.nix \
  -o /etc/nixos/configuration.nix
```

### Rebuild System

```bash
nixos-rebuild switch
reboot
```

## Pre-Template Cleanup

Before converting to a template, clean the system to minimize size and ensure unique identifiers on clones.

### Run Cleanup Commands

```bash
# Garbage collect Nix store
nix-store --gc

# Clear journals
journalctl --vacuum-time=1s

# Remove logs
rm -rf /var/log/*

# Reset machine ID
rm /etc/machine-id
touch /etc/machine-id

# Remove SSH host keys (regenerated on first boot)
rm /etc/ssh/ssh_host_*

# Clear caches
rm -rf /root/.cache
rm -rf /home/*/.cache

# Clear bash history
rm -rf /root/.bash_history
rm -rf /home/*/.bash_history

# Sync and shutdown
sync
poweroff
```

## Convert to Template

***Via Proxmox GUI***

1. Right-click the VM in Proxmox
2. Select **Convert to Template**

***Via CLI***

```bash
qm template 8080
```

## Troubleshooting

### VM Won't Boot After Configuration

- Check NixOS configuration syntax: `nixos-rebuild dry-build`
- Review boot logs in Proxmox console

### Template Clone Fails

- Ensure VM is fully powered off
- Verify sufficient storage space
- Check Proxmox storage permissions

## Next Steps

With the template ready, proceed to [CICD Mothership](cicd.md) deployment.
