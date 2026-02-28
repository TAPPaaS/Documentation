---
title: update-HA.sh
description: Manage Proxmox HA and ZFS replication for modules
---

# update-HA.sh

Manages Proxmox High Availability (HA) and ZFS replication for a TAPPaaS module based on its JSON configuration.

## Usage

```bash
update-HA.sh <module-name>
```

## What it does

Based on the module's `HANode` field in `<module>.json`:

1. **If HANode is "NONE" or not present:**
   - Removes VM from any HA group
   - Deletes any existing replication jobs

2. **If HANode is set to a valid node (e.g., "tappaas2"):**
   - Validates the HA node is reachable
   - Verifies storage exists on both nodes
   - Adds VM to HA resources with node-affinity rule
   - Sets up ZFS replication using `replicationSchedule` (default: `*/15`)

## JSON fields used

| Field | Description | Default |
|-------|-------------|---------|
| `vmid` | VM ID (required) | - |
| `node` | Primary node | `tappaas1` |
| `HANode` | Secondary node for HA | `NONE` |
| `replicationSchedule` | Cron-style replication interval | `*/15` |
| `storage` | ZFS storage pool | `tanka1` |

## Examples

```bash
# Configure HA for nextcloud module
update-HA.sh nextcloud

# After removing HANode from JSON, remove HA config
update-HA.sh nextcloud
```

## Requirements

- SSH access to all Proxmox nodes as root
- Same storage pool must exist on both primary and HA nodes
- Proxmox HA services must be enabled (pve-ha-lrm, pve-ha-crm, corosync)

## See Also

- [update-os.sh](update-os.md) - OS-specific updates
- [Module Definition](../../architecture/cicd-design/module-structure.md#module-definition) - Module JSON fields
