---
title: Home Stack
description: >
  Home automation with local control — Home Assistant, with deCONZ for Zigbee.
---

# Home Stack

| Module | Role | Status |
|--------|------|--------|
| **[Home Assistant](../../generated/apps/hass.md)** | Home automation with local control — lights, heating, sensors, cameras | Available |
| **[deCONZ](../../generated/apps/deconz.md)** | Zigbee gateway (ConBee) for sensors, switches and lights — pairs with Home Assistant | Available (Development) |

Home Assistant runs as a sealed appliance VM in the home service zone; IoT devices
live in the separated IoT zones with firewall boundaries between them — see
[Network Zones](../../generated/zones.md) for the zone model. Access from outside is
gated at the reverse-proxy layer.
