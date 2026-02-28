---
title: check-disk-threshold.sh
description: Auto-expand disks when usage exceeds threshold
---

# check-disk-threshold.sh

Checks if a VM's disk usage exceeds a threshold and automatically expands the disk by 50% if needed.

## Usage

```bash
check-disk-threshold.sh <vmname> <threshold>
```

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `vmname` | Name of the VM (must have a JSON config) | `nextcloud` |
| `threshold` | Disk usage percentage threshold (1-99) | `80` |

## Example

```bash
# Check if nextcloud disk usage exceeds 80%
check-disk-threshold.sh nextcloud 80
```

## What it does

1. Connects to the VM via SSH and checks current disk usage with `df`
2. If usage is below threshold, exits with no action
3. If usage exceeds threshold:
   - Retrieves current disk size from Proxmox
   - Calculates new size (50% increase, minimum 5GB)
   - Calls `resize-disk.sh` to perform the resize
   - Logs the resize event to `/home/tappaas/logs/disk-resize.log`

## Cron usage

```bash
# Check disk usage every hour
0 * * * * /home/tappaas/bin/check-disk-threshold.sh nextcloud 80
```

## Requirements

- SSH access to the VM as tappaas user
- SSH access to the Proxmox node as root
- VM must be running and reachable

## See Also

- [resize-disk.sh](resize-disk.md) - Manual disk resize
