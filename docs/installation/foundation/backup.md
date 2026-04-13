---
title: Backup
description: Install Proxmox Backup Server for TAPPaaS
---

# Backup Installation

This guide covers installing Proxmox Backup Server (PBS) for your TAPPaaS infrastructure.

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
cd ~/TAPPaaS/src/foundation/backup
install-module.sh backup
```

The script automatically:

1. Create the PBS datastore (tappaas_backup)
2. Create the tappaas@pbs user
3. Set permissions for the user on the datastore
4. Configure retention policy (4 last, 14 daily, 8 weekly, 12 monthly, 6 yearly)
5. Get the PBS fingerprint
6. Add PBS storage to Proxmox datacenter
7. Create a daily backup job at 21:00 for all VMs
8. Register DNS entry in OPNsense (backup.mgmt.internal)

For backup operations, restoration, monitoring, and troubleshooting, see the [Backup Manual](../../manual/backup.md).

## Next Steps

Continue to [Identity](identity.md) management setup.
