---
title: install-module.sh
description: Install a TAPPaaS module with dependency validation
---

# install-module.sh

Installs a TAPPaaS module with dependency validation and service wiring.

## Usage

```bash
install-module.sh <module-name> [--<field> <value>]...
```

## What it does

1. Copies and validates the module JSON config
2. Checks that every `dependsOn` service is provided by an installed module
3. Validates that the module has service scripts for each service it provides
4. Iterates `dependsOn` and calls each provider's `install-service.sh`
5. Calls the module's own `install.sh` (if present)

## Examples

```bash
install-module.sh vaultwarden
install-module.sh litellm --node tappaas2
```

## See Also

- [update-module.sh](update-module.md) - Update a module
- [delete-module.sh](delete-module.md) - Delete a module
- [Module Structure](../../architecture/cicd-design/module-structure.md) - Detailed module lifecycle documentation
