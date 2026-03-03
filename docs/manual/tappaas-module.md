---
title: TAPPaaS Module
description: Understanding the essential structure of a TAPPaaS module
---

# TAPPaaS Module

A TAPPaaS module is a self-contained unit that defines a service or application within the TAPPaaS platform.

## Essential Structure

```
<module-name>/
├── <module-name>.json    # Module definition and configuration
├── install.sh            # Installation script (optional)
├── update.sh             # Update script (optional)
├── delete.sh             # Deletion script (optional)
└── services/             # Services provided by this module
    └── <service-name>/
        ├── install-service.sh
        ├── update-service.sh
        └── delete-service.sh
```

## Module Definition

The `<module-name>.json` file defines the module's configuration, including:

- **Metadata**: Version, description, maintainer, status
- **Dependencies**: Services this module requires from other modules
- **Provides**: Services this module offers to other modules
- **VM Configuration**: Resources, networking, and storage settings

## Lifecycle

1. **Install**: Creates the module's VM and configures its services
2. **Update**: Applies configuration changes and updates the module
3. **Delete**: Removes the module and cleans up resources

