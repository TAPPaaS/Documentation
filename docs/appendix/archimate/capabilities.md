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

## Platform Capability Overview

The following diagram shows TAPPaaS decomposed into its five capability stacks. The Foundation Stack provides the infrastructure that all other stacks depend on.

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title TAPPaaS Platform Capabilities

' TAPPaaS Platform
Strategy_Capability(capTAPPaaS, "TAPPaaS Platform")

' Five Stacks
Strategy_Capability(capFound, "Foundation Stack")
Strategy_Capability(capAI, "AI Stack")
Strategy_Capability(capProd, "Productivity Stack")
Strategy_Capability(capHome, "Home Stack")
Strategy_Capability(capDevOps, "DevOps Stack")

' TAPPaaS aggregates all stacks
Rel_Aggregation_Down(capTAPPaaS, capFound)
Rel_Aggregation_Down(capTAPPaaS, capAI)
Rel_Aggregation_Down(capTAPPaaS, capProd)
Rel_Aggregation_Down(capTAPPaaS, capHome)
Rel_Aggregation_Down(capTAPPaaS, capDevOps)

' All stacks depend on Foundation
Rel_Serving_Up(capFound, capAI)
Rel_Serving_Up(capFound, capProd)
Rel_Serving_Up(capFound, capHome)
Rel_Serving_Up(capFound, capDevOps)

@enduml
```

## Foundation Stack

The Foundation Stack provides the core infrastructure capabilities upon which all other stacks depend.

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title Foundation Stack Capabilities

' Foundation Stack
Strategy_Capability(capFound, "Foundation Stack")

' Infrastructure capabilities
Strategy_Capability(capInfra, "Infrastructure")
Strategy_Capability(capCluster, "Cluster")
Strategy_Capability(capNetwork, "Firewall/Networking")
Strategy_Capability(capBackup, "Backup Services")

' Platform capabilities
Strategy_Capability(capIdentity, "Identity Management")
Strategy_Capability(capProxy, "Web Proxy")
Strategy_Capability(capCICD, "CI/CD")

' Foundation aggregates Infrastructure and Platform capabilities
Rel_Aggregation_Down(capFound, capInfra)
Rel_Aggregation_Down(capFound, capIdentity)
Rel_Aggregation_Down(capFound, capProxy)
Rel_Aggregation_Down(capFound, capCICD)

' Infrastructure aggregates lower-level capabilities
Rel_Aggregation_Down(capInfra, capCluster)
Rel_Aggregation_Down(capInfra, capNetwork)
Rel_Aggregation_Down(capInfra, capBackup)

@enduml
```

| Capability | Description | Realized By |
|------------|-------------|-------------|
| Cluster | Hardware virtualization, clustering, and high availability | Proxmox VE |
| Firewall/Networking | Network security and routing | OPNsense |
| Backup Services | Data protection and restoration | ZFS Snapshots |
| Identity Management | Single sign-on and user management | Authentik |
| Web Proxy | TLS termination and reverse proxy | Caddy |
| CI/CD | Deployment automation and updates | TAPPaaS CICD |

## AI Stack

The AI Stack provides private AI capabilities for local large language models and chat interfaces.

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title AI Stack Capabilities

' AI Stack
Strategy_Capability(capAI, "AI Stack")

' AI capabilities
Strategy_Capability(capChat, "Chat Interface")
Strategy_Capability(capGateway, "Model Gateway")
Strategy_Capability(capInference, "On-prem AI")

' AI Stack aggregates
Rel_Aggregation_Down(capAI, capChat)
Rel_Aggregation_Down(capAI, capGateway)
Rel_Aggregation_Down(capAI, capInference)

' Dependencies
Rel_Serving_Right(capGateway, capChat)
Rel_Serving_Right(capInference, capGateway)

@enduml
```

| Capability | Description | Realized By |
|------------|-------------|-------------|
| Chat Interface | Web-based AI conversation interface | OpenWebUI |
| Model Gateway | Unified API for multiple AI providers | LiteLLM |
| On-prem AI | On-premise model execution | vLLM |

## Productivity Stack

The Productivity Stack provides business and personal productivity tools.

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title Productivity Stack Capabilities

' Productivity Stack
Strategy_Capability(capProd, "Productivity Stack")

' Productivity capabilities
Strategy_Capability(capFiles, "File Storage")
Strategy_Capability(capWorkflow, "Workflow Automation")
Strategy_Capability(capCollab, "Collaboration")
Strategy_Capability(capSecrets, "Secret Management")

' Productivity Stack aggregates
Rel_Aggregation_Down(capProd, capFiles)
Rel_Aggregation_Down(capProd, capWorkflow)
Rel_Aggregation_Down(capProd, capCollab)
Rel_Aggregation_Down(capProd, capSecrets)

@enduml
```

| Capability | Description | Realized By |
|------------|-------------|-------------|
| File Storage | Document storage and sharing | Nextcloud |
| Workflow Automation | Process automation and integrations | n8n |
| Collaboration | Team collaboration features | Nextcloud |
| Secret Management | Secure credential storage | Vaultwarden |

## Home Stack

The Home Stack provides home and family-oriented services.

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title Home Stack Capabilities

' Home Stack
Strategy_Capability(capHome, "Home Stack")

' Home capabilities
Strategy_Capability(capAutomate, "Home Automation")
Strategy_Capability(capMedia, "Media Streaming")

' Home Stack aggregates
Rel_Aggregation_Down(capHome, capAutomate)
Rel_Aggregation_Down(capHome, capMedia)

@enduml
```

| Capability | Description | Realized By |
|------------|-------------|-------------|
| Home Automation | Smart home control and automation | Home Assistant |
| Media Streaming | Media server and streaming | Jellyfin |

## DevOps Stack

The DevOps Stack provides software development and operations capabilities.

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title DevOps Stack Capabilities

' DevOps Stack
Strategy_Capability(capDevOps, "DevOps Stack")

' DevOps capabilities
Strategy_Capability(capRepo, "Code Repository")
Strategy_Capability(capPipeline, "CI/CD Pipelines")

' DevOps Stack aggregates
Rel_Aggregation_Down(capDevOps, capRepo)
Rel_Aggregation_Down(capDevOps, capPipeline)

@enduml
```

| Capability | Description | Realized By |
|------------|-------------|-------------|
| Code Repository | Source code management | Gitea |
| CI/CD Pipelines | Build and deployment automation | Woodpecker CI |
