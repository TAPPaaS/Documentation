---
title: AI Stack
description: >
  Local AI on your own silicon: vLLM serving, the LiteLLM gateway, and the
  OpenWebUI chat interface.
---

# AI Stack

Three modules give you the full local-AI experience — models served on your own
hardware, one API for every consumer, and a polished chat UI:

| Module | Role | Status |
|--------|------|--------|
| **[vLLM (AMD)](../../generated/apps/vllm-amd.md)** | Model serving on AMD GPUs / unified-memory APUs | Available |
| **[LiteLLM](../../generated/apps/litellm.md)** | OpenAI-compatible gateway: one API + per-user keys in front of local (and optional remote) models | Available |
| **[OpenWebUI](../../generated/apps/openwebui.md)** | Chat interface for your users | Available |

**Install order follows the dependencies:** vLLM (AMD) → LiteLLM → OpenWebUI.

**Hardware:** local AI is sized by accelerator memory and the model you want — see the
[GPU / VRAM guidance](../../generated/hardware-selection.md#sizing-local-ai-gpu-vram-guidance).
The reference AI node is an AMD Ryzen AI MAX+ 395 ("Strix Halo") with 128 GB unified
memory; discrete GPUs work too.

**No local AI hardware?** LiteLLM can front remote models instead — convenient, less
sovereign. Any other OpenAI-compatible backend on your network (e.g. a vLLM or Ollama
you already run) can also be added as a provider.
