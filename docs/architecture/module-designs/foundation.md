---
title: Foundation Stack Modules
description: Module designs for the Foundation Stack
---

# Foundation Stack Modules

This page documents the module designs for the Foundation Stack components.

---

## Cluster Module

The Cluster module provides the core virtualization and high availability services.

```mermaid
flowchart TB
    subgraph Capabilities
        Compute[Compute Capability]
        HA[High Availability Capability]
    end

    subgraph Cluster Module
        ClusterComp[Cluster Component]
        VMService([VM Service])
        HAService([HA Service])
        VMService -.->|provided by| ClusterComp
        HAService -.->|provided by| ClusterComp
    end

    Compute -.->|realized by| ClusterComp
    HA -.->|realized by| ClusterComp
```

| Attribute | Value |
|-----------|-------|
| **Provides** | vm, ha |
| **Depends On** | _(none)_ |
| **Consumed By** | firewall, tappaas-cicd, identity, litellm, openwebui, vaultwarden, netbird-client, unifi |

---

## Firewall Module

The Firewall module provides network security and reverse proxy services.

```mermaid
flowchart TB
    subgraph Capabilities
        Network[Network Security Capability]
        Proxy[Reverse Proxy Capability]
    end

    subgraph Firewall Module
        FWComp[Firewall Component]
        FirewallService([Firewall Service])
        ProxyService([Proxy Service])
        FirewallService -.->|provided by| FWComp
        ProxyService -.->|provided by| FWComp
    end

    subgraph Cluster Module
        VMService([VM Service])
        HAService([HA Service])
    end

    Network -.->|realized by| FWComp
    Proxy -.->|realized by| FWComp
    FWComp -->|depends on| VMService
    FWComp -->|depends on| HAService
```

| Attribute | Value |
|-----------|-------|
| **Provides** | firewall, proxy |
| **Depends On** | cluster:vm, cluster:ha |
| **Consumed By** | identity, litellm, openwebui, vaultwarden, netbird-client |

---

## Identity Module

The Identity module provides authentication and access control services.

```mermaid
flowchart TB
    subgraph Capabilities
        Auth[Authentication Capability]
        Access[Access Control Capability]
    end

    subgraph Identity Module
        IdComp[Identity Component]
        subgraph Sub-Components
            Authentik[Authentik App]
        end
        IdentityService([Identity Service])
        AccessService([Access Control Service])
        IdComp --> Authentik
        IdentityService -.->|provided by| IdComp
        AccessService -.->|provided by| IdComp
    end

    subgraph Dependencies
        VMService([VM Service])
        HAService([HA Service])
        NixOSService([NixOS Service])
        BackupService([Backup Service])
        ProxyService([Proxy Service])
    end

    Auth -.->|realized by| IdComp
    Access -.->|realized by| IdComp
    IdComp -->|depends on| VMService
    IdComp -->|depends on| HAService
    IdComp -->|depends on| NixOSService
    IdComp -->|depends on| BackupService
    IdComp -->|depends on| ProxyService
```

| Attribute | Value |
|-----------|-------|
| **Provides** | identity, accessControl |
| **Depends On** | cluster:vm, cluster:ha, templates:nixos, backup:vm, firewall:proxy |
| **Consumed By** | litellm, openwebui, vaultwarden, netbird-client |

---

## Backup Module

The Backup module provides automated backup services using Proxmox Backup Server.

```mermaid
flowchart TB
    subgraph Capabilities
        BackupCap[Backup Capability]
    end

    subgraph Backup Module
        BackupComp[Backup Component]
        subgraph Sub-Components
            PBS[Proxmox Backup Server]
        end
        BackupService([VM Backup Service])
        BackupComp --> PBS
        BackupService -.->|provided by| BackupComp
    end

    BackupCap -.->|realized by| BackupComp
```

| Attribute | Value |
|-----------|-------|
| **Provides** | vm |
| **Depends On** | _(none)_ |
| **Consumed By** | identity, litellm, openwebui, vaultwarden, netbird-client, unifi |

---

## CICD Module

The CICD module (tappaas-cicd) provides automation and deployment management.

```mermaid
flowchart TB
    subgraph Capabilities
        Automation[Automation Capability]
        Deployment[Deployment Capability]
    end

    subgraph CICD Module
        CICDComp[CICD Component]
        subgraph Sub-Components
            Scripts[Automation Scripts]
            OPNController[OPNsense Controller]
        end
        CICDComp --> Scripts
        CICDComp --> OPNController
    end

    subgraph Cluster Module
        VMService([VM Service])
        HAService([HA Service])
    end

    Automation -.->|realized by| CICDComp
    Deployment -.->|realized by| CICDComp
    CICDComp -->|depends on| VMService
    CICDComp -->|depends on| HAService
```

| Attribute | Value |
|-----------|-------|
| **Provides** | _(none)_ |
| **Depends On** | cluster:vm, cluster:ha |
| **Consumed By** | _(orchestrates all modules)_ |
