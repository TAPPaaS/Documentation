---
title: AI Stack
description: Private AI — model serving, one gateway API, and a chat interface.
---

# AI Stack

| Module | Role |
|--------|------|
| [vLLM (AMD)](../../generated/modules/vllm-amd.md) | Model serving on AMD GPUs / unified-memory APUs |
| [LiteLLM](../../generated/modules/litellm.md) | OpenAI-compatible gateway with per-user keys |
| [OpenWebUI](../../generated/modules/openwebui.md) | Chat interface for your users |

Install guides live under [Install → Add Stacks](../../installation/ai-stack/index.md);
hardware sizing under [Hardware Selection](../../installation/hardware-selection.md#sizing-local-ai-gpu-vram-guidance).

## Architecture view

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title TAPPaaS AI Stack

' Business Actor
Business_Actor(user, "Platform User")

' Application Components (AI Services)
Application_Component(webui, "OpenWebUI")
Application_Component(litellm, "LiteLLM")
Application_Component(vllm, "vLLM")

' External Application Services
Application_Service(openai, "OpenAI API")
Application_Service(anthropic, "Anthropic API")

' Application Services exposed by components
Application_Service(chatSvc, "Chat Service")
Application_Service(routingSvc, "Model Routing")
Application_Service(inferenceSvc, "Local Inference")

' Components realize services
Rel_Realization(webui, chatSvc)
Rel_Realization(litellm, routingSvc)
Rel_Realization(vllm, inferenceSvc)

' User uses chat service
Rel_Serving(chatSvc, user)

' Service dependencies
Rel_Serving(routingSvc, webui)
Rel_Serving(inferenceSvc, litellm)
Rel_Serving(openai, litellm)
Rel_Serving(anthropic, litellm)

@enduml
```
