---
title: update-module.sh
description: Update a TAPPaaS module with dependency-aware service wiring
---

# update-module.sh

Updates a TAPPaaS module with dependency-aware service wiring.

## Usage

```bash
update-module.sh <module-name>
```

## What it does

1. Validates the module JSON config exists
2. Checks that every `dependsOn` service is still available
3. Runs the module's `pre-update.sh` (if present)
4. Iterates `dependsOn` and calls each provider's `update-service.sh`
5. Calls the module's own `update.sh`

## Examples

```bash
update-module.sh vaultwarden
update-module.sh litellm
```

## See Also

- [install-module.sh](install-module.md) - Install a module
- [delete-module.sh](delete-module.md) - Delete a module
- [Module Structure](../../architecture/cicd-design/module-structure.md) - Detailed module lifecycle documentation
