---
title: Preparation
description: Prepare your environment before installing TAPPaaS
---

# Preparation

Before beginning the TAPPaaS installation, complete these preparation steps to ensure a smooth deployment.

## Prerequisites Checklist

- [ ] Hardware acquired and assembled
- [ ] Network connectivity established
- [ ] Domain name registered
- [ ] DNS access configured
- [ ] Admin email account prepared

## Network Preparation

### Internet Connectivity

Ensure you have:

- Reliable wired internet connection
- Public IP address (static preferred)
- Ports 80 and 443 available for inbound traffic

### Domain Name

You will need:

- A registered domain name
- Access to DNS management
- Ability to create A records and subdomains

Example DNS records you'll create:

```
tappaas.yourdomain.com    → Your public IP
*.tappaas.yourdomain.com  → Your public IP (wildcard)
```

## Email Account Preparation

Prepare a dedicated email account for system administration notifications. This email will be used for:

- Let's Encrypt certificate notifications
- System alerts and monitoring
- Backup status reports
- Security notifications

!!! tip "Recommendation"
    Use a dedicated admin email address (e.g., `admin@yourdomain.com`) rather than a personal email to ensure notifications are not missed and can be monitored by multiple team members if needed.

## Software Preparation

### Download Proxmox VE

1. Visit [proxmox.com/downloads](https://www.proxmox.com/en/downloads)
2. Download the latest Proxmox VE ISO
3. Create bootable USB media using:
   - **Windows**: Rufus
   - **macOS**: balenaEtcher
   - **Linux**: `dd` command

### Verify Downloads

Always verify ISO checksums:

```bash
sha256sum proxmox-ve_*.iso
```

Compare with the official checksums from the Proxmox download page.

## Hardware Preparation

### BIOS/UEFI Settings

Configure your hardware:

- Enable virtualization (VT-x/AMD-V)
- Enable IOMMU if available
- Set boot order to USB first
- Disable Secure Boot (optional, for compatibility)

## Documentation

Keep records of:

| Item | Value |
|------|-------|
| Public IP | |
| Domain name | |
| Root password | |
| Admin email | |

## Next Steps

Once preparation is complete:

1. Begin with [Foundation Installation](foundation/index.md)
2. Start with the [Proxmox Node](foundation/proxmox-node.md) setup
