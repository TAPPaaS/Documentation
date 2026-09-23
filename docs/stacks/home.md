---
title: Home Stack
description: Home automation and the device gateways it drives; home media planned.
---

# Home Stack

| Module | Role |
|--------|------|
| [Home Assistant](../generated/modules/hass.md) | Home automation with local control |
| [deCONZ](../generated/modules/deconz.md) | Zigbee gateway (ConBee) for sensors, switches and lights |
| Jellyfin | Media server *(planned — no module yet)* |
| Immich | Photo and video library *(planned — no module yet)* |

Device gateways are part of this stack — but **IoT devices are still separated at the
network layer**, which is a different thing from the stack they belong to. They get
their own zones (local-only, cloud-dependent, cameras, untrusted) with firewall
boundaries, and Home Assistant reaches them across those boundaries through controlled
pinholes — see [Network Zones](../generated/zones.md).

Install guides under [Install → Add Stacks](../install/home-stack/index.md).
