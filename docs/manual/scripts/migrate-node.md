---
title: migrate-node.sh
description: Evacuate or return all VMs on a Proxmox node
---

# migrate-node.sh

Evacuates all VMs from a Proxmox node (for maintenance) or returns them afterwards. Uses `migrate-vm.sh` for each individual migration.

## Usage

```bash
migrate-node.sh <node-name>
migrate-node.sh --return <node-name>
migrate-node.sh --list <node-name>
```

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `node-name` | Proxmox node to evacuate | `tappaas1` |
| `--return <name>` | Return VMs that belong on this node | `--return tappaas1` |
| `--list <name>` | Dry run — show what would happen | `--list tappaas1` |
| `--offline` | Skip live migration attempts | |

## Modes

1. **Evacuate** (`migrate-node.sh tappaas1`):
    - Finds all VMs currently running on the node
    - Migrates each to its configured HANode
    - VMs without an HANode are skipped with a warning

2. **Return** (`migrate-node.sh --return tappaas1`):
    - Finds all modules whose configured `node` is `tappaas1`
    - For each VM currently running elsewhere, migrates it back
    - VMs already on the correct node are skipped

3. **List** (`migrate-node.sh --list tappaas1`):
    - Shows both evacuate and return views without migrating
    - Color-coded: green = would migrate, yellow = no target/skipped

## Example workflow — planned maintenance

```bash
# 1. Check what would happen
migrate-node.sh --list tappaas1

# 2. Evacuate the node
migrate-node.sh --offline tappaas1

# 3. Perform maintenance on tappaas1
# ...

# 4. Return all VMs
migrate-node.sh --return --offline tappaas1
```

## Notes

- Each VM migration is delegated to `migrate-vm.sh`, which handles HA save/restore
- VMs without an HANode cannot be evacuated (requires manual migration)
- The summary shows migrated/skipped/failed counts

## See Also

- [migrate-vm.sh](migrate-vm.md) - Migrate individual VMs between nodes
- [update-HA.sh](update-ha.md) - Manage HA and replication for modules
