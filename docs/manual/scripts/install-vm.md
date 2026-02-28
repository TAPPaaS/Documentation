---
title: install-vm.sh
description: VM creation library for module install scripts
---

# install-vm.sh

Creates a VM on Proxmox using a module's JSON configuration. This is a library script meant to be sourced by module install scripts.

## Usage

Source this file in module install scripts:

```bash
. /home/tappaas/bin/install-vm.sh
```

## What it does

1. Sources `copy-update-json.sh` to copy the module JSON to config
2. Sources `common-install-routines.sh` to load config functions
3. Validates the JSON configuration
4. Copies the JSON to the target Proxmox node
5. Calls `Create-TAPPaaS-VM.sh` on the node to create the VM
6. Cleans up the temporary JSON file on the node

## Exported variables after sourcing

- `VMNAME` - VM name from configuration
- `VMID` - VM ID from configuration
- `NODE` - Proxmox node where VM is created
- `ZONE0NAME` - Primary network zone

## Example module install.sh

```bash
#!/bin/envbash
set -euo pipefail

# Create the VM
. /home/tappaas/bin/install-vm.sh

# Get additional config values
IMAGE_TYPE="$(get_config_value 'imageType' 'clone')"

# Run post-install steps
/home/tappaas/bin/update-os.sh "${VMNAME}" "${VMID}" "${NODE}"
```

## See Also

- [update-os.sh](update-os.md) - Update VM operating system
- [common-install-routines.sh](common-install-routines.md) - Shared library functions
