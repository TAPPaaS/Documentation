---
title: Introduction to TAPPaaS
description: Learn what TAPPaaS is, its core concepts, and how it simplifies application deployment and management
---

# Introduction to TAPPaaS

TAPPaaS (The Application Platform as a Service) is an open-source platform that simplifies deploying, managing, and scaling applications on Kubernetes. It provides a streamlined developer experience while maintaining the power and flexibility of cloud-native infrastructure.

## What is TAPPaaS?

TAPPaaS bridges the gap between complex Kubernetes infrastructure and developer productivity. It provides:

- **Simple Application Deployment** - Deploy applications without writing complex Kubernetes manifests
- **Developer Self-Service** - Empower developers to manage their own applications
- **Platform Flexibility** - Support any language, any framework, any deployment pattern
- **Operational Simplicity** - Reduce the operational burden of managing cloud-native applications

!!!tip "Quick Start"
    Ready to try TAPPaaS? Start with our [Installation Guide](../installation/index.md) to get up and running in minutes.

---

## Core Concepts

Understanding these key concepts will help you get the most out of TAPPaaS:

### Applications

Applications are the primary unit of deployment in TAPPaaS. This is also called a "Module". Each Module represents a complete, deployable software project with its own configuration, dependencies, and runtime requirements.

### Platform as a Service

TAPPaaS provides a PaaS layer on top of physical hardware, abstracting away infrastructure complexity and maintaining all the modern complexity of backup, firewall, identity management, high availability, reverse proxy, ...

The hardware can be hosted in your own data center or in a local hosting provider

TAPPaaS scale from a medium sized single server system over a 3 node redundant cluster up to 10's of servers in a single platform cluster

### Cloud-Native Architecture

Built from the ground up for simplicity of deploying application, TAPPaaS leverages modern cloud-native patterns including:

- Declarative configuration
- Automated scaling and self-healing
- Service discovery and load balancing
- DevOps deployment pattern for autonomous updates

### Developer Experience

TAPPaaS prioritizes developer productivity through:

- Intuitive CLI and API interfaces
- Convention over configuration
- Built-in best practices
- Fast feedback loops

---

## How TAPPaaS Works

TAPPaaS operates through a simple, powerful workflow:

### 1. Configure Your Application

Define your application using simple configuration files that specify:

- Application code location
- Deployment dependencies
- Runtime environment settings
- Resource requirements

### 2. Deploy to Platform

Use the TAPPaaS CLI to deploy your application. TAPPaaS handles:

- Building Virtual machines for module
- Configuring networking and ingress
- Setting up backup, monitoring and logging

### 3. Manage and Scale

Once deployed, TAPPaaS provides tools to:

- Monitor application health and performance
- Scale applications manually or automatically
- View logs and debug issues
- Update applications with zero-downtime deployments

### 4. Operate with Confidence

TAPPaaS manages the operational complexity:

- Health checks and automatic recovery
- Rolling updates and rollbacks
- Resource optimization
- Security best practices

---

## When to Use TAPPaaS

TAPPaaS is ideal for:

<div class="grid" markdown>

!!! example "Development Teams"
    Teams that want to focus on building applications rather than managing infrastructure.

!!! example "Platform Engineers"
    Organizations building internal developer platforms to standardize application deployment.

!!! example "Multi-Tenant Environments"
    Organizations needing to support multiple teams or projects on shared infrastructure.

</div>

---

## Key Features

### Simple Deployment Model

Deploy applications with minimal configuration using familiar tools and workflows.

### Multi-Language Support

TAPPaaS supports applications written in any language including Node.js, Python, Java, Go, Ruby, and more.

### Built-in Best Practices

TAPPaaS incorporates cloud-native best practices including 12-factor app principles, secure defaults, and production-ready configurations.

### Extensible Architecture

While TAPPaaS provides sensible defaults, it remains flexible and extensible for advanced use cases.

### Open Source

Fully open source under the Mozilla Public License 2.0, with an active community and transparent development process.

---

## Getting Started

Ready to start using TAPPaaS? Here's your path forward:

<div class="grid cards" markdown>

-   :material-lightbulb-outline:{ .lg .middle } **Understand the Vision**

    ---

    Learn about the problem TAPPaaS solves and who benefits.

    [:octicons-arrow-right-24: Read the Vision](vision.md)

-   :material-chart-timeline-variant:{ .lg .middle } **Explore Architecture**

    ---

    Understand how TAPPaaS is built and how components interact.

    [:octicons-arrow-right-24: Architecture Overview](architecture.md)

-   :material-download:{ .lg .middle } **Install TAPPaaS**

    ---

    Get TAPPaaS running on your infrastructure.

    [:octicons-arrow-right-24: Installation Guide](../installation/index.md)

-   :material-rocket-launch:{ .lg .middle } **Deploy Your First App**

    ---

    Follow our quickstart to deploy your first application.

    [:octicons-arrow-right-24: Quick Start](../installation/index.md)

</div>

---

## Learning Paths

Choose your path based on your role and goals:

### For Developers

1. Read the [Vision](vision.md) to understand TAPPaaS's approach
2. Follow the [Quick Start](../installation/index.md) to deploy your first app
3. Explore language-specific deployment examples
4. Learn about configuration and scaling options

### For Platform Engineers

1. Review the [Architecture Overview](architecture.md) to understand system design
2. Complete the [Installation Guide](../installation/index.md)
3. Study operational best practices and monitoring
4. Configure multi-tenant environments and access controls

### For Decision Makers

1. Read the [Vision & Problem Statement](vision.md)
2. Review the [Architecture Overview](architecture.md)
3. Understand the [open source license](../about/license.md)
4. Explore deployment scenarios and success stories

---

## Community and Support

TAPPaaS is a community-driven project. Get involved:

- **Contribute** - Help improve TAPPaaS through [code contributions](../community/contributing.md)
- **Report Issues** - Found a bug? [Open an issue](https://github.com/TAPPaaS/Documentation/issues)
- **Ask Questions** - Get help from the community
- **Share Feedback** - Tell us about your experience with TAPPaaS

---

## Next Steps

Now that you understand what TAPPaaS is, explore these topics:

- [Vision & Problem Statement](vision.md) - Understand why TAPPaaS exists
- [Architecture Overview](architecture.md) - Learn how TAPPaaS is built
- [Getting Started](../installation/index.md) - Install and deploy your first application
- [About TAPPaaS](../about/index.md) - Learn about the project history and governance
