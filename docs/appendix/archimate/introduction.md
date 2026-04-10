---
title: Introduction
description: Overview of TAPPaaS Enterprise Architecture
---

# Introduction

This page provides an overview of the TAPPaaS platform architecture using enterprise architecture diagrams.

## TAPPaaS to ArchiMate Concept Mapping

The following table maps TAPPaaS concepts to their corresponding ArchiMate elements:

| TAPPaaS Concept | ArchiMate Element | Description |
|-----------------|-------------------|-------------|
| **Stack** | Capability | A TAPPaaS Stack (e.g., AI Stack, Productivity Stack) implements a business Capability |
| **Module** | Capability | A Module implements a more detailed Capability within a Stack |
| **Module Implementation** | Application Component | A Module is realized by one or more Application Components (the actual software) |
| **Service** | Application Service | A Module delivers Services that can be consumed by other modules or users |
| **VM** | Technology Node | Each module runs on a NixOS VM, modeled as a Technology Node |
| **Infrastructure Service** | Technology Service | Services like `cluster:vm`, `cluster:ha`, `firewall:proxy` are Technology Services |
| **User** | Business Actor | Platform users and administrators are Business Actors |
| **Proxmox Cluster** | Technology Node | The underlying virtualization infrastructure |
| **OPNsense Firewall** | Technology Node | Network security infrastructure |

### Relationship Patterns

| TAPPaaS Relationship | ArchiMate Relationship | Example |
|---------------------|------------------------|---------|
| Stack contains Modules | Aggregation | AI Stack aggregates OpenWebUI, LiteLLM, Ollama |
| Module realizes Capability | Realization | OpenWebUI module realizes "Chat Interface" capability |
| Module uses Service | Serving | OpenWebUI uses Identity service for authentication |
| Module depends on Module | Access | OpenWebUI accesses LiteLLM for model routing |
| VM hosts Application | Assignment | NixOS VM is assigned to run the application |
| Infrastructure provides Service | Serving | Proxmox cluster serves VM provisioning |

## TAPPaaS Architecture Overview

The following diagram illustrates the high-level TAPPaaS architecture, showing the relationship between users, applications, and infrastructure.

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title TAPPaaS Platform Architecture Overview

' Business Actors
Business_Actor(user, "Platform User")
Business_Actor(admin, "Administrator")

' Application Components
Application_Component(openwebui, "OpenWebUI")
Application_Component(litellm, "LiteLLM")
Application_Component(nextcloud, "Nextcloud")
Application_Component(identity, "Identity Provider")

' Technology Nodes
Technology_Node(proxmox, "Proxmox Cluster")
Technology_Node(firewall, "OPNsense Firewall")

' Application Services
Application_Service(chatSvc, "Chat Service")
Application_Service(fileSvc, "File Service")
Application_Service(authSvc, "Auth Service")

' Components realize services
Rel_Realization(openwebui, chatSvc)
Rel_Realization(nextcloud, fileSvc)
Rel_Realization(identity, authSvc)

' Users access services
Rel_Serving(chatSvc, user)
Rel_Serving(fileSvc, user)

' Admin manages infrastructure
Rel_Access(admin, proxmox, "manages")

' Application dependencies
Rel_Serving(litellm, openwebui, "API")
Rel_Serving(authSvc, openwebui)
Rel_Serving(authSvc, nextcloud)

' Infrastructure relationships
Rel_Serving(firewall, proxmox, "protects")

@enduml
```

## Key Architectural Principles

TAPPaaS follows these core architectural principles:

1. **Self-Hosted** - All services run on your own infrastructure
2. **Modular** - Components can be installed independently
3. **Automated** - CICD-driven deployment and updates
4. **Resilient** - High availability through clustering and replication
5. **Secure** - Defense in depth with firewall, SSO, and network segmentation

## Architecture Layers

### Business Layer

Represents the business actors:

- **Platform Users** - End users consuming platform services
- **Administrators** - Operators managing the platform

### Strategy Layer

The capabilities provided by TAPPaaS, organized into stacks and modules:

- **AI Stack** - Chat Interface, Model Gateway, Local Inference
- **Productivity Stack** - File Storage, Workflow Automation, Collaboration
- **Foundation Stack** - Identity Management, Secret Management, Certificate Management
- **Infrastructure** - VM Provisioning, High Availability, Network Security, Backup & Recovery

### Application Layer

The software components (applications) that realize the capabilities:

- **AI Applications** - OpenWebUI, LiteLLM, Ollama
- **Productivity Applications** - Nextcloud, n8n, Vaultwarden
- **Identity Applications** - Authentik (realizes Identity Management capability)

### Technology Layer

The underlying infrastructure:

- **Compute** - Proxmox virtualization cluster
- **Network** - OPNsense firewall and Caddy reverse proxy
- **Storage** - ZFS with replication
