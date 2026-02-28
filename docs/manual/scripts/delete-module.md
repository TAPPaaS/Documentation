---
title: delete-module.sh
description: Delete a TAPPaaS module with dependency-aware teardown
---

# delete-module.sh

Deletes a TAPPaaS module with dependency-aware service teardown.

## Usage

```bash
delete-module.sh <module-name> [--force]
```

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `module-name` | Name of the module to delete | `vaultwarden` |
| `--force` | Delete even if other modules depend on this module's services | |

## What it does

1. Validates the module JSON config exists in `/home/tappaas/config/`
2. Checks reverse dependencies — blocks if other modules depend on this module's services (unless `--force`)
3. Calls the module's own `delete.sh` (if present) while the VM still exists
4. Iterates `dependsOn` in **reverse** order and calls each provider's `delete-service.sh` (skips if not found)
5. Removes the module configuration files (`.json` and `.json.orig`)

## Examples

```bash
delete-module.sh vaultwarden
delete-module.sh litellm --force
```

## Notes

- The deletion order is reversed compared to installation: the module's own `delete.sh` runs first (while the VM still exists), then services are torn down in reverse dependency order
- HA/replication is removed before the VM is destroyed to prevent conflicts
- Missing `delete-service.sh` scripts are skipped (not an error), allowing incremental rollout
- Service teardown failures produce warnings but do not abort the overall deletion

## See Also

- [install-module.sh](install-module.md) - Install a module
- [update-module.sh](update-module.md) - Update a module
- [Module Structure](../../architecture/cicd-design/module-structure.md) - Detailed module lifecycle documentation
