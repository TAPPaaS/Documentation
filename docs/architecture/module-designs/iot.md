---
title: IoT Stack
description: Device gateways, isolated in their own network zones.
---

# IoT Stack

| Module | Role |
|--------|------|
| [deCONZ](../../generated/modules/deconz.md) | Zigbee gateway (ConBee) for sensors, switches and lights |

IoT devices get their own separated zones (local-only, cloud-dependent, cameras,
untrusted) with firewall boundaries — see [Network Zones](../../generated/zones.md).
The [Home Stack](home.md) consumes these devices through controlled pinholes.
