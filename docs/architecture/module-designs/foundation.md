---
title: Foundation Stack
description: >
  The modules the platform itself is made of — cluster, network, templates,
  automation, backup, identity, logging, satellite.
---

# Foundation Stack

The foundation is what makes TAPPaaS a *platform* rather than a pile of VMs. Like
everything else it is built from modules — see the
[Module Model](../solution-design/index.md); here is the module catalog:

| Module | Role |
|--------|------|
| [Cluster](../../generated/foundation/cluster.md) | Proxmox nodes, storage pools, HA — the ground everything stands on |
| [Network](../../generated/foundation/network.md) | OPNsense firewall: zones, DNS, DHCP, reverse proxy, rules |
| [Templates](../../generated/foundation/templates.md) | The prebuilt VM templates modules deploy from |
| [TAPPaaS CICD](../../generated/foundation/tappaas-cicd.md) | The mothership: managers and controllers that run the platform |
| [Backup](../../generated/foundation/backup.md) | Proxmox Backup Server: scheduled, verified, off-site capable |
| [Identity](../../generated/foundation/identity.md) | Authentik: SSO, users, groups, organisations |
| [Logging](../../generated/foundation/logging.md) | Loki / Grafana / Promtail: central logs |
| [Satellite](../../generated/foundation/satellite.md) | Optional VPS: public ingress, off-site backup, admin VPN |

## Architecture view

The layered ArchiMate view — capabilities at the top, through services and the
realizing components, down to the cluster nodes:

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title TAPPaaS Foundation Stack

' === STRATEGY LAYER (Capabilities) ===
Strategy_Capability(capFound, "Foundation Stack")
Strategy_Capability(capBackup, "Backup Services")
Strategy_Capability(capCluster, "Cluster")
Strategy_Capability(capFirewall, "Firewall")
Strategy_Capability(capProxy, "Web Proxy")
Strategy_Capability(capIdentity, "Identity Management")
Strategy_Capability(capCICD, "CI/CD")

' === APPLICATION LAYER (Services & Components) ===
' Application Services
Application_Service(backupSvc, "Backup Service")
Application_Service(vmSvc, "VM Service")
Application_Service(haSvc, "HA Service")
Application_Service(zoneSvc, "Zone Service")
Application_Service(firewallSvc, "Firewall Service")
Application_Service(routingSvc, "Routing Service")
Application_Service(proxySvc, "Proxy Service")
Application_Service(identitySvc, "Identity Service")
Application_Service(cicdSvc, "CI/CD Service")

' Application Components (the actual software)
Application_Component(pbs, "Proxmox Backup Server")
Application_Component(proxmox, "Proxmox VE")
Application_Component(opnsense, "OPNsense")
Application_Component(caddy, "Caddy")
Application_Component(authentik, "Authentik")
Application_Component(cicdApp, "TAPPaaS CICD")

' Caddy is a component of OPNsense
Rel_Composition(opnsense, caddy)

' === TECHNOLOGY LAYER (Infrastructure) ===
Technology_Node(node1, "tappaas1")
Technology_Node(node2, "tappaas2")
Technology_Node(node3, "tappaas3")

' Capability decomposition
Rel_Aggregation_Down(capFound, capBackup)
Rel_Aggregation_Down(capFound, capCluster)
Rel_Aggregation_Down(capFound, capFirewall)
Rel_Aggregation_Down(capFound, capProxy)
Rel_Aggregation_Down(capFound, capIdentity)
Rel_Aggregation_Down(capFound, capCICD)

' Capabilities realized by Services
Rel_Realization_Up(backupSvc, capBackup)
Rel_Realization_Up(vmSvc, capCluster)
Rel_Realization_Up(haSvc, capCluster)
Rel_Realization_Up(zoneSvc, capFirewall)
Rel_Realization_Up(firewallSvc, capFirewall)
Rel_Realization_Up(routingSvc, capFirewall)
Rel_Realization_Up(proxySvc, capProxy)
Rel_Realization_Up(identitySvc, capIdentity)
Rel_Realization_Up(cicdSvc, capCICD)

' Services delivered by Components
Rel_Realization_Up(pbs, backupSvc)
Rel_Realization_Up(proxmox, vmSvc)
Rel_Realization_Up(proxmox, haSvc)
Rel_Realization_Up(opnsense, zoneSvc)
Rel_Realization_Up(opnsense, firewallSvc)
Rel_Realization_Up(opnsense, routingSvc)
Rel_Realization_Up(caddy, proxySvc)
Rel_Realization_Up(authentik, identitySvc)
Rel_Realization_Up(cicdApp, cicdSvc)

' Components deployed on Infrastructure Nodes
Rel_Assignment_Up(node1, proxmox)
Rel_Assignment_Up(node2, proxmox)
Rel_Assignment_Up(node3, proxmox)
Rel_Assignment_Up(node3, pbs)

@enduml
```
