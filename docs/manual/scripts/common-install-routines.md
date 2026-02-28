---
title: common-install-routines.sh
description: Shared library for install scripts
---

# common-install-routines.sh

Shared library of functions and utilities for module installation scripts.

## Usage

Source this file in install scripts:

```bash
. /home/tappaas/bin/common-install-routines.sh <vmname>
```

## Features

- Color definitions for terminal output (YW, BL, RD, GN, etc.)
- `info()` - Print informational messages in green
- `warn()` - Print warning messages in yellow
- `error()` - Print error messages in red
- `get_config_value()` - Extract values from module JSON configuration
- `check_json()` - Validate a module JSON file against module-fields.json schema
- Validates that script runs on tappaas-cicd host
- Loads JSON configuration from `/home/tappaas/config/<vmname>.json`

## Example

```bash
. common-install-routines.sh mymodule
vmid=$(get_config_value "vmid")
cores=$(get_config_value "cores" "2")  # with default value
check_json /home/tappaas/config/mymodule.json || exit 1
```

## Available Functions

### get_config_value

Extract a value from the loaded module JSON configuration.

```bash
get_config_value <field> [default]
```

### check_json

Validate a JSON file against the module-fields.json schema.

```bash
check_json <json-file>
```

### info, warn, error

Print colored messages to terminal.

```bash
info "Installation complete"
warn "Optional feature not configured"
error "Installation failed"
```

## See Also

- [copy-update-json.sh](copy-update-json.md) - Copy and modify module JSON
- [install-vm.sh](install-vm.md) - VM creation library
