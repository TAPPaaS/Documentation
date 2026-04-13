---
title: Identity
description: Deploy identity and secrets management for TAPPaaS
---

# Identity Management

This guide covers deploying identity and secrets management using Authentik

***TODO: Not tested***

## Components

| Service | Purpose |
|---------|---------|
| **Authentik** | Identity provider, SSO, user management |

TODO: central management of API keys are not implemented yet

## Prerequisites

- [ ] [CICD Mothership](cicd.md) operational
- [ ] [Firewall and reverse proxy (Caddy)](firewall.md) operational

## DNS Configuration

Register the services with your DNS provider:
(This is DNS provider specific, you are on your own for the details)

| Record | Type | Value |
|--------|------|-------|
| `identity.yourdomain.com` | A | Your public IP |

## Installation

### Deploy Identity VM

From the tappaas-cicd VM:

```bash
cd ~/TAPPaaS/src/foundation/identity
install-module.sh identity
```

This creates a VM with Authentik configured.

## Authentik Configuration

(To be automated)

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


## Integration

(o be automated as a identity:auth service)

### Service Integration

Connect other TAPPaaS services to Authentik:

```yaml
# Example: n8n OAuth configuration
N8N_AUTH_OAUTH2_CLIENT_ID: "your-client-id"
N8N_AUTH_OAUTH2_CLIENT_SECRET: "your-client-secret"
N8N_AUTH_OAUTH2_AUTHORIZE_URL: "https://authentik.yourdomain.com/application/o/authorize/"
N8N_AUTH_OAUTH2_ACCESS_TOKEN_URL: "https://authentik.yourdomain.com/application/o/token/"
```

## Verification

Test the identity system:

```bash
# Check Authentik health
curl -f https://authentik.yourdomain.com/-/health/ready/

## Next Steps

Complete the foundation with [Security](security.md) hardening.
