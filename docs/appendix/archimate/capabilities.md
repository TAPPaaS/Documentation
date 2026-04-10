---
title: TAPPaaS Capabilities
description: Platform capability model for TAPPaaS
---

# TAPPaaS Capabilities

This page describes the capability model for the TAPPaaS platform. TAPPaaS delivers capabilities through five primary stacks, with the Foundation Stack providing the infrastructure upon which all other stacks depend.

## TAPPaaS Stacks

TAPPaaS organizes capabilities into the following stacks:

| Stack | Description |
|-------|-------------|
| **Foundation Stack** | The infrastructure layer providing virtualization, networking, storage, security, backup, and identity management upon which all other stacks depend |
| **AI Stack** | Private AI capabilities including local large language models, chat interfaces, and AI-powered automation workflows |
| **Productivity Stack** | Business and personal productivity tools including file sharing, workflow automation, and collaboration services |
| **Home Stack** | Home and family-oriented services such as home automation, media streaming, and personal data management |
| **DevOps Stack** | Software development and operations capabilities including CI/CD pipelines, code repositories, and deployment automation |

!!! note
    More stacks are planned and not all of the above are fully implemented yet. TAPPaaS also allows any community or private modules to be deployed.

## Platform Capability Model

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title TAPPaaS Capability Model

' Foundation Stack Capabilities
Strategy_Capability(capFound, "Foundation Stack")
Strategy_Capability(capCluster, "HW Virtualization")
Strategy_Capability(capNetwork, "Firewall/Networking")
Strategy_Capability(capIdentity, "Identity Management")
Strategy_Capability(capCICD, "CI/CD")
Strategy_Capability(capBackup, "Backup Services")

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

' Home Stack Capabilities
Strategy_Capability(capHome, "Home Stack")
Strategy_Capability(capAutomate, "Home Automation")
Strategy_Capability(capMedia, "Media Streaming")

' DevOps Stack Capabilities
Strategy_Capability(capDevOps, "DevOps Stack")
Strategy_Capability(capRepo, "Code Repository")
Strategy_Capability(capPipeline, "CI/CD Pipelines")

' Foundation Stack aggregates
Rel_Aggregation_Down(capFound, capCluster)
Rel_Aggregation_Down(capFound, capNetwork)
Rel_Aggregation_Down(capFound, capIdentity)
Rel_Aggregation_Down(capFound, capCICD)
Rel_Aggregation_Down(capFound, capBackup)

' AI Stack aggregates
Rel_Aggregation_Down(capAI, capChat)
Rel_Aggregation_Down(capAI, capGateway)
Rel_Aggregation_Down(capAI, capInference)

' Productivity Stack aggregates
Rel_Aggregation_Down(capProd, capFiles)
Rel_Aggregation_Down(capProd, capWorkflow)
Rel_Aggregation_Down(capProd, capCollab)

' Home Stack aggregates
Rel_Aggregation_Down(capHome, capAutomate)
Rel_Aggregation_Down(capHome, capMedia)

' DevOps Stack aggregates
Rel_Aggregation_Down(capDevOps, capRepo)
Rel_Aggregation_Down(capDevOps, capPipeline)

' Dependencies on Foundation
Rel_Serving_Up(capFound, capAI)
Rel_Serving_Up(capFound, capProd)
Rel_Serving_Up(capFound, capHome)
Rel_Serving_Up(capFound, capDevOps)

@enduml
```

## Capability Descriptions

### Foundation Stack

| Capability | Description | Realized By |
|------------|-------------|-------------|
| HW Virtualization | Hardware virtualization and clustering | Proxmox VE |
| Firewall/Networking | Network security and routing | OPNsense |
| Identity Management | Single sign-on and user management | Authentik |
| CI/CD | Deployment automation and updates | TAPPaaS CICD |
| Backup Services | Data protection and restoration | ZFS Snapshots |

### AI Stack

| Capability | Description | Realized By |
|------------|-------------|-------------|
| Chat Interface | Web-based AI conversation interface | OpenWebUI |
| Model Gateway | Unified API for multiple AI providers | LiteLLM |
| Local Inference | On-premise model execution | Ollama |

### Productivity Stack

| Capability | Description | Realized By |
|------------|-------------|-------------|
| File Storage | Document storage and sharing | Nextcloud |
| Workflow Automation | Process automation and integrations | n8n |
| Collaboration | Team collaboration features | Nextcloud |

### Home Stack

| Capability | Description | Realized By |
|------------|-------------|-------------|
| Home Automation | Smart home control and automation | Home Assistant |
| Media Streaming | Media server and streaming | Jellyfin |

### DevOps Stack

| Capability | Description | Realized By |
|------------|-------------|-------------|
| Code Repository | Source code management | Gitea |
| CI/CD Pipelines | Build and deployment automation | Woodpecker CI |
