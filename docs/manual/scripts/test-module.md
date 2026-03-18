---
title: test-module.sh
description: Test a TAPPaaS module with dependency-recursive service testing
---

# test-module.sh

Tests a TAPPaaS module with dependency-recursive service testing.

## Usage

```bash
test-module.sh [options] <module-name>
```

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `module-name` | Name of the module to test | `openwebui` |
| `--deep` | Run extended/heavy tests | |
| `--debug` | Show Debug-level messages | |
| `--silent` | Suppress Info-level messages | |

## What it does

1. Validates the module JSON config exists and is valid
2. Checks that dependency services have `test-service.sh` scripts
3. Iterates `dependsOn` and calls each provider's `test-service.sh`
4. Calls the module's own `test.sh` (if present)
5. Reports structured results with pass/fail/skip counts

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | All tests passed |
| `1` | One or more tests failed |
| `2` | Fatal error (requires rollback/reinstall) |

## Service tests included

| Service | Tests (standard) | Tests (--deep) |
|---------|-----------------|----------------|
| `cluster:vm` | VM running, ping, SSH | Disk usage, memory |
| `cluster:ha` | HA resource status, affinity rule | Replication job, replication health |
| `firewall:proxy` | Caddy domain, handler, HTTPS | TLS certificate, upstream reachability |

## Structured output

Each message is prepended with `[Info]`, `[Debug]`, `[Warning]`, `[Error]`, or `[Fatal]`.

## Environment variables

- `TAPPAAS_TEST_DEEP=1` — same as `--deep`
- `TAPPAAS_DEBUG=1` — same as `--debug`

## Examples

```bash
# Quick sanity check
test-module.sh openwebui

# Full regression test
test-module.sh --deep openwebui

# Silent mode for CI
test-module.sh --silent openwebui
```

## See Also

- [update-module.sh](update-module.md) - Update a module (uses test-module.sh)
- [install-module.sh](install-module.md) - Install a module
