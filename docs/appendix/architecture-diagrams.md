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

```kroki-plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/Archimate-PlantUML/master/Archimate.puml

title TAPPaaS Platform Architecture Overview

' Business Layer
Business_Actor(user, "Platform User")
Business_Actor(admin, "Platform Administrator")
Business_Service(selfService, "Self-Service Platform")

' Application Layer
Application_Component(openwebui, "OpenWebUI")
Application_Component(litellm, "LiteLLM")
Application_Component(nextcloud, "Nextcloud")
Application_Component(n8n, "n8n Automation")
Application_Component(identity, "Identity Provider")
Application_Component(cicd, "TAPPaaS CICD")

' Technology Layer
Technology_Node(proxmox, "Proxmox Cluster")
Technology_Node(firewall, "OPNsense Firewall")
Technology_SystemSoftware(nixos, "NixOS VMs")
Technology_Artifact(zfs, "ZFS Storage")

' Relationships
Rel_Serving(selfService, user, "provides access")
Rel_Serving(selfService, admin, "provides management")
Rel_Realization(openwebui, selfService, "realizes")
Rel_Realization(nextcloud, selfService, "realizes")
Rel_Realization(n8n, selfService, "realizes")
Rel_Access(openwebui, litellm, "uses")
Rel_Access(openwebui, identity, "authenticates")
Rel_Access(nextcloud, identity, "authenticates")
Rel_Access(n8n, identity, "authenticates")
Rel_Composition(proxmox, nixos, "hosts")
Rel_Composition(proxmox, zfs, "includes")
Rel_Association(firewall, proxmox, "protects")
Rel_Triggering(cicd, nixos, "deploys")

@enduml
```

## Foundation Stack

```kroki-plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/Archimate-PlantUML/master/Archimate.puml

title TAPPaaS Foundation Stack

' Technology Layer - Infrastructure
Technology_Node(node1, "tappaas1\nProxmox Node")
Technology_Node(node2, "tappaas2\nProxmox Node")
Technology_Node(node3, "tappaas3\nProxmox Node")

Technology_Node(cluster, "Proxmox Cluster") {
    Technology_SystemSoftware(ha, "HA Manager")
    Technology_SystemSoftware(ceph, "Ceph/ZFS\nReplication")
}

Technology_Node(fwNode, "Firewall VM") {
    Technology_SystemSoftware(opnsense, "OPNsense")
    Technology_SystemSoftware(caddy, "Caddy Proxy")
}

Technology_Node(cicdNode, "CICD VM") {
    Technology_SystemSoftware(cicdSvc, "TAPPaaS CICD")
    Technology_Artifact(gitRepo, "Git Repository")
}

' Relationships
Rel_Composition(cluster, node1, "includes")
Rel_Composition(cluster, node2, "includes")
Rel_Composition(cluster, node3, "includes")
Rel_Assignment(node1, fwNode, "hosts")
Rel_Assignment(node1, cicdNode, "hosts")
Rel_Triggering(cicdSvc, cluster, "manages")
Rel_Access(opnsense, cluster, "protects")
Rel_Serving(caddy, opnsense, "reverse proxy")

@enduml
```

## Module Deployment Pattern

```kroki-plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/Archimate-PlantUML/master/Archimate.puml

title TAPPaaS Module Deployment Pattern

' Application Layer
Application_Component(module, "TAPPaaS Module")
Application_DataObject(moduleJson, "module.json\nConfiguration")
Application_Function(installScript, "install.sh")
Application_Function(updateScript, "update.sh")
Application_Function(deleteScript, "delete.sh")

' Technology Layer
Technology_Node(vm, "NixOS VM")
Technology_SystemSoftware(nixConfig, "NixOS Configuration")
Technology_Artifact(snapshot, "ZFS Snapshot")

' Infrastructure Services
Application_Service(clusterVM, "cluster:vm")
Application_Service(clusterHA, "cluster:ha")
Application_Service(fwProxy, "firewall:proxy")

' Relationships
Rel_Composition(module, moduleJson, "defines")
Rel_Composition(module, installScript, "includes")
Rel_Composition(module, updateScript, "includes")
Rel_Composition(module, deleteScript, "includes")
Rel_Realization(vm, module, "realizes")
Rel_Assignment(vm, nixConfig, "configured by")
Rel_Access(clusterVM, vm, "provisions")
Rel_Access(clusterHA, vm, "enables failover")
Rel_Access(fwProxy, vm, "exposes")
Rel_Association(snapshot, vm, "protects")

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
