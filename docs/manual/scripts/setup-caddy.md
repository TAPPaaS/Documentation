---
title: setup-caddy.sh
description: Install Caddy reverse proxy on firewall
---

# setup-caddy.sh

Installs and configures the Caddy reverse proxy on the OPNsense firewall.

## Usage

```bash
setup-caddy.sh
```

## What it does

- Installs the os-caddy package on the firewall
- Creates firewall rules for HTTP (port 80) and HTTPS (port 443)
- Prints manual configuration steps for completing setup in OPNsense GUI

## Note

Additional manual configuration is required. See the tappaas-cicd README.md for details.

## See Also

- [OPNsense Controller](../opnsense-controller.md) - Firewall management tools
