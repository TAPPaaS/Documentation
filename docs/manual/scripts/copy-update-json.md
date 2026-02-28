---
title: copy-update-json.sh
description: Copy and modify module JSON configs
---

# copy-update-json.sh

Copies a module JSON file to the config directory and optionally updates fields.

## Usage

```bash
copy-update-json.sh <module-name> [--<field> <value>]...
```

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `module-name` | Name of the module | `identity` |
| `--<field> <value>` | Set JSON field to value (repeatable) | `--node "tappaas2"` |

## Examples

```bash
# Copy identity.json with default values
copy-update-json.sh identity

# Copy and modify fields
copy-update-json.sh identity --node "tappaas2" --cores 4
copy-update-json.sh nextcloud --memory 4096 --zone0 "trusted"
```

## What it does

1. Copies `./<module>.json` from current directory to `/home/tappaas/config/`
2. Automatically sets the `location` field to the module directory
3. Validates field names against `module-fields.json` schema
4. Applies `--<field> <value>` modifications to the copied JSON
5. Creates a `.orig` backup if modifications are made
6. Validates the resulting JSON is valid

## Notes

- Integer fields (per schema) are stored as JSON numbers
- String fields are stored as JSON strings
- Unknown field names will cause an error

## See Also

- [common-install-routines.sh](common-install-routines.md) - Shared library functions
- [Module Definition](../../architecture/cicd-design/module-structure.md#module-definition) - Module JSON fields
