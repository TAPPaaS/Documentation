---
title: Home Assistant
description: Deploy Home Assistant for home automation
---

# Home Assistant

Home Assistant Operating System (HAOS) provides a complete home automation platform with supervisor, add-ons, and easy management.

## Features

- 2000+ integrations
- Powerful automations
- Add-on ecosystem
- Mobile apps
- Voice assistant support
- Local processing

## Prerequisites

- [ ] [Foundation](../foundation/index.md) complete
- [ ] VLAN 200 configured for srv (recommended)
- [ ] DNS record (optional)

## System Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| vCPU | 2 | 4 |
| RAM | 2 GB | 4 GB |
| Storage | 32 GB | 64 GB |

## Installation

**TODO create, update and test**



## Initial Setup

### Access Web Interface

Navigate to:

```
http://homeassistant.<mydoamin>
```


### Create Account

1. Create owner account
2. Set home location
3. Configure basic settings

### Enable Advanced Mode

For full functionality:

1. Click your profile (bottom left)
2. Enable **Advanced Mode**

## Add-ons

### Install Terminal Add-on

For command-line access:

1. Navigate to **Settings** → **Add-ons**
2. Click **Add-on Store**
3. Search for "Terminal & SSH"
4. Click **Install**
5. Start the add-on

### Recommended Add-ons

| Add-on | Purpose |
|--------|---------|
| Terminal & SSH | Command-line access |
| File Editor | Edit configuration files |
| Samba Share | Access files from network |
| InfluxDB | Time-series database |
| Grafana | Dashboards and visualization |


## Integrations

### Add Integrations

1. Navigate to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search and configure

### Common Integrations

| Integration | Setup |
|-------------|-------|
| Philips Hue | Auto-discovered |
| Zigbee | Requires coordinator |
| Z-Wave | Requires controller |
| Google Home | Cloud account |
| Alexa | Cloud account |

## Automations

### Create Automation

1. Navigate to **Settings** → **Automations**
2. Click **Create Automation**
3. Define trigger, conditions, actions

### Example: Motion Light

```yaml
alias: "Motion Light"
trigger:
  - platform: state
    entity_id: binary_sensor.motion
    to: "on"
condition:
  - condition: sun
    after: sunset
action:
  - service: light.turn_on
    target:
      entity_id: light.living_room
```

## n8n Integration

Connect Home Assistant to n8n for complex workflows:

### Generate Long-Lived Token

1. Click your profile
2. Scroll to **Long-Lived Access Tokens**
3. Create token
4. Save securely

### Configure n8n

In n8n, use HTTP Request node:

```
URL: http://homeassistant.mgmt.internal:8123/api/services/<domain>/<service>
Headers:
  Authorization: Bearer <your-token>
  Content-Type: application/json
```

## Backup

### Built-in Backups

Home Assistant includes automatic backups:

1. Navigate to **Settings** → **System** → **Backups**
2. Configure automated backups
3. Download backups for off-site storage

### Proxmox Backup

The VM is also backed up via PBS for full system recovery.

## Troubleshooting

### Cannot Access Web Interface

- Verify VM is running
- Check IP address
- Confirm network connectivity
- Check firewall rules

### Integration Not Found

- Ensure device is on correct network
- Check mDNS/discovery settings
- Try manual configuration

### Slow Performance

- Increase VM resources
- Review integrations (disable unused)
- Check database size

## Security Best Practices

- Use strong passwords
- Enable MFA
- Keep HAOS updated
- Isolate IoT network
- Review automation rules
- Limit cloud integrations

## Next Steps

- Add smart devices
- Create automations
- Integrate with [n8n](../productivity-stack/n8n.md) for workflows
- Connect local AI via [LiteLLM](../ai-stack/litellm.md)
