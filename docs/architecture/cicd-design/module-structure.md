---
title: Module Structure
description: TAPPaaS module directory structure and conventions
---

# Module Structure

This page documents the structure and conventions for TAPPaaS modules.

---

## Module Definition

Each TAPPaaS module is defined by a `<module>.json` file that specifies its configuration, resource requirements, and dependencies.

### Core Fields

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `version` | string | Version of the module (format: `X.Y.Z`) | - |
| `description` | string | Text displayed on Proxmox summary page | "" |
| `maintainer` | string | Maintainer of the module (typically GitHub username) | "" |
| `releaseDate` | string | Date version was released (format: `YYYY-MM-DD`) | - |
| `status` | string | Development stage: `Development`, `Testing`, `Production`, `Deprecated` | Development |

### VM Configuration

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `vmid` | integer | Unique VM ID across nodes (100-999999) | *required* |
| `vmname` | string | VM/module/hostname name | *required* |
| `vmtag` | string | Proxmox tags (comma-separated) | TAPPaaS |
| `node` | string | Target Proxmox node (pattern: `tappaas[0-9]+`) | tappaas1 |
| `bios` | string | BIOS type: `ovmf` or `seabios` | ovmf |
| `ostype` | string | Proxmox VM optimization: `l26`, `l24`, `win10`, `win11`, `other` | l26 |

### Resources

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `cores` | integer | CPU cores allocated (1-128) | 2 |
| `memory` | integer | RAM in megabytes (min 512) | 4096 |
| `diskSize` | string | Disk size with unit (e.g., `8G`, `500M`) | 8G |
| `storage` | string | Storage pool name | tanka1 |

### Image Configuration

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `imageType` | string | Image source: `clone`, `iso`, `img`, `apt` | *required* |
| `image` | string | Image identifier (interpretation depends on imageType) | *required* |
| `imageLocation` | string | URL for image file (used with `iso`/`img` types) | - |
| `cloudInit` | string | Cloud-init support: `"true"` or `"false"` | "true" |

### Network Configuration

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `bridge0` | string | Proxmox bridge for net0 | lan |
| `mac0` | string | MAC address for net0 (format: `XX:XX:XX:XX:XX:XX`) | - |
| `zone0` | string | Security zone for net0 (must exist in zones.json) | mgmt |
| `trunks0` | string | Additional zones to trunk on net0 (semicolon-separated) | - |
| `bridge1` | string | Proxmox bridge for net1 (optional second NIC) | lan |
| `mac1` | string | MAC address for net1 | - |
| `zone1` | string | Security zone for net1 | mgmt |
| `trunks1` | string | Additional zones for net1 (semicolon-separated) | - |

### High Availability

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `HANode` | string | Secondary node for HA (`NONE` or `tappaas[0-9]+`) | NONE |
| `replicationSchedule` | string | Cron-style replication interval | */15 |

### Dependencies

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `dependsOn` | array | List of services this module depends on (format: `module:service`) | [] |
| `provides` | array | Services this module delivers | [] |
| `location` | string | Absolute path to module directory (auto-set) | - |

---

## Standard Scripts

*To be documented.*

---

## Service Scripts

*To be documented.*


