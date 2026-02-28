---
title: resize-disk.sh
description: Resize VM disk in Proxmox and filesystem
---

# resize-disk.sh

Resizes the disk of a VM both in Proxmox and inside the VM filesystem.

## Usage

```bash
resize-disk.sh <vmname> <new-size>
```

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `vmname` | Name of the VM (must have a JSON config) | `nextcloud` |
| `new-size` | New disk size (G, M, T, K suffix) | `50G` |

## Example

```bash
# Resize nextcloud disk to 50GB
resize-disk.sh nextcloud 50G
```

## What it does

1. Validates that the new size is larger than the current size (shrinking not supported)
2. Resizes the disk in Proxmox using `qm resize`
3. Connects to the VM via SSH and resizes the partition and filesystem:
   - **NixOS**: Uses `sfdisk` to grow the partition, then `resize2fs` for ext4
   - **Debian/Ubuntu**: Uses `growpart` to grow the partition, then `resize2fs` for ext4
4. Verifies the new filesystem size
5. Updates the `diskSize` field in the VM's JSON configuration

## Supported configurations

| OS | Filesystem | Status |
|----|------------|--------|
| NixOS | ext4 | Fully supported |
| Debian/Ubuntu | ext4 | Fully supported |
| Other | Any | Proxmox disk resized, manual filesystem resize required |

## Requirements

- SSH access to the VM as tappaas user with sudo
- SSH access to the Proxmox node as root
- VM must be running and reachable

## See Also

- [check-disk-threshold.sh](check-disk-threshold.md) - Automatic disk expansion
