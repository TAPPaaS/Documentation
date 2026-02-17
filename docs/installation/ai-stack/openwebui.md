---
title: OpenWebUI
description: Deploy OpenWebUI for AI interactions
---

# OpenWebUI

OpenWebUI provides a feature-rich web interface for interacting with large language models, similar to ChatGPT but self-hosted.

## Features

- Chat interface with conversation history
- Multiple model support
- Document upload and RAG capabilities
- User management and authentication
- Customizable system prompts
- API access for integrations

## Architecture

The OpenWebUI deployment includes:

| Component | Purpose |
|-----------|---------|
| OpenWebUI | Web application (v0.7.2+) |
| PostgreSQL | Data persistence (15.x) |
| Redis | Caching and coordination (7.x) |
| Podman | Container runtime |

## Prerequisites

- [ ] [Foundation](../foundation/index.md) complete
- [ ] DNS record for OpenWebUI
- [ ] Reverse proxy configured

## System Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| vCPU | 2 | 4 |
| RAM | 4 GB | 8 GB |
| Storage | 20 GB | 50 GB |

## Installation

### Deploy VM

From tappaas-cicd:

```bash
cd ~/TAPPaaS/src/apps/openwebui
./install.sh
```

### DNS Configuration

Add DNS record:

| Record | Type | Value |
|--------|------|-------|
| `chat.yourdomain.com` | A | Your public IP |

### Reverse Proxy

Configure Caddy in OPNsense:

```
chat.yourdomain.com {
    reverse_proxy openwebui.mgmt.internal:8080
}
```

## Configuration

### Initial Setup

Access OpenWebUI at `https://chat.yourdomain.com`

1. Create admin account on first access
2. Configure authentication settings
3. Add LLM connections

### Connect to LiteLLM

Configure OpenWebUI to use LiteLLM as backend:

1. Navigate to **Settings** → **Connections**
2. Add OpenAI-compatible endpoint:
   - URL: `http://litellm.mgmt.internal:4000/v1`
   - API Key: Your LiteLLM master key

### Connect to Ollama

For local models via Ollama:

1. Navigate to **Settings** → **Connections**
2. Add Ollama endpoint:
   - URL: `http://ollama.mgmt.internal:11434`

## User Management

### Create Users

1. Navigate to **Admin** → **Users**
2. Click **Add User**
3. Set username, email, and role

### Roles

| Role | Capabilities |
|------|--------------|
| Admin | Full access, user management |
| User | Chat access, personal settings |

## Backup

Automated backups are configured for:

| Component | Schedule | Retention |
|-----------|----------|-----------|
| PostgreSQL | Daily | 30 days |
| Redis | Daily | 30 days |
| Container data | Daily | 30 days |
| Environment files | Daily | 30 days |

### Manual Backup

```bash
# Backup PostgreSQL
pg_dump -U openwebui openwebui > backup.sql

# Backup Redis
redis-cli BGSAVE
```

## Maintenance

### View Logs

```bash
# OpenWebUI logs
podman logs openwebui

# PostgreSQL logs
journalctl -u postgresql
```

### Update

To update OpenWebUI:

```bash
cd ~/TAPPaaS/src/apps/openwebui
./update.sh
```

## Troubleshooting

### Cannot Connect to LLM

- Verify LiteLLM/Ollama is running
- Check network connectivity
- Verify API key is correct
- Check firewall rules

### Slow Performance

- Increase VM resources
- Check Redis caching status
- Review PostgreSQL performance

### Authentication Issues

- Verify user credentials
- Check authentication provider settings
- Review application logs

## Security Notes

!!! warning "Development Configuration"
    The default PostgreSQL configuration uses trust authentication without passwords. This is suitable for development and internal networks only. For production or public-facing deployments, configure proper database authentication.

## Next Steps

- Configure [LiteLLM](litellm.md) for multi-provider access
- Add local models with [Ollama](ollama.md)
