---
title: test-config.sh
description: Validate TAPPaaS installation
---

# test-config.sh

Validates the TAPPaaS-CICD installation by running a series of checks.

## Usage

```bash
test-config.sh
```

## Checks performed

- tappaas user exists
- SSH keys exist for tappaas user
- TAPPaaS repository is cloned
- NixOS configuration is applied

## Output

- Color-coded status messages (green=OK, red=error, blue=warning)
- Detailed log written to `/home/tappaas/logs/test-config.log`
