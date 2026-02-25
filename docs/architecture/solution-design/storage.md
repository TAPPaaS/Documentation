---
title: Storage
description: TAPPaaS storage design
---

# Storage Design

## Overview

The storage architecture for TAPPaaS prioritizes scalability, data security, and fault tolerance through ZFS-based pooling. The system accommodates two primary data categories: high-value information requiring robust redundancy, and secondary-tier data that can tolerate greater risk.

---

## Key Design Principles

The framework emphasizes "default setup should cater for 90% of use cases," minimizing complex decision-making for operators.

### Growth Mechanisms

- Expanding existing ZFS pools with additional disks
- Adding new pools to Proxmox nodes
- Scaling across multiple Proxmox systems

### Redundancy Strategies

- ZFS RAID configurations
- Cross-node snapshots and replication
- Backup systems between local and remote installations

The design remains hardware-agnostic regarding SSD/HDD selection and caching approaches.

---

## Pool Architecture

Pools follow a naming convention: `tanka1`, `tankb1`, etc., mounted at `/mnt`.

### tanka Pools ("a" designation)

- Provide redundancy and high performance
- Typically use mirrored SSDs
- Host VM virtual disks and high-availability module replication

### tankb Pools ("b" designation)

- Omit RAID redundancy to conserve resources
- Accommodate less performant storage
- Support backup systems, S3 buckets, and logging infrastructure

Additional pools using letters "c," "d," and beyond support specialized storage characteristics as needed.
