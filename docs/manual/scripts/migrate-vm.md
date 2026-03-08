---
title: migrate-vm.sh
description: Migrate VMs between Proxmox cluster nodes
---

# migrate-vm.sh

Migrates VMs between Proxmox cluster nodes. Attempts live migration first; if it fails, automatically falls back to offline migration (shutdown → migrate → start).

## Usage

```bash
migrate-vm.sh <module-name>
migrate-vm.sh --node <node-name>
```

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `module-name` | Name of the module to migrate | `identity` |
| `--node <name>` | Target node — migrate all its VMs back | `--node tappaas1` |
| `--offline` | Skip live migration attempt | |

## Modes

1. **Single module** (`migrate-vm.sh identity`):
    - If the VM is on its primary node (`node`), migrates to the HA node (`HANode`)
    - If the VM is on its HA node, migrates back to the primary node
    - If the VM is on any other node, migrates to the primary node

2. **Node mode** (`migrate-vm.sh --node tappaas1`):
    - Finds all modules whose configured `node` is `tappaas1`
    - For each VM not currently on that node, migrates it there
    - Useful for returning VMs after maintenance or failover

## Examples

```bash
# Migrate identity to its HA node
migrate-vm.sh identity

# Force offline migration (no live attempt)
migrate-vm.sh --offline identity

# Return all VMs to tappaas1 after maintenance
migrate-vm.sh --node tappaas1
```

## What it does

1. Reads module config to determine VMID, primary node, and HA node
2. Queries the cluster to find where the VM is currently running
3. Saves HA state (resource + affinity rule) before migration
4. Attempts live migration (unless `--offline`)
5. Falls back to offline migration if live fails
6. Restores HA resource and affinity rule after migration
7. Replication direction is automatically updated by Proxmox

## Notes

- Live migration may fail on clusters with different CPU architectures (e.g., Intel + AMD). The script handles this gracefully by falling back to offline migration
- HA affinity rules are saved and restored automatically
- The `--node` mode shows a summary of migrated/skipped/failed VMs

## See Also

- [migrate-node.sh](migrate-node.md) - Evacuate or return all VMs on a node
- [update-HA.sh](update-ha.md) - Manage HA and replication for modules
