---
title: IoT Stack
description: >
  The device side of your smart home — Zigbee and other IoT gateways, isolated
  in their own network zones.
---

# IoT Stack

| Module | Role | Status |
|--------|------|--------|
| **[deCONZ](../../generated/apps/deconz.md)** | Zigbee gateway (ConBee) for sensors, switches and lights — pairs with Home Assistant | Available (Development) |

IoT devices are the least-trusted citizens of a network, so TAPPaaS gives them their
own **separated IoT zones** (local-only, cloud-dependent, cameras, untrusted) with
firewall boundaries between them and everything else — see
[Network Zones](../../generated/zones.md). The [Home Stack](../home-stack/index.md)
(Home Assistant) consumes these devices across the zone boundary through controlled
firewall pinholes.
