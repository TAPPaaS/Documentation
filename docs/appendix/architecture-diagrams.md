---
title: Architecture Diagrams
description: Enterprise Architecture diagrams for TAPPaaS using ArchiMate notation
---

# Architecture Diagrams

This page contains Enterprise Architecture diagrams for TAPPaaS, rendered using [ArchiMate](https://www.opengroup.org/archimate-forum/archimate-overview) notation.

## About ArchiMate

ArchiMate is an open and independent enterprise architecture modeling language supported by The Open Group. It provides a uniform representation for describing, analyzing, and visualizing architecture within and across business domains.

## Diagram Rendering

The diagrams on this page are created using [PlantUML with ArchiMate support](https://github.com/plantuml-stdlib/Archimate-PlantUML) and rendered via the Kroki service.

## TAPPaaS Architecture Overview

The following diagrams illustrate the TAPPaaS architecture using standard component diagrams. Full ArchiMate notation will be added once the diagram rendering infrastructure is validated.

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

## Foundation Stack

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

## Module Deployment Pattern

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

## Creating New Diagrams

To add new ArchiMate diagrams:

1. Use PlantUML syntax with the ArchiMate include
2. Wrap the diagram in a `kroki-plantuml` code fence
3. Reference the ArchiMate library from the PlantUML stdlib

### ArchiMate Elements Reference

| Layer | Elements |
|-------|----------|
| **Business** | `Business_Actor`, `Business_Role`, `Business_Process`, `Business_Service`, `Business_Object` |
| **Application** | `Application_Component`, `Application_Service`, `Application_Function`, `Application_DataObject` |
| **Technology** | `Technology_Node`, `Technology_Device`, `Technology_SystemSoftware`, `Technology_Artifact`, `Technology_Path` |
| **Strategy** | `Strategy_Resource`, `Strategy_Capability`, `Strategy_Course_Of_Action` |

### ArchiMate Relationships Reference

| Relationship | Syntax |
|-------------|--------|
| Composition | `Rel_Composition(from, to, "label")` |
| Aggregation | `Rel_Aggregation(from, to, "label")` |
| Assignment | `Rel_Assignment(from, to, "label")` |
| Realization | `Rel_Realization(from, to, "label")` |
| Serving | `Rel_Serving(from, to, "label")` |
| Access | `Rel_Access(from, to, "label")` |
| Triggering | `Rel_Triggering(from, to, "label")` |
| Flow | `Rel_Flow(from, to, "label")` |
| Association | `Rel_Association(from, to, "label")` |

For complete documentation, see the [Archimate-PlantUML reference](https://github.com/plantuml-stdlib/Archimate-PlantUML).
