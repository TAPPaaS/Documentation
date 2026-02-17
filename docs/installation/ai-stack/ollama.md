---
title: Ollama
description: Deploy Ollama for local LLM inference
---

# Ollama

Ollama provides an easy way to run large language models locally, offering an OpenAI-compatible API for seamless integration.

## Features

- Simple model management
- OpenAI-compatible API
- Support for popular open models
- GPU acceleration support
- Low resource overhead

## Supported Models

| Model | Parameters | RAM Required | Use Case |
|-------|------------|--------------|----------|
| Llama 3.2 | 1B-3B | 4-6 GB | Fast responses |
| Llama 3.1 | 8B | 8-12 GB | General purpose |
| Llama 3.1 | 70B | 48+ GB | High quality |
| Mistral | 7B | 8 GB | Efficient |
| CodeLlama | 7B-34B | 8-32 GB | Code generation |
| Phi-3 | 3.8B | 4-6 GB | Compact |

## Prerequisites

- [ ] [Foundation](../foundation/index.md) complete
- [ ] Sufficient RAM for chosen models
- [ ] GPU recommended for performance

## System Requirements

| Configuration | RAM | GPU | Models |
|---------------|-----|-----|--------|
| Minimal | 8 GB | None | 7B quantized |
| Standard | 16 GB | Optional | 7B-13B |
| Performance | 32+ GB | Recommended | 13B-70B |

## Installation

### Deploy VM

```bash
cd ~/TAPPaaS/src/apps/ollama
./install.sh
```

### GPU Passthrough (Optional)

For GPU acceleration, configure Proxmox GPU passthrough:

1. Enable IOMMU in BIOS
2. Configure Proxmox for PCI passthrough
3. Add GPU to the Ollama VM

## Configuration

### Pull Models

Download models using the Ollama CLI:

```bash
# SSH to Ollama VM
ssh tappaas@ollama.mgmt.internal

# Pull models
ollama pull llama3.1
ollama pull mistral
ollama pull codellama
```

### List Models

```bash
ollama list
```

### Remove Models

```bash
ollama rm <model-name>
```

## API Access

Ollama exposes an OpenAI-compatible API on port 11434:

```python
import openai

client = openai.OpenAI(
    base_url="http://ollama.mgmt.internal:11434/v1",
    api_key="ollama"  # Any string works
)

response = client.chat.completions.create(
    model="llama3.1",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Integration

### With OpenWebUI

Configure OpenWebUI to use Ollama:

1. Navigate to **Settings** → **Connections**
2. Add Ollama connection:
   - URL: `http://ollama.mgmt.internal:11434`

### With LiteLLM

Add Ollama models to LiteLLM configuration:

```yaml
model_list:
  - model_name: local-llama
    litellm_params:
      model: ollama/llama3.1
      api_base: http://ollama.mgmt.internal:11434

  - model_name: local-code
    litellm_params:
      model: ollama/codellama
      api_base: http://ollama.mgmt.internal:11434
```

## Model Management

### Custom Models

Create custom models with specific system prompts:

```bash
# Create Modelfile
cat > Modelfile << EOF
FROM llama3.1
SYSTEM You are a helpful coding assistant.
PARAMETER temperature 0.7
EOF

# Create custom model
ollama create coding-assistant -f Modelfile
```

### Model Updates

Keep models updated:

```bash
# Update a model
ollama pull llama3.1

# Check for updates
ollama list
```

## Performance Tuning

### Memory Settings

Configure memory limits in the service:

```bash
# Edit service configuration
sudo systemctl edit ollama
```

Add:

```ini
[Service]
Environment="OLLAMA_MAX_LOADED_MODELS=2"
```

### GPU Configuration

For NVIDIA GPUs:

```bash
# Verify GPU is detected
nvidia-smi

# Check Ollama GPU usage
ollama ps
```

## Monitoring

### Check Status

```bash
# Service status
systemctl status ollama

# Running models
ollama ps

# Resource usage
htop
nvidia-smi  # If GPU available
```

### Logs

```bash
journalctl -u ollama -f
```

## Troubleshooting

### Model Download Fails

- Check disk space: `df -h`
- Verify network connectivity
- Try smaller model first

### Slow Inference

- Check available RAM: `free -h`
- Verify no other models loaded: `ollama ps`
- Consider GPU acceleration
- Use quantized models (Q4_K_M)

### Out of Memory

- Stop other models: `ollama stop <model>`
- Use smaller models
- Increase VM RAM allocation

## Backup

Model files are stored in `/usr/share/ollama/.ollama/models`. Include in VM backup.

### Export Models

```bash
# Models are automatically backed up with VM
# For manual export:
tar -czf ollama-models.tar.gz /usr/share/ollama/.ollama/models
```

## Next Steps

- Connect to [OpenWebUI](openwebui.md) for chat interface
- Configure [LiteLLM](litellm.md) for unified access
