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

Second design principle is to use commodity hardware coupled with smart software and smart deployment designs


## Design decisions

We decided to go with "zfs" as the storage manager. zfs offer most of the criteria we are seeking for an efficient, scalable, redundant, flexible and trust worthy  storage solution. we combine this with a standard setup that uses snapshot and replication across cluster nodes. 

The decision to use zfs allows us to have an enterprise grade storage solution for TAPPaaS without investing in dedicated costly SAN/NAS solutions. In small to medium sized deployment it can reduce the hardware cost with up to 50%

The one item the solution is NOT providing is cross cluster node synchronous replication. best replication is 5 minutes out of sync. We consider it a readmap iten to provide this as an option using Cepth and Garage S3. 

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

zfs groups physican hardware (HDD/SSDs) into storage pools. 

In TAPPaaS the pools follow a naming convention: `tanka1`, `tankb1`, etc., mounted at `/`.

### tanka Pools ("a" designation)

- Provide redundancy and high performance
- Typically use mirrored SSDs
- Host VM virtual disks and high-availability module replication

### tankb Pools ("b" designation)

- Omit RAID redundancy to conserve resources
- Accommodate less performant storage
- Support backup systems, S3 buckets, and logging infrastructure

### tankc Pools ("c" designation)

- Provide storage for Backup.
- optimized to be cost efficient and mostly single stream write only

Additional pools using letters "d," "e," and beyond support specialized storage characteristics as needed.
