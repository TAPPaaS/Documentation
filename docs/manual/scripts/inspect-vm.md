---
title: inspect-vm.sh
description: 3-column config/git/actual VM comparison
---

# inspect-vm.sh

Generates a 3-column comparison table for a module's VM showing config, git, and actual values.

## Usage

```bash
inspect-vm.sh <module-name>
```

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `module-name` | Name of the module to inspect | `openwebui` |

## Examples

```bash
inspect-vm.sh openwebui
inspect-vm.sh vaultwarden
```

## What it does

1. Reads deployed config from `~/config/<module>.json`
2. Reads git source JSON from the module's `location` directory
3. Queries actual VM config from Proxmox via `qm config`
4. Displays a comparison table with color-coded differences

## Color coding

- **Yellow** — config value differs from git value (config drift from source)
- **Red** — actual VM value differs from config value (VM out of sync)

## Fields compared

vmname, vmid, node, cores, memory, diskSize, storage, bios, cputype, bridge0, zone0 (with VLAN resolution), mac0, HANode, description, vmtag

## See Also

- [inspect-cluster.sh](inspect-cluster.md) - Cluster-wide VM overview
