---
title: LiteLLM
description: Deploy LiteLLM as a unified API gateway for LLM providers
---

# LiteLLM

LiteLLM provides a unified API gateway for multiple LLM providers, allowing you to use a single API to access OpenAI, Anthropic, local models, and more.

## Features

- Unified OpenAI-compatible API
- Support for 100+ LLM providers
- Request caching with Redis
- Usage tracking and analytics
- Cost management
- Load balancing across models

## Architecture

| Component | Purpose |
|-----------|---------|
| LiteLLM Proxy | API gateway (4 workers) |
| PostgreSQL | Configuration and metrics |
| Redis | Response caching |

## Prerequisites

- [ ] [Foundation](../foundation/index.md) complete
- [ ] API keys for desired providers
- [ ] DNS record configured

## System Requirements

| Users | vCPU | RAM | Storage |
|-------|------|-----|---------|
| 100 | 4 | 4 GB | 20 GB |
| 250 | 4 | 8 GB | 30 GB |
| 500+ | 8 | 16 GB | 50 GB |

## Installation

### Deploy VM

```bash
cd ~/TAPPaaS/src/apps/litellm
./install.sh
```

### DNS Configuration

Add DNS record:

| Record | Type | Value |
|--------|------|-------|
| `llm.yourdomain.com` | A | Your public IP |

### Reverse Proxy

Configure Caddy:

```
llm.yourdomain.com {
    reverse_proxy litellm.mgmt.internal:4000
}
```

## Configuration

### Add API Keys

Configure provider API keys via the admin interface or configuration file:

```yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: openai/gpt-4
      api_key: sk-...

  - model_name: claude-3
    litellm_params:
      model: anthropic/claude-3-opus-20240229
      api_key: sk-ant-...

  - model_name: local-llama
    litellm_params:
      model: ollama/llama2
      api_base: http://ollama.mgmt.internal:11434
```

### Master Key

A master API key is generated during installation. Retrieve it:

```bash
cat /etc/litellm/master_key
```

Use this key for admin access and to create user keys.

## Supported Providers

| Provider | Models | Notes |
|----------|--------|-------|
| OpenAI | GPT-3.5, GPT-4 | Most popular |
| Anthropic | Claude 3 family | Strong reasoning |
| OpenRouter | Multiple | Aggregator |
| Perplexity | pplx-* | Search-enhanced |
| Ollama | Local models | Self-hosted |

## Usage

### API Access

Use the LiteLLM endpoint like OpenAI:

```python
import openai

client = openai.OpenAI(
    base_url="https://llm.yourdomain.com/v1",
    api_key="your-litellm-key"
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Caching

Redis caching reduces costs and latency:

- Identical requests return cached responses
- 60-80% reduction in API calls for common queries
- Configurable cache TTL

## Monitoring

### View Usage

Access the admin dashboard:

```
https://llm.yourdomain.com/ui
```

### Metrics

```bash
# Check service status
systemctl status litellm

# View logs
journalctl -u litellm -f

# Check container stats
podman stats litellm
```

## Cost Management

### Set Budgets

Configure spending limits per user or team:

```yaml
budget_config:
  - user_id: team-dev
    max_budget: 100.00
    time_period: monthly
```

### Track Spending

View cost breakdown in the admin dashboard or via API:

```bash
curl -H "Authorization: Bearer $MASTER_KEY" \
  https://llm.yourdomain.com/spend/logs
```

## Backup

Daily automated backups include:

- PostgreSQL database
- Redis snapshots
- Configuration files

Retention: 30 days

### Restore

```bash
cd ~/TAPPaaS/src/apps/litellm
./restore.sh
```

## Troubleshooting

### Provider Errors

- Verify API key is valid
- Check provider status page
- Review rate limits

### Slow Responses

- Check Redis cache hit rate
- Verify network connectivity
- Consider adding more workers

### Database Issues

```bash
# Check PostgreSQL
systemctl status postgresql

# Check connections
psql -U litellm -c "SELECT count(*) FROM pg_stat_activity;"
```

## Next Steps

- Deploy [OpenWebUI](openwebui.md) for user interface
- Add local models with [Ollama](ollama.md)
