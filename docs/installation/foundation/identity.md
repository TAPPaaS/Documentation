---
title: Identity
description: The identity provider (Authentik) — installed and bootstrapped automatically
---

# Identity Management

TAPPaaS ships **Authentik** as the identity provider (SSO, users, groups, access
control). On 2.0 its installation and credential bootstrap are **fully automated** —
there is no manual setup wizard.

## Components

| Service | Purpose |
|---------|---------|
| **Authentik** | Identity provider, SSO, user management |

## Prerequisites

- [ ] [CICD Mothership](cicd.md) operational
- [ ] [Firewall and reverse proxy (Caddy)](firewall.md) operational

## Installation — automated

Identity is installed as part of the foundation sequence (`rest-of-foundation.sh`,
see the synced [INSTALL.md](../../generated/install.md)): backup → **identity** → …
During that run the platform also **bootstraps your people domain** — your
organisation and admin are created in Authentik automatically, driven by the
configuration you provided at bootstrap.

The credential handshake is automated and self-healing: the CICD host fetches the
Authentik bootstrap token from the identity VM on demand, so consuming modules
(access control, SSO integrations) can install without manual credential steps —
even after a CICD rebuild.

## Using it

- Admin UI: `https://identity.mgmt.internal/` (management zone).
- Users, groups and organisations are managed through the
  [People Manager](../../generated/managers/people-manager.md); see also the
  [Identity Controller](../../generated/controllers/identity-controller.md) for the
  system-level reference.

## Verification

```bash
# Check Authentik health (from the management zone)
curl -f https://identity.mgmt.internal/-/health/ready/
```

## Next Steps

Complete the foundation with [Security](security.md) hardening.
