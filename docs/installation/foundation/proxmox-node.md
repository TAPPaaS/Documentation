---
title: Proxmox Node
description: Install and configure the initial Proxmox VE hypervisor node
---

# Proxmox Node Setup

This guide covers installing Proxmox Virtual Environment (PVE) on your first TAPPaaS node, referred to as "tappaas1".

## Prerequisites

Before starting:

- [ ] Hardware prepared per [Hardware Selection](../hardware-selection.md)
- [ ] Proxmox VE ISO downloaded and bootable USB created
- [ ] Network design documented per [Preparation](../preparation.md)
- [ ] Root password ready

## Installation

### Boot and Install

1. Insert the Proxmox VE bootable USB
2. Boot from USB and select "Install Proxmox VE"
3. Accept the license agreement
4. Select the target disk for installation

### Configuration During Install

Configure the following during installation:

| Setting | Value |
|---------|-------|
| Hostname (FQDN) | `tappaas1.mgmt.internal` |
| IP Address | `10.0.0.10` |
| Netmask | `255.255.255.0` |
| Gateway | Your router IP |
| DNS | Your router IP or `1.1.1.1` |

!!! note "Subsequent Nodes"
    Additional nodes use `tappaas2.mgmt.internal` (10.0.0.11), `tappaas3.mgmt.internal` (10.0.0.12), etc.

### Complete Installation

1. Set a strong root password
2. Provide an administrator email address
3. Review settings and confirm installation
4. Reboot when prompted and remove the USB drive

## Post-Installation

### Access Web Interface

After reboot, access the Proxmox web interface:

```
https://10.0.0.10:8006
```

Login with:
- Username: `root`
- Password: Your configured password
- Realm: `Linux PAM standard authentication`

### Run TAPPaaS Setup Script

Execute the post-installation script from the Proxmox shell:

```bash
REPO="https://raw.githubusercontent.com/TAPPaaS/TAPPaaS/"
BRANCH="main"
curl -fsSL ${REPO}${BRANCH}/src/foundation/05-ProxmoxNode/install.sh | bash
```

This script configures foundational settings for TAPPaaS.

## Cluster Creation

On the first node only, create the cluster:

```bash
pvecm create TAPPaaS
```

!!! info "Joining Additional Nodes"
    Additional nodes join the cluster later using the GUI. Copy the cluster join information from tappaas1 when adding new nodes.

## Storage Configuration

### Create ZFS Pool

For data storage, create a ZFS pool named "tanka1":

**Via GUI:**

1. Navigate to **Datacenter** → **tappaas1** → **Disks** → **ZFS**
2. Click **Create: ZFS**
3. Configure:
   - Name: `tanka1`
   - RAID Level: Mirror (minimum 2 disks)
   - Select available disks

**Via CLI:**

```bash
# For mirrored pool (2 disks)
zpool create tanka1 mirror /dev/sdb /dev/sdc

# For RAIDZ1 (3+ disks)
zpool create tanka1 raidz /dev/sdb /dev/sdc /dev/sdd
```

### Wipe Existing Partitions

If disks have existing data:

```bash
# Check disk status
lsblk

# Wipe disk (replace sdX with actual device)
wipefs -a /dev/sdX
```

## Network Configuration

### Verify Bridge Configuration

Ensure the network bridge is configured:

```bash
cat /etc/network/interfaces
```

You should see `vmbr0` configured with your management IP.

### Prepare for Firewall

The network will be reconfigured when installing the [Firewall](firewall.md). The bridge will be renamed from `vmbr0` to `lan`.

## Verification

Confirm successful installation:

```bash
# Check Proxmox version
pveversion

# Check cluster status
pvecm status

# Check ZFS pool
zpool status tanka1

# Check network
ip addr show vmbr0
```

## Troubleshooting

### Cannot Access Web Interface

- Verify IP configuration: `ip addr`
- Check firewall: `pve-firewall status`
- Ensure port 8006 is not blocked

### ZFS Pool Creation Fails

- Verify disks are not in use: `lsblk`
- Wipe existing partitions: `wipefs -a /dev/sdX`
- Check for existing ZFS pools: `zpool import`

## Next Steps

Proceed to [Firewall](firewall.md) installation before adding additional nodes.
