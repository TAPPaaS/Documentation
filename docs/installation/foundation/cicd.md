---
title: CICD Mothership
description: Deploy the TAPPaaS central management and automation VM
---

# CICD Mothership

The TAPPaaS CICD "mothership" is the central control VM that manages your entire TAPPaaS infrastructure through automation and configuration management.

## Overview

The implementation involves three phases:

1. **VM Creation** - Deploy from the NixOS template
2. **System Configuration** - Configure git repository and NixOS settings
3. **Tool Installation** - Set up CI/CD pipelines and utilities

## Prerequisites

- [ ] [NixOS Template](nixos-template.md) created
- [ ] [Firewall](firewall.md) accessible
- [ ] Git repository access configured

## Deploy the VM

### Download Configuration

On a Proxmox host:

```bash
mkdir -p ~/tappaas
REPO="https://raw.githubusercontent.com/TAPPaaS/TAPPaaS/"
BRANCH="main"
curl -fsSL ${REPO}${BRANCH}/src/foundation/30-tappaas-cicd/tappaas-cicd.json \
  > ~/tappaas/tappaas-cicd.json
```

### Clone from Template

```bash
~/tappaas/Create-TAPPaaS-VM.sh tappaas-cicd
```

### Get VM IP

Once the VM boots, find its IP address:

1. Check DHCP leases in OPNsense, or
2. View the VM console in Proxmox

### Connect via SSH

```bash
ssh tappaas@<vm-ip>
```

## Initial Configuration

### Run Setup Script

```bash
REPO="https://raw.githubusercontent.com/TAPPaaS/TAPPaaS/"
REPOTOCLONE="https://github.com/TAPPaaS/TAPPaaS.git"
BRANCH="main"
curl -fsSL "${REPO}${BRANCH}/src/foundation/30-tappaas-cicd/install1.sh" \
  -o /tmp/install1.sh
bash /tmp/install1.sh "$REPOTOCLONE" "$BRANCH"
```

This script:

- Sets the hostname
- Clones the TAPPaaS repository
- Configures NixOS integration

### Reboot

```bash
sudo reboot
```

After reboot, verify connectivity using the FQDN:

```bash
ssh tappaas@tappaas-cicd.mgmt.internal
```

## Firewall Integration

### SSH Authentication

Set up SSH key authentication to OPNsense:

1. **Enable SSH in OPNsense**:
   - Navigate to **System** → **Settings** → **Administration**
   - Enable "Secure Shell"
   - Disable password authentication

2. **Install Public Key**:
   - Add the tappaas-cicd public key to root's authorized_keys in OPNsense

3. **Test Connection**:
   ```bash
   ssh root@10.0.0.1 "echo 'SSH working'"
   ```

### API Access

Create API credentials for automation:

1. In OPNsense, navigate to **System** → **Access** → **Users**
2. Create user `tappaas` with admin privileges
3. Generate API key and secret
4. Store credentials on the CICD VM:

```bash
cat > ~/.opnsense-credentials.txt << EOF
key=your-api-key
secret=your-api-secret
EOF
chmod 600 ~/.opnsense-credentials.txt
```

## Program Installation

### Run Main Deployment

```bash
cd TAPPaaS/src/foundation/30-tappaas-cicd

# Set your environment variables
UPSTREAMGIT="github.com/TAPPaaS/TAPPaaS"
BRANCH="main"
DOMAIN="yourdomain.com"
EMAIL="admin@yourdomain.com"
SCHEDULE="weekly"

./install2.sh $UPSTREAMGIT $BRANCH $DOMAIN $EMAIL $SCHEDULE
```

This script installs and configures:

- Caddy reverse proxy
- Automation pipelines
- Scheduled maintenance tasks

## Reverse Proxy Configuration

### Reassign OPNsense Port

Move OPNsense web interface off port 443:

1. Navigate to **System** → **Settings** → **Administration**
2. Change "TCP Port" to `8443`
3. Save and apply

### Configure Caddy

Access OPNsense and configure Caddy:

1. Navigate to **Services** → **Caddy Web Server** → **General Settings**
2. Enable Caddy
3. Set ACME email address

### Add Domain Handlers

Configure reverse proxy for your services in Caddy's domain configuration.

## Verification

Verify the CICD system is operational:

```bash
# Check services
systemctl status

# Verify git repository
cd ~/TAPPaaS && git status

# Test automation
./test-automation.sh
```

## Next Steps

Continue to [Backup](backup.md) configuration.
