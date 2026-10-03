# Archived: hand-written Install → Add Stacks overviews

**Not published** — this directory is outside `docs/`, so MkDocs never builds it.

Until 2026-10-03 the three *Add Stacks* overview pages were hand-written here, at
`docs/install/<stack>-stack/index.md`. Since TAPPaaS #421 every stack has its own
`src/<stack>/README.md` upstream, and `scripts/sync-source.py` now builds the whole
*Add Stacks* section from those READMEs and the modules' `INSTALL.md` files. The old
pages are kept here, unchanged (`git mv`), so their content is not lost before someone
decides what to reuse. Delete this directory once every row below is decided.

## Reuse checklist

"Upstream" = the stack README in TAPPaaS, `src/<stack>/README.md` (outside its
GENERATED block), or a module's README/INSTALL. "What" = `docs/stacks/<stack>.md`.

| From | Material | Present elsewhere today? | Suggested home | Decision |
|------|----------|--------------------------|----------------|----------|
| ai-stack | Role + status per module (table) | Roles in What → `stacks/ai.md`; upstream table has the JSON descriptions, no status | none — covered | |
| ai-stack | "Install order: vLLM (AMD) → LiteLLM → OpenWebUI" | **Conflicts** with upstream's computed order litellm → vllm-amd → openwebui (no declared dependency between vllm-amd and litellm) | Upstream: declare the litellm→vllm dependency, or accept the computed order | |
| ai-stack | Hardware: link to GPU / VRAM sizing | Yes, in `stacks/ai.md` | Upstream `src/ai/README.md` | |
| ai-stack | Reference AI node: Ryzen AI MAX+ 395 "Strix Halo", 128 GB; discrete GPUs work too | Partly: hardware-selection, vllm-amd README | Upstream `src/ai/README.md` or `DESIGN.md` | |
| ai-stack | "No local AI hardware? LiteLLM can front remote models — less sovereign; any OpenAI-compatible backend (vLLM, Ollama) can be a provider" | Not as a stack-level statement (LiteLLM pages mention providers) | Upstream `src/ai/README.md` | |
| collaboration-stack | Nextcloud status "Available (Testing)" | No | Module status lives in the module JSON — check it says so | |
| collaboration-stack | n8n "Planned — placeholder module" | n8n is now in the **AI** stack (#421); What → `stacks/ai.md` has the row | none — covered | |
| collaboration-stack | **Karakeep** — bookmarking / read-it-later, planned, no module yet | Only in TAPPaaS `INSTALL.md` stage 6 table | Upstream stack README (a "Planned" line) or `stacks/collaboration.md` | |
| collaboration-stack | EURO Office and Coturn as "related modules" | Now members of the stack — obsolete | none | |
| collaboration-stack | "Vaultwarden moved to the Security Stack" | Obsolete — Security stack has its own section | none | |
| home-stack | Role + status per module, Jellyfin and Immich planned | Yes, in `stacks/home.md` | Upstream `src/home/README.md` ("Planned") | |
| home-stack | Home Assistant runs as a sealed appliance VM in the home service zone | Partly: hass INSTALL (zone `srvHome`) | Upstream `src/home/README.md` | |
| home-stack | IoT devices separated at the network layer: own zones, firewall boundaries, controlled pinholes, outside access gated at the reverse proxy | Yes, in `stacks/home.md` (minus the reverse-proxy sentence) | none, or the reverse-proxy sentence to `stacks/home.md` | |

## Related, not archived

- What → `stacks/collaboration.md` architecture diagram still draws n8n and Vaultwarden
  in the Collaboration ("Productivity") stack.
- TAPPaaS `INSTALL.md` stage 6 table links the retired production URLs
  (`tappaas.org/install/{ai,productivity,home,iot}-stack/`).
