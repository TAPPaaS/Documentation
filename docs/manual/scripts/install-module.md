---
title: install-module.sh
description: Install a TAPPaaS module with dependency validation
---

# install-module.sh

Deploys a TAPPaaS module with comprehensive dependency validation and service integration.

## Usage

```bash
install-module.sh <module-name> [--variant <name>] [--<field> <value>]...
```

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `module-name` | Module to deploy | `openwebui` |
| `--variant <name>` | Install a variant version | `--variant staging` |
| `--<field> <value>` | Override JSON field | `--node tappaas2` |

## What it does

1. **Configuration Setup** — Uses `copy-update-json.sh` to prepare the module JSON config, supporting variant mode with automatic field derivation
2. **Dependency Validation** — Confirms all services listed in `dependsOn` are provided by already-installed modules
3. **Service Script Verification** — Ensures the module contains service scripts for each service it provides
4. **Dependency Installation** — Iterates through `dependsOn` and calls each provider's `install-service.sh`
5. **Module Installation** — Executes the module's `install.sh` if present

## Variant Mode

When `--variant <name>` is specified, the script leverages `copy-update-json.sh` to automatically derive:

- **vmname** — Base name plus variant (e.g., `openwebui-staging`)
- **vmid** — Next available ID after the source module
- **zone0** — Variant name if it matches a configured zone, otherwise unchanged
- **proxyDomain** — Variant inserted after first domain segment

These can be overridden with explicit `--<field>` parameters.

## Examples

```bash
# Basic installation
install-module.sh vaultwarden

# With field override
install-module.sh litellm --node tappaas2

# Install staging variant (auto-derives vmname, vmid, proxyDomain)
install-module.sh openwebui --variant staging

# Variant with explicit overrides
install-module.sh openwebui --variant dev --zone0 dev-srv --vmid 315
```

## See Also

- [update-module.sh](update-module.md) - Update a module
- [delete-module.sh](delete-module.md) - Delete a module
- [Module Structure](../../architecture/cicd-design/module-structure.md) - Detailed module lifecycle documentation
