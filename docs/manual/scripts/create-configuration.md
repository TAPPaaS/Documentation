---
title: create-configuration.sh
description: Generate system configuration.json
---

# create-configuration.sh

Creates or updates the `configuration.json` file for the TAPPaaS system by querying the running Proxmox cluster. Supports both named arguments (with sensible defaults) and positional arguments for backward compatibility.

## Usage

```bash
# Named arguments (all optional — defaults are discovered from the Proxmox node)
create-configuration.sh [--upstream-git URL] [--branch NAME] [--domain DOMAIN]
                        [--email EMAIL] [--schedule FREQ] [--weekday DAY] [--hour H]
                        [--primary-node FQDN] [--update]

# Positional arguments (backwards compatible)
create-configuration.sh <upstreamGit> <branch> <domain> <email> <schedule> [weekday] [hour]
```

## Named Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--upstream-git` | Git repository URL | `github.com/TAPPaaS/TAPPaaS` |
| `--branch` | Git branch to track | `stable` |
| `--domain` | Primary domain for TAPPaaS | From Proxmox node FQDN, or existing config |
| `--email` | Admin email for SSL and notifications | From Proxmox `root@pam` user, or existing config |
| `--schedule` | Update frequency: `monthly`, `weekly`, `daily`, `none` | `weekly` |
| `--weekday` | Day of week for updates | `Tuesday` |
| `--hour` | Hour of day 0-23 | `2` |
| `--primary-node` | Primary node FQDN for cluster discovery | Auto-detect from config or `tappaas1.mgmt.internal` |
| `--update` | Update mode: preserve existing config, overlay provided args | *(flag)* |

## Default Discovery

When `--domain` or `--email` are not explicitly provided, the script SSHs to the primary Proxmox node and discovers:

- **Domain**: from the node's FQDN (via `hostname --fqdn`), extracting the domain portion (e.g., `node1.mydomain.com` → `mydomain.com`)
- **Email**: from `/etc/pve/user.cfg`, reading the `root@pam` user's email address

If the node is unreachable, the script falls back to placeholder values (`CHANGE-mytappaas.dev` / `CHANGE-tappaas@mytappaas.dev`) that must be updated before deployment.

## Examples

```bash
# Create with all defaults (discovers domain/email from Proxmox node)
create-configuration.sh

# Create with specific domain and email
create-configuration.sh --domain mytappaas.dev --email admin@mytappaas.dev

# Update existing config — only change the domain
create-configuration.sh --update --domain newdomain.com

# Update mode — re-discover nodes and validate
create-configuration.sh --update

# Legacy positional syntax
create-configuration.sh github.com/TAPPaaS/TAPPaaS main my.dev admin@my.dev weekly
```

## What it does

1. Discovers domain and email from the primary Proxmox node's installer settings
2. Queries the Proxmox cluster for all nodes via `pvecm` or `pvesh`
3. Gets IP addresses for each node via DNS or SSH
4. Creates or updates `/home/tappaas/config/configuration.json`
5. In update mode: preserves existing values, repositories, and `dns-hostname` mappings
6. Runs `validate-configuration.sh` on the result

## Generated configuration

The resulting `configuration.json` includes:

- **`tappaas` section**: `version`, `domain`, `email`, `nodeCount`, `repositories[]`, `updateSchedule`
- **`tappaas-nodes` array**: `hostname`, `dns-hostname` (optional), and `ip` for each node

## See Also

- [Update Scheduler](../update-tappaas.md) - Automated update system
- [copy-update-json.sh](copy-update-json.md) - Module JSON configuration
