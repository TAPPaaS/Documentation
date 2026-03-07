---
title: inspect-cluster.sh
description: Compare running VMs against module configurations
---

# inspect-cluster.sh

Compares actual running VMs across the Proxmox cluster against module configurations.

## Usage

```bash
inspect-cluster.sh
```

## What it does

1. Discovers all reachable Proxmox nodes (tappaas1–tappaas9)
2. Queries cluster-wide VM list via `pvesh get /cluster/resources`
3. Reads all `~/config/*.json` files that define a `vmid`
4. Displays a table of all running VMs with their config status
5. Lists configured modules whose VMs are not running

## Output

- VMs with a matching config show green "yes"
- VMs not in any config show yellow "NOT IN CONFIG"
- Configured modules with no running VM show red "NOT RUNNING"

## See Also

- [inspect-vm.sh](inspect-vm.md) - Detailed comparison for a single module
