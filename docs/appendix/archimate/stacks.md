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
title TAPPaaS Foundation Stack

node "tappaas1" as node1 {
  [Firewall VM] as fw
  [CICD VM] as cicd
}

node "tappaas2" as node2
node "tappaas3" as node3

cloud "Proxmox Cluster" as cluster {
  [HA Manager] as ha
  [ZFS Replication] as zfs
}

node1 --> cluster
node2 --> cluster
node3 --> cluster
cicd --> cluster : manages
fw --> cluster : protects

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
title TAPPaaS AI Stack

actor User

package "AI Services" {
  [OpenWebUI] as webui
  [LiteLLM] as litellm
  [Ollama] as ollama
}

cloud "External AI" {
  [OpenAI API] as openai
  [Anthropic API] as anthropic
}

User --> webui : chat
webui --> litellm : API requests
litellm --> ollama : local models
litellm --> openai : cloud models
litellm --> anthropic : cloud models

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
title TAPPaaS Productivity Stack

actor User

package "Productivity Services" {
  [Nextcloud] as nextcloud
  [n8n] as n8n
  [Vaultwarden] as vault
}

database "Storage" {
  [Files] as files
  [Database] as db
}

User --> nextcloud : files & docs
User --> n8n : automation
User --> vault : passwords
nextcloud --> files
nextcloud --> db
n8n --> db

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
title TAPPaaS Module Deployment Pattern

package "TAPPaaS Module" {
  [module.json] as config
  [install.sh] as install
  [update.sh] as update
  [delete.sh] as delete
}

package "Infrastructure Services" {
  [cluster:vm] as vm_svc
  [cluster:ha] as ha_svc
  [firewall:proxy] as proxy_svc
}

node "NixOS VM" as vm {
  [Application] as app
}

database "ZFS Snapshot" as snapshot

config --> install : configures
install --> vm_svc : provisions VM
vm_svc --> vm : creates
ha_svc --> vm : enables failover
proxy_svc --> vm : exposes
snapshot --> vm : protects

@enduml
```
