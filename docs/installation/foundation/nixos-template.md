---
title: NixOS Template
description: Create the NixOS VM template for TAPPaaS services
---

# NixOS VM Template

This guide covers creating a NixOS virtual machine template on Proxmox that serves as the base for all TAPPaaS service VMs.

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

### Run Installation Script

From the Proxmox console as root:

```bash
REPO="https://raw.githubusercontent.com/TAPPaaS/TAPPaaS/"
BRANCH="main"
curl -fsSL ${REPO}${BRANCH}/src/foundation/20-tappaas-nixos/install.sh | bash
```

This creates VM 8080 for the template installation.

### Install NixOS

Access the VM console and follow the NixOS installer:

1. **Username**: `tappaas`
2. **Password**: Use a strong password
3. **Desktop Environment**: None (server installation)
4. **Proprietary Software**: Allow if needed
5. **Disk Configuration**: Erase disk, no encryption, no swap

!!! note "Installation Timing"
    The installation may appear to stall at times. This is normal - wait for it to complete.

### Post-Installation

When installation completes:

1. **Do not restart immediately**
2. Shut down the VM properly
3. Detach the installation media in Proxmox

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
curl -fsSL ${REPO}${BRANCH}/src/foundation/20-tappaas-nixos/configuration.nix \
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

### Via Proxmox GUI

1. Right-click the VM in Proxmox
2. Select **Convert to Template**

### Via CLI

```bash
qm template 8080
```

## Template Usage

When creating new VMs from this template:

```bash
# Clone template to new VM
qm clone 8080 <new-vmid> --name <vm-name> --full

# Start the new VM
qm start <new-vmid>
```

The cloned VM will:

- Generate new SSH host keys
- Get a new machine ID
- Be ready for service-specific configuration

## Verification

Verify the template is ready:

```bash
# List templates
qm list | grep template

# Check template configuration
qm config 8080
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
