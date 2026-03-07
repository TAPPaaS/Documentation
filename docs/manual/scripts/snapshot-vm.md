---
title: snapshot-vm.sh
description: Manage VM snapshots on the Proxmox cluster
---

# snapshot-vm.sh

Manages VM snapshots on the Proxmox cluster for an installed module.

## Usage

```bash
snapshot-vm.sh <module-name> [--list | --cleanup <N> | --restore <N>]
```

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `module-name` | Name of the module (must have config in ~/config) | `vaultwarden` |
| `--list` | List all snapshots on the VM | |
| `--cleanup <N>` | Delete all snapshots except the last N | `--cleanup 3` |
| `--restore <N>` | Restore snapshot N steps back (1 = most recent) | `--restore 1` |

## Examples

```bash
# Create a new snapshot
snapshot-vm.sh vaultwarden

# List all snapshots
snapshot-vm.sh vaultwarden --list

# Keep only the last 3 snapshots
snapshot-vm.sh vaultwarden --cleanup 3

# Restore to the most recent snapshot
snapshot-vm.sh vaultwarden --restore 1
```

## What it does

1. Validates the module has a config in `~/config` with a `vmid`
2. Verifies the VM exists on the configured Proxmox node
3. Performs the requested snapshot operation via `qm snapshot`/`qm rollback`/`qm delsnapshot`

## Notes

- Snapshot names follow the format `tappaas-YYYYMMDD-HHMMSS`
- Restore stops the VM, rolls back, then starts it again
- Cleanup deletes oldest snapshots first

## See Also

- [install-module.sh](install-module.md) - Install a module
- [update-module.sh](update-module.md) - Update a module
