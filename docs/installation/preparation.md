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
- [ ] Credentials prepared

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

### Internal Network Design

Plan your internal network:

| Network | VLAN | Subnet | Purpose |
|---------|------|--------|---------|
| Management | 1 | 10.0.0.0/24 | Infrastructure management |
| Services | 100 | 10.1.0.0/24 | Application services |
| IoT | 200 | 10.2.0.0/24 | Home automation devices |

## Credential Preparation

### Root Password

Create a strong root password that will be used for:

- Proxmox hypervisor
- OPNsense firewall
- Initial VM access

!!! warning "Password Requirements"
    Use a complex password with:

    - Minimum 16 characters
    - Mix of upper/lowercase letters
    - Numbers and special characters
    - No dictionary words

### SSH Keys

Generate an SSH key pair for secure access:

```bash
ssh-keygen -t ed25519 -C "tappaas-admin"
```

Store the private key securely and have the public key ready for installation.

### Service Accounts

Plan credentials for:

- Email address for Let's Encrypt certificates
- API keys for external services (if needed)
- Admin accounts for web interfaces

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

### Storage Preparation

If reusing drives:

- Back up any important data
- Note drive identifiers for ZFS pool creation

## Documentation

Keep records of:

| Item | Value |
|------|-------|
| Public IP | |
| Domain name | |
| Root password | |
| Admin email | |
| Network subnets | |
| Hardware specs | |

## Configuration File

TAPPaaS uses a central configuration file. Prepare values for:

```json
{
  "domain": "yourdomain.com",
  "email": "admin@yourdomain.com",
  "timezone": "Europe/London",
  "network": {
    "management": "10.0.0.0/24",
    "services": "10.1.0.0/24"
  }
}
```

## Next Steps

Once preparation is complete:

1. Begin with [Foundation Installation](foundation/index.md)
2. Start with the [Proxmox Node](foundation/proxmox-node.md) setup
