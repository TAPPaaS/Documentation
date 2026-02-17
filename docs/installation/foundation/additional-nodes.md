---
title: Additional Nodes
description: Expand your TAPPaaS cluster with additional Proxmox nodes
---

# Additional PVE Nodes

This guide covers expanding your Proxmox cluster beyond the initial node for increased capacity and redundancy.

## Prerequisites

- [ ] [Proxmox Node](proxmox-node.md) (tappaas1) installed
- [ ] [Firewall](firewall.md) configured
- [ ] Additional hardware prepared
- [ ] Network connectivity to existing cluster

## Node Naming Convention

| Node | Hostname | IP Address |
|------|----------|------------|
| 1 | tappaas1.mgmt.internal | 10.0.0.10 |
| 2 | tappaas2.mgmt.internal | 10.0.0.11 |
| 3 | tappaas3.mgmt.internal | 10.0.0.12 |
| n | tappaasN.mgmt.internal | 10.0.0.(9+N) |

## Installation

### Install Proxmox VE

Use the same USB installation media as the initial node:

1. Boot from Proxmox VE USB
2. Configure with appropriate hostname and IP
3. Use the same root password as tappaas1
4. Complete installation and reboot

### Run Post-Installation Script

```bash
REPO="https://raw.githubusercontent.com/TAPPaaS/TAPPaaS/"
BRANCH="main"
curl -fsSL ${REPO}${BRANCH}/src/foundation/05-ProxmoxNode/install.sh | bash
```

## DNS Registration

Register the new node in OPNsense DNS:

1. Access OPNsense web interface
2. Navigate to **Services** → **Unbound DNS** → **Host Overrides**
3. Add the new node:

| Host | Domain | IP |
|------|--------|-----|
| tappaas2 | mgmt.internal | 10.0.0.11 |

## Network Bridge Configuration

The network bridge must be renamed for consistency.

### Edit Network Configuration

```bash
nano /etc/network/interfaces
```

Replace both occurrences of `vmbr0` with `lan`:

```
auto lan
iface lan inet static
    address 10.0.0.11/24
    gateway 10.0.0.1
    bridge-ports eth0
    bridge-stp off
    bridge-fd 0
```

### Reboot

```bash
reboot
```

After reboot, verify the node is accessible at the new IP.

## Join Cluster

### Get Join Information

On **tappaas1**, get the cluster join information:

1. Navigate to **Datacenter** → **Cluster**
2. Click **Join Information**
3. Copy the join information

### Join from New Node

On the new node's web interface:

1. Navigate to **Datacenter** → **Cluster**
2. Click **Join Cluster**
3. Paste the join information
4. Enter the root password for tappaas1
5. Click **Join**

Alternatively, via CLI on the new node:

```bash
pvecm add 10.0.0.10
```

## Failover Configuration (Optional)

If the node will serve as a firewall backup:

### Create WAN Bridge

1. Navigate to **tappaas2** → **Network**
2. Click **Create** → **Linux Bridge**
3. Configure:
   - Name: `wan`
   - Bridge ports: Secondary network interface (e.g., `eth1`)

This enables high-availability firewall failover.

## Storage Configuration

### Create ZFS Pool

Create a storage pool matching your setup:

```bash
# Mirror (2 disks)
zpool create tanka1 mirror /dev/sdb /dev/sdc

# Or RAIDZ1 (3+ disks)
zpool create tanka1 raidz /dev/sdb /dev/sdc /dev/sdd
```

### Add to Proxmox Storage

The ZFS pool should automatically appear in Proxmox storage configuration.

## Verification

Verify the node joined successfully:

```bash
# On any cluster node
pvecm status
pvecm nodes
```

Expected output shows all nodes with "online" status.

## Removing Nodes

If you need to remove a node later:

```bash
# From another cluster member
pvecm delnode tappaasN

# Then remove the node directory
rm -rf /etc/pve/nodes/tappaasN
```

## Repeat for Additional Nodes

Follow this procedure for each additional node you want to add to the cluster.

## Next Steps

Continue to [NixOS Template](nixos-template.md) creation.
