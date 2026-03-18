---
title: update-module.sh
description: Update a TAPPaaS module with snapshot, testing, and automatic rollback
---

# update-module.sh

Updates a TAPPaaS module safely with snapshot, testing, and automatic rollback.

## Usage

```bash
update-module.sh [options] <module-name>
```

## Options

| Option | Description |
|--------|-------------|
| `--force` | Proceed even if pre-update test fails |
| `--debug` | Show Debug-level messages |
| `--silent` | Suppress Info-level messages |

## What it does

1. Creates a pre-update VM snapshot (rollback safety net)
2. Runs `test-module.sh` pre-update — aborts if tests fail (unless `--force`)
3. Runs the module's `pre-update.sh` hook (if present)
4. Iterates `dependsOn` and calls each provider's `update-service.sh`
5. Calls the module's own `update.sh`
6. Runs `test-module.sh` post-update — rolls back on fatal failure

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | Update succeeded, all tests passed |
| `1` | Update completed but post-update test failed (non-fatal) |
| `2` | Fatal error (rollback attempted if snapshot exists) |

## Examples

```bash
update-module.sh vaultwarden
update-module.sh --force litellm
update-module.sh --debug openwebui
```

## See Also

- [install-module.sh](install-module.md) - Install a module
- [delete-module.sh](delete-module.md) - Delete a module
- [test-module.sh](test-module.md) - Test a module
- [Module Structure](../../architecture/cicd-design/module-structure.md) - Detailed module lifecycle documentation
