---
title: Home Stack
description: >
  Home automation, its device gateways, and home media — Home Assistant and
  deCONZ today; Jellyfin and Immich planned.
---

# Home Stack

| Module | Role | Status |
|--------|------|--------|
| **[deCONZ](../../generated/apps/deconz.md)** | Zigbee gateway (ConBee) for sensors, switches and lights | Available |
| **[Home Assistant](../../generated/apps/hass.md)** | Home automation with local control — lights, heating, sensors, cameras | Available |
| **Jellyfin** | Media server — your movies, series and music, streamed locally | Planned — no module yet |
| **Immich** | Photo and video library — your pictures, indexed and searchable at home | Planned — no module yet |

Home Assistant runs as a sealed appliance VM in the home service zone. The device
gateways belong to this stack too, but **IoT devices remain separated at the network
layer**: they are the least-trusted citizens of a network, so they get their own zones
(local-only, cloud-dependent, cameras, untrusted) with firewall boundaries between them
and everything else — see [Network Zones](../../generated/zones.md). Home Assistant
reaches them across that boundary through controlled pinholes, and access from outside
is gated at the reverse-proxy layer.
