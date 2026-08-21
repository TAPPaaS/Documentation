---
title: Admin Access
description: >
  The three ways to reach the tappaas@tappaas-cicd prompt — from the management
  network, over WireGuard to a public IP, or over WireGuard via a satellite.
---

# Admin Access

Nearly every operation in this section is run from the **`tappaas@tappaas-cicd`
prompt** — the CICD mothership account that holds the managers, the controllers,
and SSH access to the rest of the cluster.

TAPPaaS deliberately exposes **no inbound SSH**: there are no port forwards, and
the management plane (`mgmt`, `10.0.0.0/24`) is never reachable from the internet
directly. So getting to that prompt means being *on* the management network — either
physically, or through a WireGuard tunnel that lands you there.

```bash
ssh tappaas@tappaas-cicd.mgmt.internal
```

## The three ways in

| | Use when | Setup |
| --- | --- | --- |
| **1. A client on the `mgmt` network** | You are on site, on the LAN. The simplest case and the fallback when the others are down. | [Network Zones](../generated/zones.md) — the `mgmt` zone and what may enter it |
| **2. WireGuard to a public IP** | The cluster's WAN has a real public IP (not CGNAT). Your device tunnels straight to OPNsense. | [Admin VPN (WireGuard)](../generated/admin-vpn.md) — Topology B |
| **3. WireGuard via a satellite** | The site is behind CGNAT or has no inbound reach. A satellite with a public IP blind-relays the tunnel. | [Add Satellite](../generated/satellite-install.md), then [Admin VPN (WireGuard)](../generated/admin-vpn.md) — Topology A |

Ways 2 and 3 are the **same tunnel**: your WireGuard session always terminates on
OPNsense and lands in the `admin` overlay zone (`10.255.1.0/24`), which one
least-privilege firewall rule grants into `mgmt`. Only the `Endpoint` in your client
config differs — the cluster's public IP, or the satellite's. A satellite never holds
admin keys and never sees the traffic; it forwards opaque UDP.

That also means switching between them, or adding a satellite later, needs no change
on the OPNsense side — just a new `Endpoint`.

## SSH keys

All three ways end in an SSH session, so you need a key pair on your workstation and
its public half installed on the target. The procedure — generating an `ed25519` key,
copying it across, and clearing a stale host key after a reinstall — is in the install
guide:

- [Generate and install an SSH key](../generated/install.md#1-generate-and-install-an-ssh-key-from-your-workstation)

Give each device its own key pair, and each device its own WireGuard peer — removing a
peer or a key then revokes exactly one device.

## Related

- [Admin VPN (WireGuard)](../generated/admin-vpn.md) — the full runbook: enrolling a
  peer, managing peers, reaching zones beyond `mgmt`, and troubleshooting.
- [Install Foundation](../generated/install.md) — the admin VPN termination is brought
  up during bootstrap; no manual firewall step is needed.
- [Network Zones](../generated/zones.md) — the zone model the firewall enforces.
