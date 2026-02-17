---
title: Security
description: Harden your TAPPaaS installation
---

# Securing TAPPaaS

This guide covers security hardening activities for your TAPPaaS installation and establishing secure remote access.

## Overview

Security hardening includes:

- Access control improvements
- Network security
- Monitoring and detection
- Secure remote access via Netbird

## Planned Security Tasks

!!! warning "Work in Progress"
    Some security features are still being developed. This guide covers currently available hardening steps.

- [ ] Lock down root login with password
- [ ] Execute security test scripts
- [ ] Deploy CrowdSec
- [ ] Restrict backup user permissions

## SSH Hardening

### Disable Root Password Login

Edit SSH configuration on all nodes:

```bash
sudo nano /etc/ssh/sshd_config
```

Set:

```
PermitRootLogin prohibit-password
PasswordAuthentication no
```

Restart SSH:

```bash
sudo systemctl restart sshd
```

### SSH Key Management

Ensure only authorized keys are present:

```bash
# Review authorized keys
cat ~/.ssh/authorized_keys

# Remove unauthorized keys
nano ~/.ssh/authorized_keys
```

## Firewall Hardening

### Review OPNsense Rules

Audit firewall rules in OPNsense:

1. Navigate to **Firewall** → **Rules**
2. Review each interface's rules
3. Remove unnecessary allow rules
4. Ensure default deny is in place

### Network Segmentation

Implement VLANs for isolation:

| VLAN | Purpose | Access |
|------|---------|--------|
| Management | Infrastructure | Restricted |
| Services | Applications | Internal |
| IoT | Home automation | Isolated |
| Guest | Visitor access | Internet only |

## Netbird VPN Setup

Netbird provides secure remote access to your TAPPaaS infrastructure.

### Account Setup

Choose your Netbird deployment:

1. **Public Service**: Use netbird.io (easiest)
2. **Self-Hosted**: Deploy on a separate TAPPaaS system

!!! tip "Resilience Recommendation"
    If self-hosting Netbird, deploy it on a **different** TAPPaaS system or configure high availability. This ensures VPN access remains available if your primary system has issues.

### Client Installation

Netbird client is pre-installed on TAPPaaS nodes. Activate on each node:

```bash
# Using netbird.io public service
netbird up

# Using self-hosted Netbird
netbird up --management-url https://netbird.yourdomain.com:33073
```

Follow the prompts and open the provided URL in a web browser to authenticate.

### Alternative: Setup Key

For automated deployment, generate a setup key from Netbird admin console:

```bash
netbird up --setup-key <your-key> --management-url https://netbird.yourdomain.com:33073
```

### Benefits

With Netbird configured:

- Access TAPPaaS from anywhere securely
- No port forwarding required
- Encrypted peer-to-peer connections
- Redundant access through multiple nodes

## CrowdSec (Planned)

CrowdSec will provide:

- Intrusion detection
- Collaborative threat intelligence
- Automated blocking of malicious IPs

Installation documentation coming soon.

## Audit and Monitoring

### Log Review

Regularly review system logs:

```bash
# Authentication logs
journalctl -u sshd --since "24 hours ago"

# System logs
journalctl -p err --since "24 hours ago"
```

### Failed Login Monitoring

Monitor for brute force attempts:

```bash
# Check for failed SSH attempts
grep "Failed password" /var/log/auth.log | tail -20
```

## Backup Security

### Restrict Backup User

The backup user should not have delete permissions:

1. In PBS, navigate to **Configuration** → **Access Control**
2. Edit `tappaas@pbs` permissions
3. Remove `DatastoreAdmin` role
4. Assign `DatastoreBackup` role only

This prevents ransomware from deleting backups through a compromised system.

## Security Checklist

### Initial Deployment

- [ ] Change all default passwords
- [ ] Enable SSH key authentication
- [ ] Disable password authentication
- [ ] Configure firewall rules
- [ ] Set up Netbird VPN

### Ongoing

- [ ] Regular security updates
- [ ] Log review
- [ ] Access audit
- [ ] Backup verification
- [ ] Penetration testing (annual)

## Verification

Run security verification:

```bash
# Check SSH configuration
sshd -T | grep -E "(passwordauthentication|permitrootlogin)"

# Check for listening services
ss -tlnp

# Check firewall status
# (on OPNsense via API or web interface)
```

## Next Steps

With the foundation complete, you can now deploy optional stacks:

- [AI Stack](../ai-stack/index.md)
- [Productivity Stack](../productivity-stack/index.md)
- [Home Stack](../home-stack/index.md)
