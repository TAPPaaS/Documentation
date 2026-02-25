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

## Quick start

In order to simplify it we have two standard recommendations that can be used as a starting point

- Minimum config: Good for trying out TAPPaaS, potentially ok for a small home installation
- Redundant config: a good solid setup with mirrored disks, and High Availability capabilities with 3 compute nodes 


### Minimum config: Single Node Setup

For a basic TAPPaaS installation:

| Component | Minimum |  for production |
|-----------|---------|-------------|
| CPU | 4 cores | 8+ cores |
| RAM | 16 GB | 32+ GB |
| Boot disk | 256 GB | 512 GB SSD |
| tanka1 (VMs and data) | 500 GB | 2x 2 TB mirrored |
| tankb1 (non critical data) | none | 4TB |
| tankc1 (backup) | none | 12 TB |
| Network | 2x 1 Gbps | 1Gbps + 2.5 Gbps |

Disk and RAM can be adjusted based on expected data load.

If local AI models wil lbe used then add a GPU card to setup.

### Redundant config: Multi-Node Cluster

For high availability and additional capacity we recommend a 3 node cluster setup

- Node 1: Primary node running Foundations stack
- Node 2: HA and AI node: Runs that AI stack and have the GPU card
- Node 3: Backup node, small machine with a large tankc1 for backup storage

The individual nodes are designed based on recommendation from "minimum configuration"

Consider using ECC memoriy for Node 1 and possible node 2.
If high amount of storage is needed then consider using zfs raidz2 with traditional disk complemented with an SSD for cache

## Resource Planning

**Work in Progress**

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


## Next Steps

Once you have selected your hardware:

1. Proceed to [Preparation](preparation.md)
2. Begin [Foundation](foundation/index.md) installation
