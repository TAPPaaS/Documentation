---
title: n8n
description: Deploy n8n workflow automation platform
---

# n8n

n8n is a fair-code workflow automation platform that allows you to connect services, automate tasks, and build complex integrations.

## Features

- Visual workflow builder
- 400+ built-in integrations
- Custom code nodes (JavaScript/Python)
- Webhook triggers
- AI/LLM integration
- Self-hosted and private

## Architecture

| Component | Purpose |
|-----------|---------|
| n8n | Workflow engine |
| PostgreSQL | Data persistence |
| Docker/Podman | Container runtime |

## Prerequisites

- [ ] [Foundation](../foundation/index.md) complete
- [ ] DNS record configured
- [ ] Reverse proxy ready

## System Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| vCPU | 2 | 4 |
| RAM | 2 GB | 4 GB |
| Storage | 10 GB | 20 GB |

## Installation

### Deploy VM

```bash
cd ~/TAPPaaS/src/apps/n8n
./install.sh
```

### DNS Configuration

Add DNS record:

| Record | Type | Value |
|--------|------|-------|
| `n8n.yourdomain.com` | A | Your public IP |

### Reverse Proxy

Configure Caddy:

```
n8n.yourdomain.com {
    reverse_proxy n8n.mgmt.internal:5678
}
```

## Configuration

### Initial Setup

Access n8n at `https://n8n.yourdomain.com`

1. Create owner account
2. Set instance name
3. Configure basic settings

### Environment Variables

Key configuration options:

| Variable | Description |
|----------|-------------|
| `N8N_ENCRYPTION_KEY` | Encrypts credentials |
| `N8N_HOST` | Public hostname |
| `WEBHOOK_URL` | Webhook base URL |
| `N8N_SMTP_*` | Email settings |

### Authentication

Configure SSO with Authentik (recommended):

```bash
# Environment variables for OAuth
N8N_AUTH_OAUTH2_CLIENT_ID="your-client-id"
N8N_AUTH_OAUTH2_CLIENT_SECRET="your-client-secret"
N8N_AUTH_OAUTH2_AUTHORIZE_URL="https://authentik.yourdomain.com/application/o/authorize/"
N8N_AUTH_OAUTH2_ACCESS_TOKEN_URL="https://authentik.yourdomain.com/application/o/token/"
```

## Building Workflows

### Create a Workflow

1. Click **Add Workflow**
2. Add trigger node (Schedule, Webhook, etc.)
3. Add action nodes
4. Connect nodes
5. Activate workflow

### Example: Daily Report

```
Schedule Trigger (9 AM)
    ↓
HTTP Request (Fetch data)
    ↓
Code Node (Process data)
    ↓
Email Node (Send report)
```

### AI Integration

Connect to your AI stack:

1. Add **HTTP Request** node
2. Configure LiteLLM endpoint:
   - URL: `http://litellm.mgmt.internal:4000/v1/chat/completions`
   - Method: POST
   - Headers: Authorization: Bearer `<your-key>`
3. Use AI response in workflow

## Common Integrations

### Webhooks

Expose webhooks for external triggers:

```
https://n8n.yourdomain.com/webhook/<webhook-id>
```

### Database Connections

Connect to databases for data operations:

- PostgreSQL
- MySQL
- MongoDB
- SQLite

### API Integrations

Built-in nodes for popular services:

- Slack, Discord, Telegram
- Google Workspace
- Microsoft 365
- GitHub, GitLab
- AWS, Azure, GCP

## Monitoring

### Check Status

```bash
# Service status
systemctl status n8n

# Container logs
podman logs n8n

# Execution history
# View in n8n web interface
```

### Execution Logs

Review workflow executions in the n8n interface:

1. Navigate to **Executions**
2. Filter by status, workflow, or date
3. Debug failed executions

## Backup

### Automated Backup

PostgreSQL data is included in VM backups via PBS.

### Export Workflows

Export workflows for version control:

1. Select workflow
2. Click **...** → **Download**
3. Save JSON file

### Restore Workflows

```bash
# Import via CLI
n8n import:workflow --input=workflow.json
```

## Troubleshooting

### Workflow Fails

- Check execution logs for errors
- Verify credentials are valid
- Test nodes individually
- Check external service status

### Webhook Not Triggering

- Verify webhook URL is accessible
- Check firewall rules
- Confirm reverse proxy configuration

### Performance Issues

- Increase VM resources
- Optimize workflow design
- Use sub-workflows for complex logic

## Security Best Practices

- Use Authentik SSO for access control
- Store credentials in n8n credential manager
- Limit webhook exposure
- Regular workflow audits
- Keep n8n updated

## Next Steps

- Explore built-in workflow templates
- Connect to [AI Stack](../ai-stack/index.md) for AI workflows
- Integrate with [Home Assistant](../home-stack/home-assistant.md) for home automation
