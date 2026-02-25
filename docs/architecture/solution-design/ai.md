---
title: AI
description: TAPPaaS AI stack integration
---

# AI Design

## AI Server

AI models, especially LLMs, come in many variants, and typically you need to specialize what models you are running. The models require GPU resources and will serve a number of use cases across TAPPaaS.

### Architecture

The architecture uses an LLM server setup:

- One VM on a machine with resources for AI, running **Ollama** as the central point for loading and accessing LLMs
- No users directly interact with this server - interactions are done via AI client programs

---

## AI Clients

Several client types exist in the TAPPaaS ecosystem:

### Chat Clients

TAPPaaS installs **OpenWebUI** as default in a dedicated VM. This provides:

- Web-based chat interface for interacting with LLMs
- RAG (Retrieval Augmented Generation) capabilities via SearXNG

### Workflow Automation

**n8n** provides workflow automation with AI capabilities, allowing:

- Automated processing pipelines
- Integration with other TAPPaaS services
- Custom AI-powered workflows

### Application Integration

Regular clients that need OpenAI API access include:

- **Home Assistant** - Home butler function for smart home automation
- **Immich** - Picture classification and search capabilities
