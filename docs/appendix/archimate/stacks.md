---
title: TAPPaaS Stacks
description: Technology stack diagrams for TAPPaaS
---

# TAPPaaS Stacks

This page contains architecture diagrams for the various TAPPaaS technology stacks.

## Foundation Stack

The foundation stack provides the core infrastructure services that all other modules depend on.

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title TAPPaaS Foundation Stack

' Technology Nodes (Physical/Virtual Infrastructure)
Technology_Node(node1, "tappaas1")
Technology_Node(node2, "tappaas2")
Technology_Node(node3, "tappaas3")

' Application Components (VMs running on nodes)
Application_Component(fw, "Firewall VM")
Application_Component(cicd, "CICD VM")

' Technology Services
Technology_Service(cluster, "Proxmox Cluster")
Technology_Service(ha, "HA Manager")
Technology_Service(zfs, "ZFS Replication")

' Nodes assigned to cluster
Rel_Assignment(node1, cluster)
Rel_Assignment(node2, cluster)
Rel_Assignment(node3, cluster)

' VMs deployed on node1
Rel_Assignment(node1, fw)
Rel_Assignment(node1, cicd)

' Cluster provides services
Rel_Aggregation(cluster, ha)
Rel_Aggregation(cluster, zfs)

' CICD manages cluster, Firewall protects it
Rel_Access(cicd, cluster, "manages")
Rel_Serving(fw, cluster, "protects")

@enduml
```

### Foundation Components

| Component | Purpose | VM ID Range |
|-----------|---------|-------------|
| Firewall | Network security and routing | 110 |
| CICD | Deployment automation | 120 |
| Identity | Single sign-on | 130 |
| Backup | Data protection | 140 |

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
