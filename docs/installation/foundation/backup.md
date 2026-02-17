---
title: Backup
description: Configure Proxmox Backup Server for TAPPaaS
---

# Backup Configuration

This guide covers installing and configuring Proxmox Backup Server (PBS) for your TAPPaaS infrastructure.

## Overview

Proxmox Backup Server provides:

- Incremental backups with deduplication
- VM and container backup support
- Encrypted backup storage
- Automated retention policies

## Installation

### Run Installation Script

From the tappaas-cicd VM:

```bash
cd ~/TAPPaaS/src/foundation/35-backup
./install.sh
```

The script automatically:

- Creates the PBS datastore (`tappaas_backup`)
- Creates the `tappaas@pbs` user
- Sets appropriate permissions
- Configures retention policies
- Registers DNS entries

## Available Scripts

| Script | Purpose |
|--------|---------|
| `install.sh` | Deploy PBS and configure components |
| `restore.sh` | Restore VMs from backups |
| `backup-manage.sh` | Operational management tasks |

## Backup Operations

### Check Status

```bash
./backup-manage.sh status
```

### List Backup Jobs

```bash
./backup-manage.sh list
```

### Run Immediate Backup

```bash
# Backup specific VM
./backup-manage.sh backup 100

# Backup all VMs
./backup-manage.sh backup-all
```

### Prune Old Backups

```bash
./backup-manage.sh prune
```

### Garbage Collection

Reclaim storage space:

```bash
./backup-manage.sh gc
```

## Restoration

### Restore Latest Backup

```bash
./restore.sh <vmid>
```

### Restore Options

```bash
# Restore to specific node
./restore.sh <vmid> --node tappaas2

# Restore to different storage
./restore.sh <vmid> --storage tanka1

# Restore specific snapshot
./restore.sh <vmid> --snapshot backup/vm/100/2024-01-15T10:30:00Z
```

## Web Interface

Access the PBS dashboard:

```
https://pbs.mgmt.internal:8007
```

Authentication options:

| Account | Type |
|---------|------|
| `root@pam` | Linux system root |
| `tappaas@pbs` | Dedicated backup user |

## Retention Policy

Default retention settings:

| Policy | Value | Coverage |
|--------|-------|----------|
| Keep Last | 4 | Most recent backups |
| Keep Daily | 14 | Two weeks of daily |
| Keep Weekly | 8 | Two months of weekly |
| Keep Monthly | 12 | One year of monthly |
| Keep Yearly | 6 | Six years of yearly |

### Modify Retention

To adjust retention policies, edit the datastore configuration in the PBS web interface or via CLI.

## Backup Schedule

By default, backups run:

- **Daily** at 2:00 AM
- Includes all VMs and containers
- Prune runs after backup completion

### Modify Schedule

Edit the backup job in Proxmox:

1. Navigate to **Datacenter** → **Backup**
2. Select the backup job
3. Modify schedule as needed

## Monitoring

### Check Backup Health

```bash
# View recent tasks
./backup-manage.sh tasks

# Check datastore usage
./backup-manage.sh usage
```

### Alerts

Configure email alerts in PBS:

1. Navigate to **Configuration** → **Notifications**
2. Add email recipient
3. Configure notification rules

## Verification

Regularly verify backups:

```bash
# Verify backup integrity
./backup-manage.sh verify

# Test restore (creates temporary clone)
./backup-manage.sh test-restore 100
```

## Troubleshooting

### Backup Fails

- Check disk space: `./backup-manage.sh usage`
- Verify VM is running: `qm status <vmid>`
- Check PBS logs: `journalctl -u proxmox-backup-proxy`

### Restore Fails

- Verify backup exists: `./backup-manage.sh list`
- Check target storage capacity
- Review PBS task logs

## Security Considerations

- PBS uses encrypted connections
- Consider enabling backup encryption for sensitive data
- Restrict `tappaas@pbs` permissions appropriately
- Store encryption keys securely off-site

## Next Steps

Continue to [Identity](identity.md) management setup.
