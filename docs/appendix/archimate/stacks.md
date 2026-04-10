---
title: TAPPaaS Stacks
description: Technology stack diagrams for TAPPaaS
---

# TAPPaaS Stacks

This page contains architecture diagrams for the various TAPPaaS technology stacks.

## Foundation Stack

The foundation stack provides the core infrastructure services that all other modules depend on. The diagram shows the layered architecture from capabilities at the top, through services and applications, down to infrastructure nodes.

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title TAPPaaS Foundation Stack

' === STRATEGY LAYER (Capabilities) ===
Strategy_Capability(capFound, "Foundation Stack")
Strategy_Capability(capCluster, "Cluster")
Strategy_Capability(capNetwork, "Firewall/Networking")
Strategy_Capability(capIdentity, "Identity Management")
Strategy_Capability(capCICD, "CI/CD")
Strategy_Capability(capBackup, "Backup Services")
Strategy_Capability(capProxy, "Web Proxy")

' === APPLICATION LAYER (Services & Components) ===
' Application Services
Application_Service(clusterSvc, "Cluster Service")
Application_Service(networkSvc, "Network Service")
Application_Service(identitySvc, "Identity Service")
Application_Service(cicdSvc, "CI/CD Service")
Application_Service(backupSvc, "Backup Service")
Application_Service(proxySvc, "Proxy Service")

' Application Components (the actual software)
Application_Component(proxmox, "Proxmox VE")
Application_Component(opnsense, "OPNsense")
Application_Component(authentik, "Authentik")
Application_Component(cicdApp, "TAPPaaS CICD")
Application_Component(pbs, "Proxmox Backup Server")
Application_Component(caddy, "Caddy")

' === TECHNOLOGY LAYER (Infrastructure) ===
Technology_Node(node1, "tappaas1")
Technology_Node(node2, "tappaas2")
Technology_Node(node3, "tappaas3")

' Capability decomposition
Rel_Aggregation_Down(capFound, capCluster)
Rel_Aggregation_Down(capFound, capNetwork)
Rel_Aggregation_Down(capFound, capIdentity)
Rel_Aggregation_Down(capFound, capCICD)
Rel_Aggregation_Down(capFound, capBackup)
Rel_Aggregation_Down(capFound, capProxy)

' Capabilities realized by Services
Rel_Realization_Up(clusterSvc, capCluster)
Rel_Realization_Up(networkSvc, capNetwork)
Rel_Realization_Up(identitySvc, capIdentity)
Rel_Realization_Up(cicdSvc, capCICD)
Rel_Realization_Up(backupSvc, capBackup)
Rel_Realization_Up(proxySvc, capProxy)

' Services delivered by Components
Rel_Realization_Up(proxmox, clusterSvc)
Rel_Realization_Up(opnsense, networkSvc)
Rel_Realization_Up(authentik, identitySvc)
Rel_Realization_Up(cicdApp, cicdSvc)
Rel_Realization_Up(pbs, backupSvc)
Rel_Realization_Up(caddy, proxySvc)

' Components deployed on Infrastructure Nodes
Rel_Assignment_Up(node1, proxmox)
Rel_Assignment_Up(node2, proxmox)
Rel_Assignment_Up(node3, proxmox)

@enduml
```

## AI Stack

The AI stack provides artificial intelligence capabilities.

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title TAPPaaS AI Stack

' Business Actor
Business_Actor(user, "Platform User")

' Application Components (AI Services)
Application_Component(webui, "OpenWebUI")
Application_Component(litellm, "LiteLLM")
Application_Component(ollama, "Ollama")

' External Application Services
Application_Service(openai, "OpenAI API")
Application_Service(anthropic, "Anthropic API")

' Application Services exposed by components
Application_Service(chatSvc, "Chat Service")
Application_Service(routingSvc, "Model Routing")
Application_Service(inferenceSvc, "Local Inference")

' Components realize services
Rel_Realization(webui, chatSvc)
Rel_Realization(litellm, routingSvc)
Rel_Realization(ollama, inferenceSvc)

' User uses chat service
Rel_Serving(chatSvc, user)

' Service dependencies
Rel_Serving(routingSvc, webui)
Rel_Serving(inferenceSvc, litellm)
Rel_Serving(openai, litellm)
Rel_Serving(anthropic, litellm)

@enduml
```

### AI Components

| Component | Purpose | VM ID Range |
|-----------|---------|-------------|
| OpenWebUI | Chat interface | 310 |
| LiteLLM | Model gateway | 320 |
| Ollama | Local inference | 330 |

## Productivity Stack

The productivity stack provides collaboration and automation tools.

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title TAPPaaS Productivity Stack

' Business Actor
Business_Actor(user, "Platform User")

' Application Components
Application_Component(nextcloud, "Nextcloud")
Application_Component(n8n, "n8n")
Application_Component(vault, "Vaultwarden")

' Application Services
Application_Service(fileSvc, "File Storage")
Application_Service(workflowSvc, "Workflow Automation")
Application_Service(secretSvc, "Secret Management")

' Technology Artifacts (Data)
Technology_Artifact(files, "Files")
Technology_Artifact(db, "Database")

' Components realize services
Rel_Realization(nextcloud, fileSvc)
Rel_Realization(n8n, workflowSvc)
Rel_Realization(vault, secretSvc)

' User uses services
Rel_Serving(fileSvc, user)
Rel_Serving(workflowSvc, user)
Rel_Serving(secretSvc, user)

' Data access
Rel_Access(nextcloud, files)
Rel_Access(nextcloud, db)
Rel_Access(n8n, db)

@enduml
```

### Productivity Components

| Component | Purpose | VM ID Range |
|-----------|---------|-------------|
| Nextcloud | File storage | 610 |
| n8n | Workflow automation | 620 |
| Vaultwarden | Password management | 630 |

## Module Deployment Pattern

All TAPPaaS modules follow a consistent deployment pattern.

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title TAPPaaS Module Deployment Pattern

' Module artifacts
Technology_Artifact(config, "module.json")
Technology_Artifact(install, "install.sh")
Technology_Artifact(update, "update.sh")
Technology_Artifact(delete, "delete.sh")

' Infrastructure Technology Services
Technology_Service(vmSvc, "cluster:vm")
Technology_Service(haSvc, "cluster:ha")
Technology_Service(proxySvc, "firewall:proxy")

' Technology Node (VM)
Technology_Node(vm, "NixOS VM")

' Application running on VM
Application_Component(app, "Application")

' Backup
Technology_Service(snapshot, "ZFS Snapshot")

' Configuration flow
Rel_Association(config, install, "configures")

' Install uses VM service
Rel_Access(install, vmSvc, "provisions")

' VM service creates node
Rel_Realization(vmSvc, vm)

' Application assigned to VM
Rel_Assignment(vm, app)

' HA and proxy serve VM
Rel_Serving(haSvc, vm, "failover")
Rel_Serving(proxySvc, vm, "exposes")

' Snapshot protects VM
Rel_Serving(snapshot, vm, "protects")

@enduml
```
