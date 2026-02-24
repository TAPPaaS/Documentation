---
title: CICD Mothership
description: Deploy the TAPPaaS central management and automation VM
---

# CICD Mothership aka tappaas-cicd

The TAPPaaS CICD "mothership" named "tappaas-cicd" is the central control VM that manages your entire TAPPaaS infrastructure through automation and configuration management.

## Overview

The implementation involves three phases:

1. **VM Creation** - Deploy from the NixOS template
2. **System Configuration** - Configure git repository and NixOS settings
3. **Tool Installation** - Set up CI/CD pipelines and utilities

## Prerequisites

- [ ] [VM Templates](vm-templates.md) created
- [ ] [Firewall](firewall.md) accessible
- [ ] Git repository access configured

## Deploy the VM

### Download Configuration

On a Proxmox host:

```bash
REPO="https://raw.githubusercontent.com/TAPPaaS/TAPPaaS/"
BRANCH="main"
curl -fsSL ${REPO}${BRANCH}/src/foundation/tappaas-cicd/tappaas-cicd.json \
  > ~/tappaas/tappaas-cicd.json
```

### Clone from Template

```bash
~/tappaas/Create-TAPPaaS-VM.sh tappaas-cicd
```

### Get VM IP

Once the VM boots, find its IP address:

1. Check DHCP leases in OPNsense, or
2. View the VM summary page in Proxmox

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
curl -fsSL "${REPO}${BRANCH}/src/foundation/tappaas-cicd/install1.sh" \
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
   - Log into OPNsense on firewall.mgmt.internal
   - Navigate to **System** → **Settings** → **Administration**
   - Enable "Secure Shell"
   - Permit root user login
   - Disable password authentication
   - press Save to apply settings

2. **Install Public Key**:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the output and enter it in the OPNsense gui under:

- System->Access->Users
- click edit command on the "root" account
- Scroll down to the bottom and enter the key
- press save

3. **Test Connection**:
   ```bash
   ssh root@10.0.0.1 "echo 'SSH working'"
   ```

### API Access

Create API credentials for automation:

1. In OPNsense, navigate to **System** → **Access** → **Users**
2. Create user `tappaas` with 
  - gGoup membership "admin"
  - Privileges: "all pages"
3. Generate API key and secret
  - On the same page, in the new user line tappaas, look at the commands section to the rigth. There is a "create and download API keys" button 
  - press and create 
  - open the downloaded txt file and copy the two key lines
4. In a terminal window ssh into the tappaas-cicd and:
  - create a file ~/.opnsense-credentials.txt using you vi or nano.
  - insert the copied two API key lines
  - save

Delete the downloaded key file from your browser pc.

## Program Installation

### Run Main Deployment

```bash
cd
cd TAPPaaS/src/foundation/tappaas-cicd
UPSTREAMGIT="github.com/TAPPaaS/TAPPaaS"
BRANCH="main"
DOMAIN="yourdomain.com"
EMAIL="admin@yourdomain.com"
SCHEDULE="weekly"
./install2.sh $UPSTREAMGIT $BRANCH $DOMAIN $EMAIL $SCHEDULE
```

The script might prompt for root paswords to the tappaas nodes

This script installs and configures:

- All the scripts and programs that tappaas-cicd need
- finish off install of firewall
- Installs Caddy reverse proxy
- Sets up Automation pipelines and scheduled maintenance tasks

## Reverse Proxy Configuration

### Reassign OPNsense Port

Move OPNsense web interface off port 443:

1. Navigate to **System** → **Settings** → **Administration**
2. Change "TCP Port" to `8443`
3. press Save to apply
4. Reconnect to OPNsense at firewall.mgmt.internal:8443

### Configure Caddy

Access OPNsense and configure Caddy:

1. Navigate to **Services** → **Caddy Web Server** → **General Settings**
2. Enable Caddy
3. Set ACME email address to your administrator email

### Add Domain Handlers

Configure reverse proxy for your services in Caddy's domain configuration.

(information to be provided eventually)

## Verification

Verify the CICD system is operational:

```bash
# Test VM automation
./test.sh
```

## Next Steps

Continue to [Backup](backup.md) configuration.
