---
title: Introduction
description: Overview of TAPPaaS Enterprise Architecture
---

# Introduction

This page provides an overview of the TAPPaaS platform architecture using enterprise architecture diagrams.

## TAPPaaS Architecture Overview

The following diagram illustrates the high-level TAPPaaS architecture, showing the relationship between users, applications, and infrastructure.

```kroki-plantuml
@startuml
title TAPPaaS Platform Architecture Overview

package "Users" {
  actor "Platform User" as user
  actor "Administrator" as admin
}

package "Application Layer" {
  [OpenWebUI] as openwebui
  [LiteLLM] as litellm
  [Nextcloud] as nextcloud
  [Identity Provider] as identity
}

package "Infrastructure Layer" {
  [Proxmox Cluster] as proxmox
  [OPNsense Firewall] as firewall
}

user --> openwebui : uses
user --> nextcloud : uses
admin --> proxmox : manages
openwebui --> litellm : API calls
openwebui --> identity : authenticates
nextcloud --> identity : authenticates
firewall --> proxmox : protects

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

Represents the business actors and services:

- **Platform Users** - End users consuming platform services
- **Administrators** - Operators managing the platform

### Application Layer

The software components providing functionality:

- **AI Services** - OpenWebUI, LiteLLM, Ollama
- **Productivity** - Nextcloud, n8n
- **Identity** - Single sign-on and authentication

### Technology Layer

The underlying infrastructure:

- **Compute** - Proxmox virtualization cluster
- **Network** - OPNsense firewall and Caddy reverse proxy
- **Storage** - ZFS with replication
