---
title: create-configuration.sh
description: Generate system configuration.json
---

# create-configuration.sh

Creates the `configuration.json` file for the TAPPaaS system by querying the running cluster.

## Usage

```bash
create-configuration.sh <upstreamGit> <branch> <domain> <email> <updateSchedule> [weekday] [hour]
```

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `upstreamGit` | Git URL of the upstream repository | `github.com/TAPPaaS/TAPPaaS` |
| `branch` | Branch to use for updates | `main` |
| `domain` | Primary domain for TAPPaaS | `mytappaas.dev` |
| `email` | Admin email for SSL and notifications | `admin@mytappaas.dev` |
| `updateSchedule` | Update frequency | `monthly`, `weekly`, `daily`, `none` |
| `weekday` | (Optional) Day of week for updates, default: Thursday | `Wednesday` |
| `hour` | (Optional) Hour of day 0-23, default: 2 | `3` |

## Examples

```bash
create-configuration.sh github.com/TAPPaaS/TAPPaaS main mytappaas.dev admin@mytappaas.dev monthly
create-configuration.sh github.com/TAPPaaS/TAPPaaS main mytappaas.dev admin@mytappaas.dev weekly Wednesday 3
```

## What it does

1. Queries Proxmox cluster for all nodes via `pvesh`
2. Lists all VMs and their IP addresses
3. Creates `/home/tappaas/config/configuration.json` with a global `updateSchedule`

## Generated configuration includes

- `repositories` array (initialized with the upstream repo and branch from arguments), `domain`, `email`, `updateSchedule` (in the `tappaas` section)
- `nodes` array with hostname and IP for each node

## See Also

- [Update Scheduler](../update-tappaas.md) - Automated update system
- [copy-update-json.sh](copy-update-json.md) - Module JSON configuration
