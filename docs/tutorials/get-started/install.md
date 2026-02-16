---
title: Install TAPPaaS
description: Step-by-step guide to installing TAPPaaS in your Kubernetes cluster
---

# Install TAPPaaS

**Estimated Time**: 15-20 minutes | **Difficulty**: Beginner

This tutorial walks you through installing TAPPaaS in your Kubernetes cluster using Helm, the recommended installation method. By the end, you'll have a fully functional TAPPaaS installation ready to deploy applications.

## What You'll Learn

- How to install TAPPaaS using Helm
- How to verify the installation
- Understanding TAPPaaS components
- Basic post-installation configuration

## Prerequisites

Before you begin, ensure you have:

- **Kubernetes cluster** (version 1.24 or higher)
    - At least 4 CPU cores and 8GB RAM available
    - CNCF-certified Kubernetes distribution
- **kubectl** CLI installed and configured
    - Run `kubectl version` to verify
    - Cluster admin access recommended
- **Helm 3** (version 3.8 or higher)
    - Run `helm version` to verify
- **Internet access** from your cluster to pull container images

!!! tip "Don't Have a Cluster?"
    For local development, we recommend [minikube](https://minikube.sigs.k8s.io/) or [kind](https://kind.sigs.k8s.io/). Start a cluster with:
    ```bash
    # Using minikube
    minikube start --cpus=4 --memory=8192

    # Using kind
    kind create cluster --config kind-config.yaml
    ```

## Installation Methods

TAPPaaS can be installed using two methods:

1. **Helm** (Recommended) - Simplifies installation and upgrades
2. **kubectl** - Direct YAML manifest installation

This tutorial focuses on the Helm method, which is recommended for most users.

---

## Step 1: Verify Cluster Access

First, verify that you can access your Kubernetes cluster and have sufficient permissions.

```bash
kubectl cluster-info
```

**Expected Output:**
```
Kubernetes control plane is running at https://...
CoreDNS is running at https://...
```

Check available resources:

```bash
kubectl get nodes
```

**Expected Output:**
```
NAME                STATUS   ROLES           AGE   VERSION
my-cluster-node-1   Ready    control-plane   5d    v1.28.0
```

!!! warning "Cluster Requirements"
    Ensure your cluster has sufficient resources. TAPPaaS requires at least 2GB RAM and 1 CPU core for the control plane components.

---

## Step 2: Create TAPPaaS Namespace

Create a dedicated namespace for TAPPaaS components:

```bash
kubectl create namespace tappas-system
```

**Expected Output:**
```
namespace/tappas-system created
```

Verify the namespace was created:

```bash
kubectl get namespace tappas-system
```

**Expected Output:**
```
NAME             STATUS   AGE
tappas-system    Active   5s
```

---

## Step 3: Add TAPPaaS Helm Repository

Add the official TAPPaaS Helm chart repository:

```bash
helm repo add tappas https://charts.tappas.io
```

**Expected Output:**
```
"tappas" has been added to your repositories
```

Update your Helm repositories to fetch the latest charts:

```bash
helm repo update
```

**Expected Output:**
```
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "tappas" chart repository
Update Complete. ⎈Happy Helming!⎈
```

Verify the TAPPaaS chart is available:

```bash
helm search repo tappas
```

**Expected Output:**
```
NAME                    CHART VERSION   APP VERSION     DESCRIPTION
tappas/tappas          1.0.0           1.0.0           TAPPaaS - The Application Platform as a Service
```

---

## Step 4: Install TAPPaaS with Helm

Install TAPPaaS using Helm with default configuration:

```bash
helm install tappas tappas/tappas \
  --namespace tappas-system \
  --create-namespace \
  --wait
```

**Expected Output:**
```
NAME: tappas
LAST DEPLOYED: Mon Feb 16 10:30:00 2026
NAMESPACE: tappas-system
STATUS: deployed
REVISION: 1
NOTES:
TAPPaaS has been installed successfully!

To get started, check the status of your installation:
  kubectl get pods -n tappas-system

For more information, visit https://docs.tappas.io
```

!!! info "Installation Options"
    The `--wait` flag ensures Helm waits for all resources to be ready before completing. This may take 2-5 minutes depending on your cluster.

### Custom Installation (Optional)

If you need to customize the installation, create a `values.yaml` file:

```yaml
# values.yaml
controller:
  replicas: 2
  resources:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi

builder:
  enabled: true
  storage:
    size: 10Gi

ingress:
  enabled: true
  className: nginx
```

Install with custom values:

```bash
helm install tappas tappas/tappas \
  --namespace tappas-system \
  --values values.yaml \
  --wait
```

---

## Step 5: Verify Installation

Check that all TAPPaaS components are running:

```bash
kubectl get pods -n tappas-system
```

**Expected Output:**
```
NAME                                    READY   STATUS    RESTARTS   AGE
tappas-controller-6d8b9f5c7d-x7k9m     1/1     Running   0          2m
tappas-builder-5c7d8b4f9e-p2n5k        1/1     Running   0          2m
tappas-registry-7f8c9d5e6a-q3m7n       1/1     Running   0          2m
tappas-database-0                       1/1     Running   0          2m
```

!!! success "All Pods Running"
    All pods should show `STATUS: Running` and `READY: 1/1`. If any pods show different status, see the Troubleshooting section below.

Verify the TAPPaaS API is accessible:

```bash
kubectl get service -n tappas-system
```

**Expected Output:**
```
NAME                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
tappas-controller   ClusterIP   10.96.100.50    <none>        8080/TCP   3m
tappas-builder      ClusterIP   10.96.100.51    <none>        8081/TCP   3m
tappas-registry     ClusterIP   10.96.100.52    <none>        5000/TCP   3m
```

Check Custom Resource Definitions (CRDs) were installed:

```bash
kubectl get crds | grep tappas
```

**Expected Output:**
```
applications.tappas.io           2026-02-16T10:30:00Z
builds.tappas.io                 2026-02-16T10:30:00Z
deployments.tappas.io            2026-02-16T10:30:00Z
routes.tappas.io                 2026-02-16T10:30:00Z
```

---

## Step 6: Install TAPPaaS CLI (Optional)

The TAPPaaS CLI provides a convenient way to interact with your installation:

=== "macOS"
    ```bash
    brew install tappas/tap/tappas-cli
    ```

=== "Linux"
    ```bash
    curl -sSL https://get.tappas.io/cli | bash
    ```

=== "Windows"
    ```powershell
    scoop bucket add tappas https://github.com/TAPPaaS/scoop-bucket
    scoop install tappas-cli
    ```

Verify the CLI installation:

```bash
tappas version
```

**Expected Output:**
```
TAPPaaS CLI version 1.0.0
```

Configure the CLI to use your cluster:

```bash
tappas config set-context --kubeconfig ~/.kube/config
```

**Expected Output:**
```
Context configured successfully
```

Test the connection:

```bash
tappas status
```

**Expected Output:**
```
TAPPaaS Status
--------------
Version:        1.0.0
Status:         Ready
Applications:   0
Builds:         0
```

---

## Understanding TAPPaaS Components

Your TAPPaaS installation includes several key components:

| Component | Purpose | Resource Type |
|-----------|---------|---------------|
| **Controller** | Manages application lifecycle and reconciliation | Deployment |
| **Builder** | Handles source-to-image builds using buildpacks | Deployment |
| **Registry** | Stores built container images | StatefulSet |
| **Database** | Stores application state and metadata | StatefulSet |

You can view detailed information about each component:

```bash
kubectl describe deployment tappas-controller -n tappas-system
```

---

## Post-Installation Configuration

### Configure Default Storage Class (Optional)

If your cluster doesn't have a default storage class, set one for TAPPaaS:

```bash
kubectl get storageclass
```

If no storage class is marked as default, set one:

```bash
kubectl patch storageclass <storage-class-name> \
  -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

### Configure Ingress (Optional)

To expose applications externally, configure an ingress controller. TAPPaaS works with any Kubernetes ingress controller.

Example with NGINX Ingress Controller:

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace
```

Update TAPPaaS to use ingress:

```bash
helm upgrade tappas tappas/tappas \
  --namespace tappas-system \
  --set ingress.enabled=true \
  --set ingress.className=nginx
```

### Enable Monitoring (Optional)

Install Prometheus and Grafana for monitoring:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

TAPPaaS automatically exports metrics that Prometheus can scrape.

---

## Troubleshooting

### Pods Not Starting

If pods remain in `Pending` or `CrashLoopBackOff` state:

```bash
# Check pod details
kubectl describe pod <pod-name> -n tappas-system

# Check logs
kubectl logs <pod-name> -n tappas-system
```

**Common issues:**

- **Insufficient resources**: Increase cluster resources or adjust TAPPaaS resource requests
- **Image pull errors**: Verify internet connectivity and image registry access
- **Storage issues**: Ensure a storage class is available

### Helm Installation Fails

If the Helm installation fails:

```bash
# Uninstall failed release
helm uninstall tappas -n tappas-system

# Check Helm release history
helm history tappas -n tappas-system

# Reinstall with verbose output
helm install tappas tappas/tappas \
  --namespace tappas-system \
  --debug \
  --wait
```

### CRDs Not Installed

If Custom Resource Definitions are missing:

```bash
# Manually install CRDs
kubectl apply -f https://raw.githubusercontent.com/TAPPaaS/TAPPaaS/main/install/crds.yaml
```

### Database Connection Issues

If applications can't connect to the database:

```bash
# Check database pod
kubectl get pod -n tappas-system -l app=tappas-database

# Check database logs
kubectl logs -n tappas-system -l app=tappas-database

# Test database connection
kubectl run -it --rm debug \
  --image=postgres:14 \
  --restart=Never \
  -- psql -h tappas-database.tappas-system.svc.cluster.local -U tappas
```

---

## Verify Installation Checklist

Before proceeding, verify:

- [ ] All pods in `tappas-system` namespace are running
- [ ] TAPPaaS CRDs are installed
- [ ] Services are accessible within the cluster
- [ ] (Optional) TAPPaaS CLI is installed and configured
- [ ] (Optional) Ingress controller is configured
- [ ] No error logs in component pods

---

## Next Steps

Congratulations! You've successfully installed TAPPaaS. Now you're ready to:

- **[Deploy Your First App](/tutorials/get-started/deploy-first-app/)** - Create and deploy a sample application
- **[Explore Configuration](/docs/configuration/)** - Learn about configuration options
- **[Review Architecture](/docs/architecture/)** - Understand TAPPaaS components in detail
- **[Check CLI Reference](/docs/cli/)** - Explore CLI commands

---

## Uninstalling TAPPaaS (Optional)

If you need to uninstall TAPPaaS:

!!! danger "Data Loss Warning"
    Uninstalling TAPPaaS will delete all applications, builds, and data. Back up any important data first.

```bash
# Uninstall using Helm
helm uninstall tappas -n tappas-system

# Delete namespace
kubectl delete namespace tappas-system

# Remove CRDs (optional, removes all custom resources)
kubectl delete crd applications.tappas.io
kubectl delete crd builds.tappas.io
kubectl delete crd deployments.tappas.io
kubectl delete crd routes.tappas.io
```

---

**Ready to deploy your first application?** Continue to [Deploy Your First App](/tutorials/get-started/deploy-first-app/).
