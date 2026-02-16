---
title: Installation
description: Install TAPPaaS on your Kubernetes cluster
---

# Installation

This guide walks you through installing TAPPaaS on your Kubernetes cluster.

## Prerequisites

- Kubernetes cluster v1.26 or later
- `kubectl` configured with cluster access
- Helm 3.x
- Cluster admin permissions

## Installation Methods

### Using Helm (Recommended)

```bash
# Add the TAPPaaS Helm repository
helm repo add tappaas https://charts.tappaas.org
helm repo update

# Install TAPPaaS
helm install tappaas tappaas/tappaas \
  --namespace tappaas-system \
  --create-namespace
```

### Using kubectl

```bash
# Apply the TAPPaaS manifests
kubectl apply -f https://raw.githubusercontent.com/TAPPaaS/tappaas/main/deploy/install.yaml
```

## Verify Installation

Check that all components are running:

```bash
kubectl get pods -n tappaas-system
```

All pods should show `Running` status.

## Next Steps

- [Quick Start](quickstart.md) - Deploy your first application
- [Configuration](../docs/index.md) - Configure TAPPaaS for your needs
