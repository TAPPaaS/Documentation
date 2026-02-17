---
title: Identity
description: Deploy identity and secrets management for TAPPaaS
---

# Identity Management

This guide covers deploying identity and secrets management using Authentik and VaultWarden.

## Components

| Service | Purpose |
|---------|---------|
| **Authentik** | Identity provider, SSO, user management |
| **VaultWarden** | Password and secrets management |

## Prerequisites

- [ ] [CICD Mothership](cicd.md) operational
- [ ] DNS management access
- [ ] Reverse proxy configured

## DNS Configuration

Register the services with your DNS provider:

| Record | Type | Value |
|--------|------|-------|
| `authentik.yourdomain.com` | A | Your public IP |
| `vaultwarden.yourdomain.com` | A | Your public IP |

## Reverse Proxy Setup

Configure Caddy routing in OPNsense:

### Authentik Route

```
authentik.yourdomain.com {
    reverse_proxy identity.mgmt.internal:80
}
```

### VaultWarden Route

```
vaultwarden.yourdomain.com {
    reverse_proxy identity.mgmt.internal:8080
}
```

## Installation

### Deploy Identity VM

From the tappaas-cicd VM:

```bash
cd ~/TAPPaaS/src/foundation/40-Identity
./install.sh
```

This creates a VM with both Authentik and VaultWarden pre-configured.

## Firewall Rules

Create firewall rules in OPNsense:

| Source | Destination | Port | Protocol | Action |
|--------|-------------|------|----------|--------|
| Caddy | identity.mgmt.internal | 80 | TCP | Allow |
| Caddy | identity.mgmt.internal | 8080 | TCP | Allow |

## Authentik Configuration

### Initial Setup

Access Authentik at `https://authentik.yourdomain.com/if/flow/initial-setup/`

1. Create the admin account
2. Set a strong password
3. Complete the setup wizard

### Configure Applications

For each TAPPaaS service requiring authentication:

1. Navigate to **Applications** → **Applications**
2. Click **Create**
3. Configure the application settings
4. Set up the appropriate provider (OAuth2, SAML, etc.)

### User Management

Create users and groups:

1. Navigate to **Directory** → **Users**
2. Create users as needed
3. Assign to appropriate groups

## VaultWarden Configuration

### Initial Access

Access VaultWarden at `https://vaultwarden.yourdomain.com`

### Create Admin Account

1. Register a new account
2. Set a strong master password
3. Enable admin features if needed

### Organization Setup

For team usage:

1. Create an organization
2. Invite team members
3. Set up shared collections

## Integration

### Authentik + VaultWarden SSO

Configure VaultWarden to use Authentik for SSO:

1. In Authentik, create an OAuth2 provider for VaultWarden
2. Configure VaultWarden's SSO settings
3. Test the authentication flow

### Service Integration

Connect other TAPPaaS services to Authentik:

```yaml
# Example: n8n OAuth configuration
N8N_AUTH_OAUTH2_CLIENT_ID: "your-client-id"
N8N_AUTH_OAUTH2_CLIENT_SECRET: "your-client-secret"
N8N_AUTH_OAUTH2_AUTHORIZE_URL: "https://authentik.yourdomain.com/application/o/authorize/"
N8N_AUTH_OAUTH2_ACCESS_TOKEN_URL: "https://authentik.yourdomain.com/application/o/token/"
```

## Backup

Both services store critical data - ensure backups are configured:

### Authentik Backup

Authentik data is stored in PostgreSQL. The PBS backup includes the VM's database.

### VaultWarden Backup

VaultWarden stores data in SQLite. Additional export is recommended:

```bash
# Export vault data
sqlite3 /data/db.sqlite3 ".backup '/backup/vaultwarden.db'"
```

## Verification

Test the identity system:

```bash
# Check Authentik health
curl -f https://authentik.yourdomain.com/-/health/ready/

# Check VaultWarden health
curl -f https://vaultwarden.yourdomain.com/alive
```

## Security Recommendations

- Enable MFA for all admin accounts
- Use strong, unique passwords
- Regularly audit user access
- Keep services updated
- Monitor authentication logs

## Next Steps

Complete the foundation with [Security](security.md) hardening.
