---
title: Home Stack
description: Deploy home automation with Home Assistant
---

# Home Stack

The TAPPaaS Home Stack provides home automation capabilities through Home Assistant, allowing you to control and automate your smart home devices.

## Components

| Component | Purpose |
|-----------|---------|
| **Home Assistant** | Central home automation platform |

## Overview

Home Assistant is a powerful open-source home automation platform that:

- Integrates with 2000+ devices and services
- Runs locally for privacy and reliability
- Provides powerful automation capabilities
- Works offline without cloud dependencies

## Prerequisites

- [ ] [Foundation](../foundation/index.md) complete
- [ ] VLAN configured for IoT devices (recommended)
- [ ] Compatible smart home devices

## System Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| vCPU | 2 | 4 |
| RAM | 2 GB | 4 GB |
| Storage | 32 GB | 64 GB |

## Network Considerations

### IoT VLAN

For security, place IoT devices on a separate VLAN:

| VLAN | Network | Purpose |
|------|---------|---------|
| 200 | 10.2.0.0/24 | IoT devices |

Configure firewall rules to:

- Allow Home Assistant to communicate with IoT VLAN
- Block IoT devices from accessing management network
- Allow specific internet access as needed

### Device Discovery

Home Assistant uses mDNS for device discovery. Ensure:

- mDNS/Avahi traffic allowed between VLANs
- Or configure devices manually

## Supported Devices

Home Assistant supports thousands of integrations including:

### Lighting

- Philips Hue
- LIFX
- Zigbee bulbs
- Z-Wave switches

### Climate

- Nest
- Ecobee
- Generic thermostats
- HVAC systems

### Security

- Ring
- Arlo
- Generic cameras
- Door/window sensors

### Voice Assistants

- Amazon Alexa
- Google Home
- Apple HomeKit

## Installation

<div class="grid cards" markdown>

-   :material-home-automation: **[Home Assistant](home-assistant.md)**

    ---

    Deploy Home Assistant Operating System on TAPPaaS

</div>

## Integration with TAPPaaS

Home Assistant integrates with other TAPPaaS components:

| Integration | Use Case |
|-------------|----------|
| n8n | Complex automation workflows |
| LiteLLM | Voice commands with local AI |
| Authentik | User authentication |
| VaultWarden | Secure API key storage |

## Security Considerations

- Isolate IoT devices on dedicated VLAN
- Use strong passwords for all devices
- Regularly update firmware
- Limit cloud integrations
- Review automation rules
