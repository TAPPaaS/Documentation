---
title: TAPPaaS Capabilities
description: Platform capability model for TAPPaaS
---

# TAPPaaS Capabilities

This page describes the capability model for the TAPPaaS platform.

## Platform Capability Model

```kroki-plantuml
@startuml
title TAPPaaS Capability Model

package "Platform Capabilities" {
  package "AI Capabilities" {
    [Chat Interface] as chat
    [Model Gateway] as gateway
    [Local Inference] as inference
  }

  package "Productivity Capabilities" {
    [File Storage] as files
    [Workflow Automation] as workflow
    [Collaboration] as collab
  }

  package "Foundation Capabilities" {
    [Identity Management] as identity
    [Secret Management] as secrets
    [Certificate Management] as certs
  }
}

package "Infrastructure Capabilities" {
  [VM Provisioning] as vm
  [High Availability] as ha
  [Network Security] as network
  [Backup & Recovery] as backup
}

chat --> gateway : uses
gateway --> inference : routes to
files --> identity : authenticates
workflow --> identity : authenticates
vm --> ha : enables
network --> vm : protects
backup --> vm : protects

@enduml
```

## Capability Descriptions

### AI Capabilities

| Capability | Description | Realized By |
|------------|-------------|-------------|
| Chat Interface | Web-based AI conversation interface | OpenWebUI |
| Model Gateway | Unified API for multiple AI providers | LiteLLM |
| Local Inference | On-premise model execution | Ollama |

### Productivity Capabilities

| Capability | Description | Realized By |
|------------|-------------|-------------|
| File Storage | Document storage and sharing | Nextcloud |
| Workflow Automation | Process automation and integrations | n8n |
| Collaboration | Team collaboration features | Nextcloud |

### Foundation Capabilities

| Capability | Description | Realized By |
|------------|-------------|-------------|
| Identity Management | Single sign-on and user management | Authentik/Keycloak |
| Secret Management | Secure credential storage | Vaultwarden |
| Certificate Management | TLS certificate automation | Caddy |

### Infrastructure Capabilities

| Capability | Description | Realized By |
|------------|-------------|-------------|
| VM Provisioning | Virtual machine lifecycle management | TAPPaaS CICD |
| High Availability | Failover and redundancy | Proxmox HA + ZFS Replication |
| Network Security | Firewall and network segmentation | OPNsense |
| Backup & Recovery | Data protection and restoration | ZFS Snapshots |
