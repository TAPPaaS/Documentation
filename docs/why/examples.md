---
title: Examples — running today
description: >
  What people actually run on TAPPaaS: files and collaboration, home automation,
  local AI, workflow automation, passwords — every entry a real module in the
  TAPPaaS source tree.
---

# Running today. Not a roadmap.

TAPPaaS systems are live with their first adopters. Every example below is a **real
module** in the TAPPaaS source tree
([`src/apps`](https://codeberg.org/TAPPaaS/TAPPaaS/src/branch/main/src/apps)) — installed,
updated and backed up by the platform.

## Your files and collaboration

<div class="grid cards" markdown>

-   :material-cloud-outline: **Nextcloud**

    ---

    Files, calendars, contacts, photos and Talk — your own cloud drive, under your
    roof. A high-performance backend module (`nextcloud-hpb`) scales Talk and push
    notifications.

    [:octicons-arrow-right-24: Install guide](../generated/apps/nextcloud.md)

-   :material-file-document-edit-outline: **EURO Office**

    ---

    A full web office suite integrated into Nextcloud — edit documents,
    spreadsheets and presentations in the browser, without a US SaaS in the loop.

    [:octicons-arrow-right-24: Module page](../generated/modules/euro-office.md)

-   :material-shield-key-outline: **Vaultwarden**

    ---

    A Bitwarden-compatible password manager: one vault for the family or the
    company, stored on your hardware, reachable from every device.

    [:octicons-arrow-right-24: Module page](../generated/modules/vaultwarden.md)

-   :material-phone-in-talk-outline: **Coturn**

    ---

    The TURN relay that makes Nextcloud Talk calls work reliably across firewalls —
    your calls never route through someone else's relay.

    [:octicons-arrow-right-24: Module page](../generated/modules/coturn.md)

</div>

## Your AI — on your own silicon

<div class="grid cards" markdown>

-   :material-chat-processing-outline: **OpenWebUI**

    ---

    A polished chat interface for AI models — the familiar assistant experience,
    served from your own rack.

    [:octicons-arrow-right-24: Install guide](../generated/apps/openwebui.md)

-   :material-brain: **vLLM (AMD)**

    ---

    Local model serving on AMD GPUs and unified-memory APUs — from 7B up to
    100B+-class models on a single inexpensive box.

    [:octicons-arrow-right-24: Module page](../generated/modules/vllm-amd.md)

-   :material-swap-horizontal: **LiteLLM**

    ---

    One OpenAI-compatible gateway in front of your local models (and, if you choose,
    remote ones) — apps talk to one API, you decide where inference runs.

    [:octicons-arrow-right-24: Install guide](../generated/apps/litellm.md)

</div>

## Your home and your workflows

<div class="grid cards" markdown>

-   :material-home-automation: **Home Assistant**

    ---

    Home automation with local control: lights, heating, sensors and cameras that
    keep working when the internet doesn't.

    [:octicons-arrow-right-24: Install guide](../generated/apps/hass.md)

-   :material-zigbee: **deCONZ**

    ---

    A Zigbee gateway for sensors, switches and lights — pairs naturally with Home
    Assistant, no vendor cloud required.

    [:octicons-arrow-right-24: Module page](../generated/modules/deconz.md)

-   :material-robot-industrial: **n8n**

    ---

    Workflow automation connecting your services — the "glue" tier of your platform,
    self-hosted instead of subscription-hosted.

    [:octicons-arrow-right-24: Module page](../generated/modules/n8n.md)

</div>

## Connectivity and the stragglers

<div class="grid cards" markdown>

-   :material-lan-connect: **NetBird client**

    ---

    WireGuard-based mesh connectivity — reach your platform securely from anywhere
    without opening your network to the world.

    [:octicons-arrow-right-24: Module page](../generated/modules/netbird-client.md)

-   :material-microsoft-windows: **Windows Server**

    ---

    Some workloads just need Windows. Run it as a managed TAPPaaS module — inside
    your environments, backed up like everything else.

    [:octicons-arrow-right-24: Module page](../generated/modules/windows-server.md)

</div>

---

## More than one tenant

A single TAPPaaS site can host **separated environments** — production next to family,
tenants next to experiments — with network boundaries between them. See the worked
multi-tenant setup in [Add an Environment](../generated/install-environment.md).

## Build your own

Every module follows the same structure (the
[`00-Template`](https://codeberg.org/TAPPaaS/TAPPaaS/src/branch/main/src/apps/00-Template) app is
the starting point) — see the [module structure](../generated/module-template.md)
documentation to package the app *you* need.

[Install TAPPaaS](../generated/install-overview.md){ .md-button .md-button--primary }
