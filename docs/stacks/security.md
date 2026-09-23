---
title: Security Stack
description: Secrets and secure access — the modules whose job is protecting the rest.
---

# Security Stack

| Module | Role |
|--------|------|
| [Vaultwarden](../generated/modules/vaultwarden.md) | Bitwarden-compatible password manager — your credentials, at home |
| [NetBird Client](../generated/modules/netbird-client.md) | Mesh connectivity, so a site is reachable without opening a port |

These are modules whose *purpose* is security. They are not the whole of TAPPaaS's
security posture — that is built into the platform rather than added on: identity and
single sign-on come from the [Foundation Stack](foundation.md), network separation from
the zone model (see [Network Zones](../generated/zones.md)), and off-site, encrypted
backup from `backup`. A stack groups modules by what they are *for*; it does not say
where the security lives.

Install guides live under [Install → Add Stacks](../install/index.md).
