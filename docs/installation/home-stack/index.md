---
title: Home Stack
description: >
  Home automation and home media — Home Assistant today; Jellyfin and Immich
  planned.
---

# Home Stack

| Module | Role | Status |
|--------|------|--------|
| **[Home Assistant](../../generated/apps/hass.md)** | Home automation with local control — lights, heating, sensors, cameras | Available |
| **Jellyfin** | Media server — your movies, series and music, streamed locally | Planned — no module yet |
| **Immich** | Photo and video library — your pictures, indexed and searchable at home | Planned — no module yet |

Home Assistant runs as a sealed appliance VM in the home service zone; IoT devices
live in the separated IoT zones — see the [IoT Stack](../iot-stack/index.md) for the
device-side modules and [Network Zones](../../generated/zones.md) for the zone model.
Access from outside is gated at the reverse-proxy layer.
