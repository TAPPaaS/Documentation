---
title: Introduction to TAPPaaS
description: Learn what TAPPaaS is, its core concepts, and how it simplifies self-hosted infrastructure
---

# Introduction to TAPPaaS

TAPPaaS (Trusted Automated Private Platform as a Service) is an open-source platform that simplifies deploying, managing, and maintaining self-hosted applications on Proxmox virtualization. It provides enterprise-class capabilities without the complexity.

## What is TAPPaaS?

TAPPaaS bridges the gap between complex IT infrastructure and practical usability. It provides:

- **Simple Deployment** - Deploy applications without deep infrastructure expertise
- **Integrated Security** - Firewall, identity management, and network segmentation built-in
- **Automated Backup** - 3-2-1 backup strategy with disaster recovery
- **Operational Simplicity** - Reduce the operational burden of managing self-hosted infrastructure

!!!tip "Quick Start"
    Ready to try TAPPaaS? Start with our [Installation Guide](../installation/index.md) to get up and running.

---

## Core Concepts

Understanding these key concepts will help you get the most out of TAPPaaS:

### Module / Applications

A module is the primary unit of deployment in TAPPaaS. Often a module will have a single primary application at the center of the module. Each module represents a complete, deployable software project with its own configuration, dependencies, and runtime requirements.

### Platform as a Service

TAPPaaS provides a PaaS layer on top of physical hardware, abstracting away infrastructure complexity and maintaining all the modern complexity of backup, firewall, identity management, high availability, reverse proxy, and more.

The hardware can be hosted in your own data center or in a local hosting provider.

TAPPaaS scales from a medium sized single server system over a 3 node redundant cluster up to 10's of servers in a single platform cluster.

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

Use the TAPPaaS CI/CD system to deploy your application. TAPPaaS handles:

- Building Virtual machines for each module
- Configuring networking and ingress
- Setting up backup, monitoring and logging

### 3. Manage and Scale

Once deployed, TAPPaaS provides tools to:

- Monitor application health and performance
- Scale applications across nodes
- View logs and debug issues
- Update applications with managed deployments

### 4. Operate with Confidence

TAPPaaS manages the operational complexity:

- Health checks and automatic recovery
- Rolling updates and rollbacks
- Resource optimization
- Security best practices

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

    [:octicons-arrow-right-24: Architecture Overview](../docs/index.md)

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
