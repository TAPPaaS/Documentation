---
title: Backup
description: TAPPaaS backup, disaster recovery and high availability design
---

# Backup, Disaster Recovery and High Availability

## Introduction

Backup, Disaster Recovery (DR) and High Availability (HA) go hand in hand and are typical topics that are not well planned for SMB and home use.

- **High Availability**: Ensure that the services continue running in case of component failure
- **Backup**: Ensuring that you never lose data
- **Disaster Recovery**: Ensure that you can recover from a fatal error

A goal for TAPPaaS is to ensure all three topics are delivered out of the box.

---

## High Availability

TAPPaaS provides options for managing the following high availability scenarios:

- Hard disk failure
- General hardware failure
- Reboots and reconfiguration of TAPPaaS nodes
- Overloaded services
- Internet failure

### Hard Disk Redundancy

The Proxmox and associated ZFS file system allow TAPPaaS to be configured with Mirror or RAIDz1/2 redundancy.

- TAPPaaS separates between important and non-important services, deployed on two different ZFS datapools (tanka and tankb). This way you can reserve the hard disk redundancy to the services that are high in importance
- TAPPaaS does not enforce a particular redundancy level for datapools, but recommends mirror for tanka and no redundancy for tankb

### Cluster Setup

TAPPaaS supports setting Proxmox up in a cluster with 3 or more nodes. It is not a requirement but recommended for anything but a small setup.

If TAPPaaS is configured on 3 or more nodes then each of the high priority services are setup with a default failover node, and regular snapshot transfer is configured.

### Internet Failure

It is the intent to test the OPNsense setup and associated caching recursive DNS and ensure that the local TAPPaaS ecosystem continues to function when there is an internet outage.

---

## Backup Strategy

We follow the **3-2-1 backup design principle** for TAPPaaS:

- Have **3 copies** of data
- Have **2 different formats** of backup
- Have **1 backup** in a remote location

### Design Principles

The primary design principle for the TAPPaaS backup strategy is that every configuration and all user data is located inside the VMs that host the services. The TAPPaaS instance configuration itself is located inside the TAPPaaS CICD VM.

### Proxmox Backup Server (PBS)

Every TAPPaaS system should have a local Proxmox Backup Server. The PBS runs on a regular interval (default is daily). With compression and deduplication it can keep:

- Daily backup for 7 days
- Weekly for 4 weeks
- Monthly for one year
- Yearly forever

This ensures you can go back in time in case of a long running hacking attempt or if an accidental delete is not discovered immediately.

### Remote Backup

The second layer of backup ties the local PBS to a remote PBS backup service using the PBS replication feature. Any TAPPaaS system can act as a PBS for another TAPPaaS system. Backups are encrypted by default, ensuring that you do not need to trust the remote TAPPaaS operator.

### Personal Backup

The final aspect of backup allows individual users to create their own data backup on a detachable media (typically a USB HD). This data is stored in the native format of the individual applications. This last backup also allows a user to leave a TAPPaaS system without losing their data.

---

## Disaster Recovery

There are generally 4 types of disasters to deal with:

1. Hardware failure (including environmental failures like power spikes or fire)
2. Software updates that go wrong
3. Hackers infiltrate and destroy, encrypt or generally make the system unreliable
4. The user (or Administrator) accidentally deletes data or disrupts the working installation

### Recovery Methods

TAPPaaS operates with 3 kinds of disaster recovery methods:

1. **Rebuild from backup** - Restore the system from local or remote backup
2. **Rent space on another TAPPaaS system** - Re-establish services from backup in separate VLANs
3. **Cloud recovery** - Rent VPCs in a cloud provider and re-establish VMs
