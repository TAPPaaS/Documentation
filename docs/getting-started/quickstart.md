---
title: Quick Start
description: Deploy your first application with TAPPaaS in minutes
---

# Quick Start

Deploy your first application with TAPPaaS in under 5 minutes.

## Prerequisites

- TAPPaaS installed ([Installation Guide](installation.md))
- `tappaas` CLI installed

## Step 1: Create an Application

```bash
# Create a new application
tappaas app create my-first-app
```

## Step 2: Deploy Your Code

```bash
# Deploy from a Git repository
tappaas app deploy my-first-app \
  --git https://github.com/your-org/your-app.git

# Or deploy from local directory
tappaas app deploy my-first-app --source .
```

## Step 3: Check Status

```bash
# View application status
tappaas app status my-first-app
```

## Step 4: Access Your Application

```bash
# Get the application URL
tappaas app url my-first-app
```

## What's Next?

- Learn about [application configuration](../docs/index.md)
- Set up [custom domains](../docs/index.md)
- Configure [scaling and resources](../docs/index.md)

!!! tip "Need Help?"
    Join our [community](../community/contributing.md) or check the [documentation](../docs/index.md) for more details.
