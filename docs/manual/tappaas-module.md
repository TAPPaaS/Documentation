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
├── install.sh            # Module specific installation script
├── update.sh             # Module specific Update script
├── pre-update.sh         # Module specific Update script run before service updates
├── delete.sh             # Deletion script (optional)
└── services/             # Services provided by this module
    └── <service-name>/
        ├── install-service.sh called when a module that depends on this module is installed
        ├── update-service.sh
        └── delete-service.sh
```

## Module Definition

The `<module-name>.json` file defines the module's configuration, including:

- **Metadata**: Version, description, maintainer, status
- **Dependencies**: Services this module requires from other modules
- **Provides**: Services this module offers to other modules
- **VM Configuration**: Resources, networking, and storage settings

---

For detailed documentation on module fields and scripts, see [Module Structure](../architecture/cicd-design/module-structure.md).
