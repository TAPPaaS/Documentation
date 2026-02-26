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
        PVE[Proxmox Virtual Environment]
        VMService([VM Service])
        HAService([HA Service])
        VMService -.->|provided by| PVE
        HAService -.->|provided by| PVE
    end

    Compute -.->|realized by| PVE
    HA -.->|realized by| PVE
```

### Design considerations

*To be documented.*

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
        OPNsense[OPNsense]
        subgraph Sub-Components
            Rules[Rules]
            DNS[DNS]
            DHCP[DHCP]
            VLANs[VLANs]
            Caddy[Caddy]
        end
        FirewallService([Firewall Service])
        ProxyService([Proxy Service])
        OPNsense --> Rules
        OPNsense --> DNS
        OPNsense --> DHCP
        OPNsense --> VLANs
        OPNsense --> Caddy
        FirewallService -.->|provided by| OPNsense
        ProxyService -.->|provided by| Caddy
    end

    subgraph Cluster Module
        VMService([VM Service])
        HAService([HA Service])
    end

    Network -.->|realized by| OPNsense
    Proxy -.->|realized by| Caddy
    OPNsense -->|depends on| VMService
    OPNsense -->|depends on| HAService
```

### Design considerations

*To be documented.*

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
        Authentik[Authentik]
        IdentityService([Identity Service])
        AccessService([Access Control Service])
        IdentityService -.->|provided by| Authentik
        AccessService -.->|provided by| Authentik
    end

    subgraph Dependencies
        VMService([VM Service])
        HAService([HA Service])
        NixOSService([NixOS Service])
        BackupService([Backup Service])
        ProxyService([Proxy Service])
    end

    Auth -.->|realized by| Authentik
    Access -.->|realized by| Authentik
    Authentik -->|depends on| VMService
    Authentik -->|depends on| HAService
    Authentik -->|depends on| NixOSService
    Authentik -->|depends on| BackupService
    Authentik -->|depends on| ProxyService
```

### Design considerations

*To be documented.*

---

## Backup Module

The Backup module provides automated backup services using Proxmox Backup Server.

```mermaid
flowchart TB
    subgraph Capabilities
        BackupCap[Backup Capability]
    end

    subgraph Backup Module
        PBS[Proxmox Backup Server]
        BackupService([VM Backup Service])
        BackupService -.->|provided by| PBS
    end

    BackupCap -.->|realized by| PBS
```

### Design considerations

*To be documented.*

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

### Design considerations

*To be documented.*
