---
title: Software Selection
description: TAPPaaS software selection and stack design
---

# Software Selection

This is the reason we call it TAPPaaS. Pronounced Tapas like the Spanish dish: A collection of delicious appetizers that makes up a comprehensive serving.

The Software Stack of TAPPaaS delivers the capabilities we believe is needed for a well served Private IT Platform.

Selecting from the enormous pool of software we have used the principles of:

- must be Open Source
- must show a track record of being Secure
- must be "established", and sufficient feature complete
- must be open w.r.t. data formats (enabling migration away from TAPPaaS and/or away from the package)



## Foundation

Mapping of TAPPaaS functionality to FOSS solutions

| Capability | Priority | Software | Comments |
|------------|-----------|----------|----------|
| Compute    | Mandatory | Proxmox | provide excellent compute cluster capability |
| Storage    | Mandatory | Proxmox-ZFS | ZFS gives a lot of flexibility. and is build into proxmox, making it well aligned with Cluster management |
| Firewall.  | Mandatory | OPNsense | Virtualized and combined with a layer 3 switch and proxmox bridging and vlan support |
| User Mgmt. | Mandatory | Authentik | | 
| Backup     | Mandatory | Proxmox Backup Server | |

### Base Cloud Infrastructure platform: Proxmox

This  deliver most of the Compute and Storage foundation

Alternatives:

- XCP-ng: seems less polished and with less features. 
  - But it also seems more "free"
- FreeNAS, TrueNAS: good for storage, but not really a cloud platform, they do not have clustering and HA as Proxmox. Uses the same underpinning zfs file system

### Persistent Storage layer

proxmox with ZFS gives: RAID, Snapshotting, Replication, NFS, iSCSI, 
Problem with proxmox is a limited GUI for management, and further the choice explosion zfs gives makes it hard to design a solution
TAPPaaS will address this with recommended setup and automation

Note that proxmox and zfs do not give Hight Available storage. 
For this we plan on using CEPHT and Garage S3
We do not consider this a Foundation. but something that goes in to the business layer of TAPPaaS together with a HA implementation of a relational database

### Firewall: OPNSense

Alternatives are:

- PFsense: PFSense is the original but is going more and more commercial
- OpenWRT: it seems less scalable and less feature rich
- proxmox firewall: would make it easier as it is already build in, but less secure

### Backup: 

- We generally keep all functions contained in VM's or LCM's. 
- Running a Proxmox Backup service allow us to store backups on secondary tank, on separate nodes and on separate (off site) TAPPaaS systems
- In case of TAPPaaS deployment in High Availability then the HA mirror will add another backup copy
- We need to find a solution for backing up the PVE nodes them self, and any data that we store outside containers.
- We need to give special consideration to encryption keys

We will consider znapzend, used to snapshot and replicate zfs volumes across servers



## AI Stack

## Productivity Stack

## Home Stack

| Capability | Priority | Software | Comments |
|------------|-----------|----------|----------|
| email | medium | PostIO | Very difficult to run autonomously, maintenance is high|
| Address book | High | NextCloud | need to be integrated into many other applications |
| Calendering | High | NextCloud | |
| Note Taking | Medium | ?? | Could simply be files in NextCloud, but need to be investigated |
| Photos | High | Immich | considered NextCloud with Memories module, but not well functioning on Android ||
| Music | High | Jellyfin | |
| Video | High | Jellyfin| |
| Podcasts | medium | [audiobookshelf](https://www.audiobookshelf.org/)?? | |
| Document | high | NextCloud Office / Libraoffice / OnlyOffice | consider Nextcloud, but not as FOSS as we would prefer |
| File synching | high | NextCloud | also function as document backup |
| Offline Web | medium | Karakeep | self-hosted open source version of Pocket |
| Virtual Assistant | medium | litellm, olama + Home Assistant | |
| Bookshelf | low | Calibra?? | |
| chat and video | High | Nextcloud ? | encourage use of Signal. need a solution for resiliency

## Small Community (variation of HOME)

| Capability | Priority | Software | Comments |
|------------|-----------|----------|----------|
| WiFi Rooming | medium | R.O.B.I.N. ?? | |
| Internet Sharing | High | OPNsense | |
| Public Bookshelf | Medium | Calibra, wikipedia hosting, ... ?? | |
| Community Social | High | Mastedont? | |
| Video Conferencing | low | Nextcloud? | |

## Productivity Stack

| Capability | Priority | Software | Comments |
|------------|-----------|----------|----------|
| Email | High | | | 
| Office Suite | High | OnlyOffice/Nextcloud Office | |
| Corporate website | High | | |
| ERP System | Medium |||
| Office Wifi | Medium | | |
| Corporate VPN | High | NetBird | |
| Video Conferencing | Medium | NextCloud | |
| Chat | Medium | NextCloud? | |

## Software Development Stack

| Capability | Priority | Software | Comments |
|------------|-----------|----------|----------|
| Git | High | CodeBerg | |
| CICD | High | Terraform, Ansible | |
| Backlog | High | ?? | |
| Application platform | High | K3S, Garage, PostGreSQL | |
| Reverse Proxy | High | Caddy | for development the requirement is easy access to a reverse proxy in a secure manner |




