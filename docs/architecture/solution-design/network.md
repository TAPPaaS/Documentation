---
title: Network
description: TAPPaaS network design and topology
---

# Network Design

## Introduction

There are a number of parts to the TAPPaaS network design:

- The local TAPPaaS network topology, managed as a VLAN overlay network
- The firewall and router: manage the routing and traffic control between elements of the TAPPaaS network topology as well as the access to and from the Internet
- The switching infrastructure: In very small TAPPaaS installations the switching is purely virtual but in most cases there is both virtual switching in the virtualization nodes and physical switching equipment
- IP number allocations
- The WiFi access points (AP): TAPPaaS makes suggestions for what needs to be configured
- The Network services: DNS, DHCP
- The connectivity proxies
- The network monitoring

We recognize that for some it will make sense to reuse existing firewall, switching and WiFi access points, in which case TAPPaaS just makes recommendations for how those components are configured. But in the ideal case TAPPaaS controls all of this infrastructure.

---

## Network Topology

Moving to a self-hosted setup introduces a number of security challenges, and to deal with this we are segmenting TAPPaaS. The cost of segmentation is more challenges in connecting the relevant components together, and secondly a lot of "internal" traffic will now need to be routed between networks.

In the TAPPaaS design we are trying to reach a balance between simplicity and security, but we are leaning towards security more than simplicity.

### Network Zones

| Segment | Description |
|---------|-------------|
| **srv** | Where all services for a business or reside (OpenWebUI, NextCloud, etc.). There can be several "srv" Zones in a TAPPaaS setup. |
| **IoT** | Where all IoT equipment lives. IoT is generally considered more insecure. "srv" can access IoT, but not the other way around. |
| **Mgmt** | Management section for self-management of TAPPaaS. Generally the management segment can connect to everything (except Guest). |
| **DMZ** | Demilitarized Zone - the only place traffic from the internet can enter. It is a reverse tunnel proxy that cannot access anything else in TAPPaaS. |
| **Client** | Where end users of the system resides. as with srv there can be several separate Client zones (employees, guests, contractors, homeusers)

---

## IP and VLAN Assignments

TAPPaaS supports IPv4 and IPv6. In the ideal world, the TAPPaaS system plugs into an Internet connection that provides one public IPv4 and at least a /54 IPv6 range. TAPPaaS can function without IPv6 connectivity and with no public IPv4.

For IPv4, TAPPaaS does NAT translation to an internal 10.0.0.0/8 network.

Each network segment has its own IP sub-range and traffic is tagged with VLAN tags when sent through the switching infrastructure. TAPPaaS uses a 3-digit tag where the first digit indicates the type of VLAN traffic.

| Segment | VLAN | IPv4 Subnet | Description |
|---------|------|-------------|-------------|
| Management | none | 10.0.0.0/24 | Untagged traffic is considered management traffic |
| DMZ | 100 | 10.1.0.0/24 | Demilitarized zone |
| Service | 200 | 10.2.0.0/24 | Where services for consumption live |
| Client | 300 | 10.3.0.0/24 | Unconnected client network |
| IoT | 400 | 10.4.0.0/24 | Unsecure devices and systems |


## DNS and DHCP

We generally allocate IP numnbers through DHCP and use maskarading DNS to make all resources in TAPPaaS accesible under: <device/vm name>.<Zone>.internal

## Proxy

TAPPaaS comes with a Proxy service that will ensure https termination using public certificate and do routing to right service based on http header

## Best Practices

- Place media devices (TVs, set-top boxes, smart speakers) in the IoT VLAN
- This isolates less-trusted consumer devices from user devices and critical infrastructure
- Use mDNS/SSDP relays or firewall rules to allow casting and streaming from user VLANs if needed

## TODO

document IPv6 allocaiton