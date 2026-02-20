---
title: FAQ
description: Frequently asked questions about TAPPaaS
---

# Frequently Asked Questions

Find answers to common questions about TAPPaaS.

---

## General

### What is TAPPaaS?

TAPPaaS (The Application Platform as a Service) is an open-source platform designed to simplify deploying and managing applications on Kubernetes. It provides a developer-friendly interface while leveraging the power and flexibility of Kubernetes underneath.

### Is TAPPaaS free to use?

Yes! TAPPaaS is open source software licensed under the [Mozilla Public License 2.0](../about/license.md). You can use, modify, and distribute it freely.

### How is TAPPaaS different from other PaaS solutions?

TAPPaaS differentiates itself by:

- **Open Source**: Full transparency and community-driven development
- **Kubernetes Native**: Builds on Kubernetes rather than abstracting it away
- **Self-Hosted**: Run on your own infrastructure with full control
- **Extensible**: Plugin system for custom integrations

See our [Architecture Overview](../docs/index.md) for more details.

### What Kubernetes versions are supported?

TAPPaaS supports Kubernetes 1.26 and later. We recommend using a recent stable version for the best experience.

---

## Installation

### What are the system requirements?

**Minimum requirements:**

- Kubernetes cluster v1.26+
- 2 CPU cores available for TAPPaaS
- 4GB RAM available for TAPPaaS
- `kubectl` configured with cluster access
- Helm 3.x

**Recommended for production:**

- High-availability Kubernetes cluster
- 4+ CPU cores for TAPPaaS
- 8GB+ RAM for TAPPaaS
- Persistent storage for state

### Can I install TAPPaaS on my local machine?

Yes! You can use local Kubernetes distributions like:

- **minikube**
- **kind** (Kubernetes in Docker)
- **Docker Desktop** with Kubernetes enabled
- **k3s** / **k3d**

See the [Installation Guide](../installation/index.md) for details.

### How do I upgrade TAPPaaS?

Use Helm to upgrade:

```bash
helm repo update
helm upgrade tappaas tappaas/tappaas -n tappaas-system
```

Check the official documentation for upgrade procedures.

---

## Deployment

### What programming languages are supported?

TAPPaaS supports any language that can run in a container:

- **Built-in buildpacks**: Node.js, Python, Go, Java, Ruby, PHP
- **Custom Dockerfiles**: Any language or runtime
- **Pre-built images**: Any OCI-compatible container image

### How do I deploy a private Git repository?

Configure Git credentials as a Kubernetes secret:

```bash
kubectl create secret generic git-credentials \
  --from-literal=username=your-username \
  --from-literal=password=your-token \
  -n tappaas-system
```

Then reference the secret in your application configuration.

### Can I deploy multiple applications?

Yes! TAPPaaS is designed for multi-application environments. Each application is isolated with its own:

- Configuration
- Resources
- Networking
- Scaling settings

### How do I rollback a deployment?

```bash
# List deployment history
tappaas releases list my-app

# Rollback to a specific version
tappaas rollback my-app --revision 3
```

---

## Configuration

### How do I set environment variables?

There are several ways:

**CLI:**
```bash
tappaas config set my-app ENV_VAR=value
```

**Application manifest:**
```yaml
env:
  - name: DATABASE_URL
    value: postgres://...
```

**From secrets:**
```yaml
env:
  - name: API_KEY
    valueFrom:
      secretKeyRef:
        name: my-secrets
        key: api-key
```

### How do I configure custom domains?

1. Add the domain to your application:
   ```bash
   tappaas domains add my-app example.com
   ```

2. Configure DNS to point to your TAPPaaS ingress

3. TLS certificates are automatically provisioned via Let's Encrypt

See the documentation for custom domain configuration details.

### How do I configure autoscaling?

```yaml
# In your application manifest
scaling:
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: cpu
      target: 70
    - type: memory
      target: 80
```

---

## Operations

### How do I view application logs?

```bash
# Stream logs
tappaas logs my-app -f

# Show last 100 lines
tappaas logs my-app --tail 100

# Show logs from a specific time
tappaas logs my-app --since 1h
```

### How do I access my application's shell?

```bash
tappaas exec my-app -- /bin/sh
```

### How do I backup my applications?

TAPPaaS stores application configuration in Kubernetes. Back up using:

1. **Kubernetes backups**: Use Velero or similar tools
2. **GitOps**: Store configuration in Git
3. **Export**: `tappaas export my-app > my-app.yaml`

See the operations documentation for backup and recovery procedures.

### How do I monitor TAPPaaS?

TAPPaaS exposes Prometheus metrics. Integrate with:

- **Prometheus** for metrics collection
- **Grafana** for visualization
- **Alertmanager** for alerting

See the operations documentation for monitoring setup.

---

## Troubleshooting

### My application won't deploy

Check these common issues:

1. **Build errors**: Check build logs with `tappaas logs my-app --build`
2. **Resource limits**: Ensure enough CPU/memory is available
3. **Image pull errors**: Verify registry credentials
4. **Health check failures**: Check application health endpoints

See the [Support](support.md) page for troubleshooting help.

### Pods are stuck in Pending

Usually indicates resource constraints:

```bash
kubectl describe pod <pod-name> -n <namespace>
```

Look for events explaining why scheduling failed.

### I'm getting 502/503 errors

Common causes:

- Application isn't ready (check health probes)
- Application crashed (check logs)
- Resource exhaustion (check metrics)
- Ingress misconfiguration

---

## Community

### How can I contribute?

We welcome contributions! See our [Contributing Guide](contributing.md) for:

- Code contributions
- Documentation improvements
- Bug reports
- Feature requests

### Where can I get help?

- **Documentation**: You're already here!
- **GitHub Discussions**: [Ask questions](https://github.com/TAPPaaS/TAPPaaS/discussions)
- **GitHub Issues**: [Report bugs](https://github.com/TAPPaaS/TAPPaaS/issues)

See [Support](support.md) for more options.

### Is there commercial support?

TAPPaaS is a community project. For commercial support options, see the [Support page](support.md).

---

## Still Have Questions?

If your question isn't answered here:

1. Search the [documentation](../index.md)
2. Check [GitHub Discussions](https://github.com/TAPPaaS/TAPPaaS/discussions)
3. Ask a new question in the community

[:octicons-comment-discussion-24: Ask the Community](https://github.com/TAPPaaS/TAPPaaS/discussions/new?category=q-a){ .md-button .md-button--primary }
