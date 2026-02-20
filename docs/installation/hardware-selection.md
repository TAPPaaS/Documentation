---
title: Hardware Selection
description: Guide to selecting appropriate hardware for your TAPPaaS deployment
---

# Hardware Selection

Selecting the right hardware is crucial for a successful TAPPaaS deployment. This guide helps you size your infrastructure based on your requirements.

## Design Process

Hardware selection follows these phases:

1. **Problem Definition** - Determine what operational challenges TAPPaaS should address
2. **Infrastructure Sizing** - Calculate compute and storage requirements
3. **Hardware Procurement** - Acquire equipment matching your calculations

## Minimum Requirements

### Single Node Setup

For a basic TAPPaaS installation:

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores | 8+ cores |
| RAM | 16 GB | 32+ GB |
| Boot disk | 256 GB | 512 GB SSD |
| tanka (data) | 500 GB | 2x 2 TB mirrored |
| tankb (backup) | - | 12 TB |
| Network | 1 Gbps | 2.5 Gbps+ |

**Minimum disk layout:**

- 1x 256 GB boot disk
- 1x 500 GB tanka1 (primary data pool)

**Recommended disk layout:**

- 1x 512 GB SSD (boot)
- 2x 2 TB mirrored (tanka - redundant data pool)
- 1x 12 TB (tankb - backup pool)

### Multi-Node Cluster

For high availability and additional capacity:

| Component | Per Node | Notes |
|-----------|----------|-------|
| CPU | 4+ cores | More cores enable more VMs |
| RAM | 16+ GB | Plan for VM overhead |
| Storage | 256+ GB | Consider ZFS mirroring |
| Network | 1+ Gbps | Dedicated management NIC recommended |

## Resource Planning

When planning resources, account for:

### Foundation Services

| Service | RAM | Storage |
|---------|-----|---------|
| Proxmox Host | 2 GB | 32 GB |
| OPNsense Firewall | 2 GB | 16 GB |
| TAPPaaS CICD | 4 GB | 50 GB |
| NixOS Template | 1 GB | 10 GB |
| Identity (Authentik) | 4 GB | 20 GB |
| Backup Server | 2 GB | Variable |

### Optional Stacks

| Stack | RAM | Storage | GPU |
|-------|-----|---------|-----|
| AI Stack (OpenWebUI) | 4-8 GB | 50 GB | Optional |
| AI Stack (vLLM) | 8-32 GB | 100+ GB | Recommended |
| Productivity (n8n) | 2-4 GB | 20 GB | - |
| Home (Home Assistant) | 2 GB | 32 GB | - |

## Hardware Recommendations

### Entry Level

Repurpose an old workstation or small server:

- Intel i5/i7 or AMD Ryzen 5/7
- 32 GB DDR4 RAM
- 500 GB NVMe SSD
- Gigabit Ethernet

### Production Ready

For reliable operation:

- Server-grade CPU (Xeon, EPYC)
- 64+ GB ECC RAM
- Multiple NVMe drives for ZFS
- Dual network interfaces
- UPS power protection

### High Availability

For mission-critical deployments:

- 2-3 identical nodes
- Shared or replicated storage
- Redundant networking
- Remote management (IPMI/iLO/iDRAC)

## Storage Considerations

### ZFS Recommendations

TAPPaaS uses ZFS for storage management:

- **Mirror** - Minimum 2 drives, good redundancy
- **RAIDZ1** - Minimum 3 drives, single drive fault tolerance
- **RAIDZ2** - Minimum 4 drives, two drive fault tolerance

### Storage Tiers

Consider separating:

- **Fast tier** - NVMe for VMs and databases
- **Bulk tier** - HDD for backups and archives

## Network Requirements

### Basic Setup

- Single NIC with VLAN support
- Managed switch for VLAN trunking
- Reliable internet connection

### Advanced Setup

- Dedicated management network
- Separate storage network
- Multiple uplinks for redundancy

## Next Steps

Once you have selected your hardware:

1. Proceed to [Preparation](preparation.md)
2. Begin [Foundation](foundation/index.md) installation
