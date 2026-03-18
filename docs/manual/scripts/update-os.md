---
title: update-os.sh
description: Update a VM's operating system (NixOS or Debian/Ubuntu)
---

# update-os.sh

Updates a VM's operating system based on its type (NixOS or Debian/Ubuntu).

## Usage

```bash
update-os.sh <vmname> <vmid> <node>
```

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `vmname` | Name of the VM | `nextcloud` |
| `vmid` | Proxmox VM ID | `610` |
| `node` | Proxmox node name | `tappaas1` |

## Example

```bash
update-os.sh myvm 610 tappaas1
```

## What it does

1. Waits for VM to get an IP address (via guest agent or DHCP leases)
2. Updates SSH known_hosts
3. Detects OS type (NixOS or Debian/Ubuntu)
4. For **NixOS**:
   - Runs `nixos-rebuild` using `./<vmname>.nix` in current directory
   - Reboots VM to apply configuration
   - Waits for VM to come back up
5. For **Debian/Ubuntu**:
   - Waits for cloud-init to complete
   - Runs `apt-get update && apt-get upgrade`
   - Installs QEMU guest agent
6. Fixes DHCP hostname registration via NetworkManager

## Requirements

- For NixOS VMs: `./<vmname>.nix` must exist in current directory
- SSH access to VM as tappaas user
- QEMU guest agent installed on VM

## See Also

- [install-module.sh](install-module.md) - Install a module
