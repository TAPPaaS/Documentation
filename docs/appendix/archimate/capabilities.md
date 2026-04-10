---
title: TAPPaaS Capabilities
description: Platform capability model for TAPPaaS
---

# TAPPaaS Capabilities

This page describes the capability model for the TAPPaaS platform.

## Platform Capability Model

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title TAPPaaS Capability Model

' AI Stack Capabilities
Strategy_Capability(capAI, "AI Stack")
Strategy_Capability(capChat, "Chat Interface")
Strategy_Capability(capGateway, "Model Gateway")
Strategy_Capability(capInference, "Local Inference")

' Productivity Stack Capabilities
Strategy_Capability(capProd, "Productivity Stack")
Strategy_Capability(capFiles, "File Storage")
Strategy_Capability(capWorkflow, "Workflow Automation")
Strategy_Capability(capCollab, "Collaboration")

' Foundation Stack Capabilities
Strategy_Capability(capFound, "Foundation Stack")
Strategy_Capability(capIdentity, "Identity Management")
Strategy_Capability(capSecrets, "Secret Management")
Strategy_Capability(capCerts, "Certificate Management")

' Infrastructure Capabilities
Strategy_Capability(capInfra, "Infrastructure")
Strategy_Capability(capVM, "VM Provisioning")
Strategy_Capability(capHA, "High Availability")
Strategy_Capability(capNetwork, "Network Security")
Strategy_Capability(capBackup, "Backup & Recovery")

' Stack aggregates modules
Rel_Aggregation_Down(capAI, capChat)
Rel_Aggregation_Down(capAI, capGateway)
Rel_Aggregation_Down(capAI, capInference)

Rel_Aggregation_Down(capProd, capFiles)
Rel_Aggregation_Down(capProd, capWorkflow)
Rel_Aggregation_Down(capProd, capCollab)

Rel_Aggregation_Down(capFound, capIdentity)
Rel_Aggregation_Down(capFound, capSecrets)
Rel_Aggregation_Down(capFound, capCerts)

Rel_Aggregation_Down(capInfra, capVM)
Rel_Aggregation_Down(capInfra, capHA)
Rel_Aggregation_Down(capInfra, capNetwork)
Rel_Aggregation_Down(capInfra, capBackup)

' Dependencies
Rel_Serving_Right(capChat, capGateway)
Rel_Serving_Right(capGateway, capInference)
Rel_Serving_Right(capFiles, capIdentity)
Rel_Serving_Right(capWorkflow, capIdentity)

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
