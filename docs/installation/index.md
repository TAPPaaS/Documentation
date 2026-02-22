---
title: Installation Overview
description: Complete guide to installing and configuring TAPPaaS
---

# Installation Overview

TAPPaaS is a set of interlinked foundational infrastructure modules and platform services that are built and configured to work together. This guide walks you through the complete installation process.

## Installation Process

The installation involves three primary steps:

### Step 1: Hardware Selection

Select and acquire the appropriate hardware for your deployment. Review sizing guidelines and choose between single-node or multi-node configurations.

[:octicons-arrow-right-24: Hardware Selection](hardware-selection.md)

### Step 2: Preparation

Prepare your environment before installation. This includes network planning, DNS configuration, and gathering required credentials.

[:octicons-arrow-right-24: Preparation](preparation.md)

### Step 3: Stack Deployment

Deploy AI, Productivity, and other relevant stacks:

| Stack | Description |
|-------|-------------|
| **[AI Stack](ai-stack/index.md)** | Local AI capabilities: OpenWebUI, LiteLLM, Ollama |
| **[Productivity Stack](productivity-stack/index.md)** | Workflow automation: n8n, Nextcloud, Karakeep |
| **[Home Stack](home-stack/index.md)** | Home automation: Home Assistant |

## Prerequisites

Before starting, ensure you have:

- A reliable wired internet connection
- A registered domain name with DNS management access
- Hardware meeting the [minimum requirements](hardware-selection.md)
- A strong root password for hypervisor and firewall systems

## Ongoing Operations

After installation, regular maintenance includes:

- Periodic execution of update scripts
- Continuous health monitoring
- Backup verification

## Need Help?

- Check the [FAQ](../community/faq.md) for common questions
- Visit [Community Support](../community/support.md) for assistance
