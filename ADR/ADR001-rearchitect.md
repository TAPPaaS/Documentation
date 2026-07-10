# ADR-001 — Re-architect the TAPPaaS Website

**Status:** Draft for review — planning mode
**Owner:** Lars Rossen
**Date:** 2026-07-09
**Supersedes:** `ARCHITECTURE_PLAN.md` (sunset — removed; see [Relationship to the old plan](#relationship-to-the-old-architecture_plan))

---

## 1. Purpose

The TAPPaaS documentation site (published to **tappaas.org**, source in this repo) needs a
significant upgrade across five fronts: a more *alive* front-end, sharper and consolidated
messaging, a rebuilt installation experience, a reorganised manual/architecture split, and a
maintainable roadmap. This document is the working plan — it captures the current state, the
decisions to be made, the recommended direction, and a phased set of workstreams.

This is a **planning document**, not a spec. Each workstream lists options with a recommendation so
we can decide together before building.

---

## 2. Current state (assessment)

**Stack:** MkDocs + Material theme, Kroki (ArchiMate/PlantUML), deployed via GitHub Actions on push
to `main`. Config in [`mkdocs.yml`](../mkdocs.yml), content in [`docs/`](../docs/).

**Information architecture (today):** `Home · Intro · Installation · Manual · Architecture · Roadmap · About · Appendix`
(a Terraform-inspired layout).

**What works:**

- Solid, conventional docs tooling; ArchiMate rendering pipeline already wired.
- Installation section is well-decomposed (Foundation / AI / Productivity / Home stacks).
- Architecture section has real depth (solution design, CICD design, module designs, meta-model).

**What's weak:**

- **Front page & Intro are generic PaaS boilerplate.** Copy like "scale your application", "CLI",
  "cloud-native", "multi-tenant capabilities", "ship faster" is inherited from a generic
  Heroku-style template and *misrepresents* TAPPaaS. TAPPaaS is a **self-hosted, Proxmox-based
  platform for digital sovereignty** — the messaging should say so. The real story (Digital
  Sovereignty, Trusted/Automated/Private) is buried in `intro/` sub-pages.
- **Front page is static.** It's a hero + three cards + prose. Modern comparable products (see
  §5.1) lead with motion, product visuals, and a crisp "who/what/why" above the fold.
- **Installation drifts from source.** The authoritative install procedure lives in the TAPPaaS
  repo ([`INSTALL.md`](../../TAPPaaS/INSTALL.md), `INSTALL-ENVIRONMENT.md`) and in ~60 `README.md` /
  `INSTALL.md` files under `src/`. The docs site paraphrases these by hand, so it will always lag.
- **Manual / Architecture / Appendix are organised by artifact type, not by audience.** An operator
  and a contributor need very different things; today they're interleaved.
- **Roadmap is partly stale** (hardcoded "on track for 1.0 by end of Q1 2026"; today is
  2026-07-09) even though it already links to GitHub milestones.
- **Versioning is unaddressed.** The site tracks whatever is on `main` of the docs repo, with no
  notion of TAPPaaS `stable` vs `main`, and no home for the ADR-007 / 2.0 transition.

**Asset gap:** the site ships only a logo and an icon — no screenshots, diagrams-as-images, or
presentation graphics. The presentation material the user referenced is **not in either repo** and
is a hard dependency for the messaging workstream (see [Open Decisions](#11-open-decisions--inputs-needed)).

---

## 3. Guiding principles

1. **Truth over polish.** Every claim on the site must reflect what TAPPaaS actually is and does
   today. Kill the generic-PaaS vocabulary.
2. **Single source of truth.** Installation and operational reference should be *generated/synced*
   from the TAPPaaS source repo, not hand-copied. The docs site curates and frames; the code repo
   owns the procedure.
3. **Audience-first IA.** Organise around *who is reading* (prospective adopter → operator →
   developer) rather than around document types.
4. **Version-aware.** The public site reflects `stable`; contributors can find `main`/next.
5. **Low maintenance burden.** Prefer automation (CI sync, milestone links) over content that must
   be manually kept current.
6. **Sovereign toolchain.** A site about digital sovereignty must be built and hosted sovereignly.
   **Decided:** the `Documentation` repo moves to **Codeberg (Forgejo) now** — dev/staging/preview on
   Codeberg Pages via **Woodpecker (Codeberg CI)** — while **GitHub keeps publishing the live 1.x
   site** until the 2.0 cutover. The **TAPPaaS source code stays on GitHub for now** (synced
   cross-forge). Every tool we adopt must be **open-source and self-hostable** — no proprietary SaaS —
   and the site should eventually run **on a TAPPaaS system itself**. Keep build and publish decoupled
   so migration only swaps the publish target.

---

## 4. Workstreams overview

| # | Workstream | Core outcome | Depends on |
|---|------------|--------------|------------|
| WS-S | Staging / pre-release env | Preview & review changes before publishing | — |
| WS1 | Front-end / UI framework | Decide & prototype a more "live" front-end | — |
| WS2 | Messaging & front page | One focused who/what/why story + Examples | Presentation assets, WS1 |
| WS3 | Installation overhaul | Source-synced install, macro steps, hardware personas | WS6 (versioning), source-sync mechanism |
| WS4 | Manual → Operate vs Develop | Audience-split reference, README sync | Source-sync mechanism |
| WS5 | Roadmap | Self-maintaining, milestone-driven | — |
| WS6 | Versioning (stable vs main) | Public site = `stable`; ADR-007 → 2.0 story | — |
| WS0 | Source-sync mechanism | Reusable pipeline feeding WS3 & WS4 | — |

WS-S (staging) is stood up **first** so every other workstream can be reviewed on a real URL before
publishing. WS0 (source-sync) is the next enabler because WS3 and WS4 both consume it.

---

## 5. WS1 — Front-end / UI framework

**Goal:** decide whether MkDocs Material is the right vehicle, and prototype a noticeably more
"alive" front page. The user explicitly wants to *investigate and experiment with a few* options.

### 5.1 Reference products to study (for the "live" feel)

Pull concrete patterns (hero motion, product visuals, "who/what/why" above the fold, example
gallery) from a handful of modern docs+marketing sites, e.g. Tailscale, Coolify, Proxmox, HashiCorp,
Astro, Supabase, Umbrel/Start9 (closest in spirit — self-hosting for sovereignty). Capture what
makes each feel current: animation, real screenshots/video, opinionated typography, and a tight
value proposition.

### 5.2 The key architectural choice: coupled vs decoupled

A recurring pattern in the reference set is a **decoupled marketing landing** (rich, animated, built
with a web framework) that links into a **docs tool** (fast, searchable, content-heavy). We should
decide between:

- **Option A — Stay on MkDocs Material, enhance it.** Push the theme with custom CSS/JS, a bespoke
  landing template, and light animation. Lowest cost, keeps one toolchain and the Kroki pipeline.
  Ceiling on how "live" it can feel.
- **Option B — Decoupled: marketing landing (Astro/Next/SvelteKit) + keep MkDocs for docs.**
  Best "live" front page; docs stay stable. Cost: two toolchains, two deploys, shared design system.
- **Option C — Migrate everything to a modern docs framework** (Astro Starlight, Docusaurus,
  Nextra, VitePress). Unifies marketing + docs with modern DX and components. Cost: migrate ~90
  Markdown pages and re-solve ArchiMate/Kroki rendering; risk to existing content.

**Recommendation:** run a **time-boxed spike** comparing **A** and **B** on the *actual* front page
before committing. Default lean is **Option B** (decoupled landing + MkDocs docs) — it gets the
biggest visual win for the least risk to the large existing docs corpus, and matches how the
reference products are built. Reserve Option C only if the spike shows the docs experience itself is
a bottleneck.

> **Decision (agreed):** we *will* run the A-vs-B spike. **Not yet** — we finish planning first; the
> spike is the first build action in Phase 0 once this plan is signed off. Whether the decoupled
> Option B is acceptable operationally (two toolchains) is a judgement to make *from the spike
> results*, not before. The spike must be built on the **sovereign/portable pipeline** (WS-S): both
> prototypes have to be buildable under Woodpecker (Codeberg CI) and hostable on Codeberg Pages /
> self-hosted Caddy, so we don't prototype something we can't sovereignly ship.

### 5.3 Evaluation criteria

Score each prototype on: visual "aliveness", authoring effort for non-developers, build/deploy
complexity, ArchiMate/Kroki + Mermaid support, search quality, i18n headroom, and long-term
maintenance load.

### 5.4 Tasks

- [ ] Assemble a 1-page inspiration board from the reference products (screens + what to steal).
- [ ] Spike A: a redesigned MkDocs landing (custom template + CSS/JS + motion) on a branch.
- [ ] Spike B: a small Astro/Next landing that links into the existing docs.
- [ ] Side-by-side review; decide A / B / C and record the decision in this file.
- [ ] Define the shared design tokens (color, type, spacing) so marketing + docs stay consistent.

---

## 6. WS2 — Messaging & front page

**Goal:** replace the generic-PaaS story with one focused, honest narrative and combine the current
front page + Intro into a tight funnel. Incorporate the presentation material (graphics + storylines).

### 6.1 The canonical storyline (from the promo script)

We now have a strong, finished narrative — the **5-minute promo video script**
(`.../Marketing/tappaas-promo-video-script.md`, see §6.2). It is on-message, honest, and should be
the **backbone of the front page and Intro**, replacing the generic-PaaS copy wholesale. Its beats:

1. **Hook — "Who is in control of your digital life?"** The triad **data · cost · access**. This is
   the front-page headline energy; far sharper than today's "deploy and scale your applications".
2. **The cloud continuum & the "glass wall"** — sovereignty is *architecture, not a contract*; the
   right side is also about **resilience** (runs even when disconnected). (Slide 1)
3. **The hurdle — what a cloud really is: four building blocks** — **Site · Workloads · People ·
   Environments**. Hyperscalers won by *packaging* complexity; TAPPaaS packages the same convenience
   *on your side of the wall*, pre-integrated and open source. (Slide 2)
4. **The vision — Trusted · Automated · Private** (self-hosted), resilient by design, **running
   today** with first adopters. (Slide 3)
5. **Close / CTA** — "who is in control? — **we are**." → tappaas.org. Sign-off: *Your data. Your
   costs. Your access. Your platform.*

**Map to the page ladder:** Hook + triad → hero; continuum/glass-wall + four-blocks → "Why TAPPaaS";
T-A-P vision → "What it is"; "running today" → **Examples** (§6.3); CTA → Install (versioned, WS6).
Explicit audiences (small business, government/NGO, community of homes, capable households) tie to the
hardware personas in WS3. The already-on-message `intro/problem.md` and `intro/digital-sovereignty.md`
fold into this; the generic `intro/*` copy is retired.

> **Strong internal alignment — use it.** The promo's **four building blocks (Site · Workloads ·
> People · Environments)** are essentially the **ADR-007 taxonomy** (Site · Apps · People ·
> Environments · Health). The *marketing story and the architecture spine are the same model.* Present
> them consistently: the front page introduces the four blocks; the Develop track (WS4 §8.3) is the
> same model in technical depth. One mental model, two altitudes.

### 6.2 Presentation & video assets (located)

Source material lives in Nextcloud (outside the repo), at
`/Users/larsrossen/Nextcloud/Rossen/RossenConsulting/TAPPaaS/Marketing`:

| Asset | Use |
|-------|-----|
| `tappaas-promo-video-script.md` / `.pdf` / teleprompter | The storyline SSOT for front page + Intro copy |
| `video-assets/slide-1..3.png` | Ready front-page graphics: continuum/glass-wall, four blocks, vision |
| `tappaas-promo-video-slides.pptx` | Editable source of the three slides |
| `5 minute TAPPAaS overview.pptx` | Deeper overview — mine for Intro/Why diagrams |
| `TOG - Oslo - Sovereignty and Resiliency v2.pptx` | Talk deck — mine for sovereignty framing/graphics |
| (promo video, when produced) | Embed on the front page / Why page |

Because these live in Nextcloud, **copy exports into the repo** under `docs/assets/` (don't reference
Nextcloud paths). Prefer re-drawing the continuum/four-blocks diagrams as Kroki/Mermaid so they stay
editable and theme-aware (light/dark); import polished illustrations as SVG/PNG where redraw isn't
worth it. Optimize all raster assets.

> **Claims hygiene:** the script's production notes flag a named early adopter (e.g. Qualiware) with
> "check what's public before using it." Any named adopter, logo, or "first companies" claim on the
> public site needs sign-off before publishing.

### 6.3 New "Examples" section

Add a curated gallery of what people actually run on TAPPaaS, sourced from the real modules in
[`../TAPPaaS/src/apps`](../../TAPPaaS/src/apps) (Nextcloud, Home Assistant, OpenWebUI, n8n, LiteLLM,
Coturn, deCONZ, EURO Office, …) and the worked multi-tenant example in `INSTALL-ENVIRONMENT.md`.
Each example: a screenshot/visual, the problem it solves, and a link to its install page. This
doubles as social proof and as an entry point to installation.

### 6.4 Tasks

- [ ] Rewrite `docs/index.md` around the promo storyline (§6.1); delete generic-PaaS copy.
- [ ] Copy/export the marketing assets (§6.2) into `docs/assets/`; establish an assets convention.
- [ ] Redraw continuum + four-blocks diagrams as Kroki/Mermaid (theme-aware) where worthwhile.
- [ ] Consolidate `intro/*` into a lean set (kill duplication with the front page).
- [ ] Present the four building blocks consistently with the ADR-007 taxonomy (align with WS4 §8.3).
- [ ] Build the Examples gallery from real `src/apps` modules (the "running today" proof).
- [ ] Copy-review pass: no "CLI/scale/multi-tenant/ship faster" unless literally true.
- [ ] Get sign-off before publishing any named-adopter/logo claim.

---

## 7. WS3 — Installation overhaul

**Goal:** make installation clearly staged, current with source, and personalised by user category.

### 7.1 Sync with the source `INSTALL.md`

The authoritative procedure is [`../TAPPaaS/INSTALL.md`](../../TAPPaaS/INSTALL.md) (Prerequisites →
Bootstrap: nodes/firewall/CICD → Foundation → Stacks → Network cutover → Appendices) plus
`INSTALL-ENVIRONMENT.md`. The docs site must stay current with these. Two viable models:

- **Reference-out:** the site frames the macro steps and deep-links into the source `INSTALL.md` at
  a pinned tag. Zero drift, minimal effort, but readers leave the site for the details.
- **Sync-runner (recommended):** a CI step (WS0) pulls `INSTALL.md` / `INSTALL-ENVIRONMENT.md` from
  a pinned TAPPaaS ref, transforms them into site pages (fix relative links, inject front matter,
  add nav), and fails the build if the source moved unexpectedly. Keeps everything on-site and
  always current.

Recommendation: **sync-runner**, pinned to `stable` for the public site (see WS6), with a clear
"generated from source — edit upstream" banner on synced pages.

### 7.2 Clarify the macro steps

Present installation as a small number of unmistakable macro-stages with a progress model, e.g.:

1. **Choose hardware** (size tier × capability options → sizing, §7.3)
2. **Prepare** (network/DNS/domain/credentials)
3. **Bootstrap the foundation** (first node + firewall + CICD mothership)
4. **Grow the cluster** (optional additional nodes)
5. **Add stacks** (AI / Productivity / Home / community modules)
6. **Cut over the network** to the firewall
7. **Operate** (hand-off to the Operate section, WS4)

Each stage: prerequisites, what success looks like, and the exact commands (synced from source).

### 7.3 Hardware selection — a two-axis model

Today's [hardware-selection.md](../docs/installation/hardware-selection.md) offers just two configs
(Minimum / Redundant). Replace it with a **two-axis model**: pick a **size tier** (what you're
running it for), then toggle a few **capability options** independently. This is far clearer than a
flat persona list because the options are genuinely orthogonal — an SMB may skip local AI; a home
may have no public IP; an evaluator may want neither backup nor ingress.

#### Axis A — Size tier (the "how big" axis)

Driven by users/workload and how much redundancy you need. Baselines reuse the numbers already in
`hardware-selection.md` (storage roles `tanka1` = VMs+data, `tankb1` = bulk/non-critical,
`tankc1` = backup).

| Tier | For whom | Topology | Per-node baseline | Redundancy |
|------|----------|----------|-------------------|------------|
| **Evaluation** | Trying/testing TAPPaaS, dev, labs | 1 node (min spec; nested-virt OK) | 4 cores / 16 GB / 256 GB boot + 500 GB `tanka1` | none — disposable |
| **Home** | Technically-capable household | 1 strong node | 8+ cores / 32 GB / 512 GB SSD + 2×2 TB mirror `tanka1` | disk mirror; single box |
| **SMB** | Business / NGO, uptime matters | 3-node HA cluster | ~8 cores / 32 GB ECC each | HA + ZFS mirror; 3-2-1 |
| **Scale-out** | Many users/tenants, growth | 3 → N nodes, dedicated roles | add compute / GPU / storage nodes | HA + role separation |

Evaluation ≈ today's *Minimum*; SMB ≈ today's *Redundant 3-node*. Scale-out extends SMB by adding
role-dedicated nodes and using ADR-007 **Environments** for multi-tenant separation (the
`INSTALL-ENVIRONMENT.md` pattern).

#### Axis B — Capability options (the "with or without" axis)

Each option is an **independent yes/no**, layered on any size tier. The recurring theme: **the
satellite (ADR-010) is the escape hatch when a capability can't or shouldn't live locally.**

| Option | "With" (local) | "Without" → alternative |
|--------|----------------|--------------------------|
| **Local AI** | Add a **GPU** (+ VRAM/RAM); runs vLLM locally, full sovereignty | Omit GPU; either no AI, or LiteLLM/OpenWebUI fronting a remote model (less sovereign) |
| **Local Backup** | Add a **backup node/disk** (`tankc1` + PBS on-site) | **Satellite `backup` role** — off-site PBS *pull*, S3 Object-Lock (or a buddy PBS) |
| **Local public IP** | Direct WAN ingress: **Caddy on OPNsense** on a routable IP | **Satellite `reverse-proxy` role** — public ingress from a VPS when behind CGNAT / dynamic / no-inbound |

#### The satellite as the gap-filler (ADR-010)

A **satellite** is a small operator-owned node with a stable public IP (typically a low-cost EU VPS,
Hetzner is the reference). It is **optional and non-invasive** — a site with a public IP and local
backup needs none — and carries any combination of three independent roles:

- **`reverse-proxy`** → *the answer to "no local public IP."* Blind L4 TLS-passthrough to Caddy at
  home over WireGuard (home dials out, so CGNAT is fine). TLS keys stay home.
- **`backup`** → *the answer to "no local backup."* Off-site PBS the home PBS is pulled into;
  client-side encrypted, immutable (S3 Object-Lock).
- **`admin-vpn`** → public admin reach into the management plane with no public IP (pairs naturally
  with `reverse-proxy`).

So the two "without" cases the user flagged both resolve to the satellite: **no public IP → satellite
`reverse-proxy` (+`admin-vpn`); no local backup → satellite `backup`.** One satellite can do both.

#### Putting it together — the sizing decision flow

The install "Choose hardware" step becomes a short decision:

1. **Pick a size tier** — Evaluation / Home / SMB / Scale-out (Axis A table).
2. **Local AI?** If yes, add a GPU or unified-memory APU to the node hosting the AI stack (a dedicated
   AI node at SMB/Scale-out); size it via the GPU/VRAM guidance below.
3. **Local backup?** If yes, size `tankc1` / a backup node. If no, plan a **satellite `backup`**.
4. **Local public IP?** If yes, standard WAN ingress. If no (CGNAT/dynamic/no-inbound), plan a
   **satellite `reverse-proxy` (+`admin-vpn`)**.

Worked example: *Home tier, with local AI, without local backup, without public IP* → one 32 GB node
+ GPU/APU + mirrored `tanka1`, and **one satellite carrying `backup` + `reverse-proxy` + `admin-vpn`**.

#### GPU / VRAM guidance for local AI

The "with local AI" option is sized by the **memory available to the accelerator** and the **model
size × quantization** you want to run — not by GPU brand. Two hardware paths, both supported by the
AI stack (vLLM serving → LiteLLM gateway → OpenWebUI):

- **Unified-memory APU (the TAPPaaS reference).** An **AMD Ryzen AI MAX+ 395 "Strix Halo"** with
  **128 GB LPDDR5x unified memory** is the reference AI node (`tappaas2` in the sample cluster). The
  iGPU shares system memory, so "VRAM" = a large slice of unified RAM — which is what lets a single
  inexpensive box reach very large models. *Note gfx1151 has no FP8; use AWQ/GPTQ quantization, and
  its ROCm builds are nightly/unofficial (upstream caveats apply).*
- **Discrete GPU.** A dedicated card with its own VRAM (NVIDIA/AMD) — size the card by the table below.

| AI ambition | Example models (as tested) | Accelerator memory | Fits which path |
|-------------|----------------------------|--------------------|-----------------|
| **Entry** | 7–8B FP16 (Qwen2.5-7B ≈ 50 tok/s); ~14B AWQ | **12–16 GB** | Entry discrete GPU, or any APU |
| **Solid / general** | up to ~30B 4-bit (Qwen3-Coder-30B GPTQ ≈ 20 tok/s) | **24–32 GB** | 24 GB-class GPU, or a 32 GB+ APU |
| **Large** | 70B–120B AWQ (gpt-oss-120B tested) | **64–128 GB unified** | Strix-Halo-class 128 GB APU |

Rules of thumb: **4-bit quantization (AWQ/GPTQ) roughly quarters** the memory vs FP16, and is the
practical choice above ~14B; leave headroom for the KV-cache/context on top of the weights. Where a
big model matters more than raw speed, the **unified-memory APU** gives the most capability per euro;
where latency matters most, a **discrete GPU** with fast dedicated VRAM wins at a given model size.
By tier: local AI is natural on a **Home** single strong node (APU or one GPU), and on **SMB /
Scale-out** as a **dedicated AI node** (matching the sample cluster's Node 2 = AI node). Choosing
**without** local AI, LiteLLM can still front a **remote** model — convenient, but less sovereign.

**Structure confirmed.** Four tiers × three options, as above. **No budget bands** on the page —
spec-only guidance (decided). GPU/VRAM guidance drafted above (sync exact model/throughput numbers
from the `vllm-amd` module via WS0 so they stay current).

### 7.4 Tasks

- [ ] Build the WS0 sync-runner for `INSTALL.md` + `INSTALL-ENVIRONMENT.md`.
- [ ] Restructure `installation/index.md` around the 7 macro stages with a progress model.
- [ ] Rewrite `hardware-selection.md` around the two-axis model (size tier × capability options).
- [ ] Add a "Choose hardware" **decision flow** (the 4 steps above) with per-tier sizing tables.
- [ ] Add the **GPU/VRAM guidance** table for local AI; sync model/throughput numbers from `vllm-amd`.
- [ ] Document the **satellite (ADR-010)** as the no-public-IP / no-local-backup path; sync from the
      satellite `README.md` / `INSTALL.md` via WS0.
- [ ] Add the multi-tenant/Environments path (`INSTALL-ENVIRONMENT.md`) for Scale-out.
- [ ] Add stable-vs-main install guidance (WS6) at the top of the install flow.

---

## 8. WS4 — Manual / Architecture / Appendix → Operate vs Develop

**Goal:** regroup the reference material by audience into two top-level tracks: **Operate TAPPaaS**
(run it day-to-day) and **Develop TAPPaaS** (extend/contribute), and systematically sync the source
`README.md` files.

### 8.1 The split

- **Operate TAPPaaS** — for people running a live system: the scripts manual, update scheduler,
  OPNsense controller, backup, health, environments/tenants, troubleshooting. Draws from
  `docs/manual/*` and operational `README`s under `src/foundation/.../{manager,controller}`.
- **Develop TAPPaaS** — for contributors/module authors: CICD design, module structure, the
  ADR-007 taxonomy (People/Apps/Environments/Health), meta-model, ADRs, and the module-authoring
  workflow (the `00-Template` app, `install-module.sh`, schemas). Draws from
  `docs/architecture/*`, `docs/appendix/*`, the source `docs/ADR/*`, and `src/**/README.md`.

The current **Architecture** and **Appendix** sections mostly become the backbone of **Develop**;
the **Manual** becomes the backbone of **Operate**.

### 8.2 Systematic README sync

There are ~60 `README.md` / `INSTALL.md` files under [`../TAPPaaS/src`](../../TAPPaaS/src) (controllers,
managers, apps, schemas). These are the real reference for how modules work. Use the **same WS0
sync-runner** to pull a curated subset into the site (e.g. each manager/controller README → an
Operate reference page; each app README → an Examples/install page), with generated-from-source
banners and pinned refs. Define an allow-list rather than syncing everything, to avoid importing
internal/WIP notes.

### 8.3 ADR-007 as the architecture spine

ADR-007 (TAPPaaS Taxonomy: **People · Apps · Environments · Health**) is the current, accepted model
and the basis for 2.0. The Develop track's architecture overview should be rebuilt around it,
superseding older framing. Pull from `../TAPPaaS/docs/ADR/ADR-007*` and the ontology SSOT it
references. Coordinate with WS6 — publish the ADR-007 model as the architecture once it's on `stable`.

### 8.4 Tasks

- [ ] Design the Operate vs Develop nav (see §10) and migrate existing pages into it.
- [ ] Extend WS0 to sync an allow-listed set of `src/**/README.md` into Operate/Develop pages.
- [ ] Rebuild the architecture overview around the ADR-007 taxonomy.
- [ ] Fold the ArchiMate appendix into Develop (it's contributor-facing reference).
- [ ] Add a contributor "author a module" guide from the `00-Template` + schemas.

---

## 9. WS5 — Roadmap

**Goal:** a roadmap that stays current with near-zero maintenance.

The page already links to [GitHub milestones](https://github.com/TAPPaaS/TAPPaaS/milestones); the
problem is the *hand-maintained* timeline and status note that go stale. Options:

- **Replace** the static timeline with a short "how we plan" explainer + a live pointer to
  milestones/issues (optionally auto-embedded via CI). Lowest maintenance.
- **Rewamp**: keep a light phase narrative (Framework → MVP → 2.0/ADR-007 → Growth) but remove all
  dated status claims, and let milestones carry specifics.

**Recommendation:** rewamp to a thin, dateless phase narrative anchored to the 2.0/ADR-007 milestone,
plus a CI-refreshed milestone list. Remove the "on track for Q1 2026" style claims entirely.

### 9.1 Tasks

- [ ] Strip dated status assertions from `roadmap/index.md`.
- [ ] Add a short "how we plan / where to look" section pointing at milestones + this upgrade plan.
- [ ] (Optional) CI job to render current open milestones into the page at build time.

---

## 10. WS6 — Versioning: stable vs main, and ADR-007 → 2.0

**Goal:** the public site reflects TAPPaaS **`stable`**; contributors can reach `main`/next; and the
ADR-007 work (currently on the `ADR007` branch, pending merge to `stable`) has a clear 2.0 home.

**Context:** ADR-007 is *accepted and implemented* on the `ADR007` branch and expected to become
**release 2.0** and land on `stable` soon. The site must not present the new taxonomy as live until
it is on `stable`, but should be ready to flip.

**Decided (open decision #5): clean flip, no long-term versioning.** We do **not** need to preserve
1.x docs after 2.0 goes live — so **no `mike`/multi-version tooling**. But 1.x must **stay live until
2.0 is ready to go live**; the switch is a **one-time content cutover**, not a period of hosting both.
This is handled entirely by the WS-S environments model:

- **Production stays on 1.x** (WS0 pinned to `stable`) right up to the cutover — no gap in the live site.
- **2.0 is built and reviewed on staging** (`staging`/`next`, WS0 pinned to `main`/next) until it's
  signed off.
- **Cutover = repoint production** to the 2.0 content (once ADR-007 is on `stable` and 2.0 released).
  1.x is simply replaced; nothing to archive.

**Approach:**

- **Pin synced content (WS0) to `stable`** for the public tappaas.org build; 2.0 previews on staging.
- Add a prominent **"stable vs main"** explainer in the install flow: which branch to install from,
  what "2.0 / ADR-007" changes, and how to choose. Written to flip cleanly at cutover.

### 10.1 Cutover runbook — serving `tappaas.org` v2 from Codeberg

The cutover is a **staged, reversible DNS flip**, made safe by the parallel setup (1.x on GitHub,
v2 on Codeberg staging). The one wrinkle: `tappaas.org` is an **apex domain**, and DNS forbids a
CNAME at the apex — so the apex uses one of, **depending on the DNS provider**:

- **CNAME-flattening / ALIAS → `tappaas.codeberg.page`** (preferred — auto-tracks Codeberg's IP).
  **Cloudflare** (current provider) does this: put a "CNAME" at the apex and it flattens to A records.
  Route 53 ALIAS likewise. **deSEC does *not*** offer flattening/ALIAS.
- **A/AAAA → Codeberg Pages server IPs** (from docs.codeberg.org/codeberg-pages/; works anywhere but
  must be updated by hand if Codeberg changes IPs). This is the path on **deSEC** (planned future
  provider).

> **Cloudflare proxy must be OFF (grey cloud / DNS-only)** for both `staging` and the apex — an
> orange-cloud proxy makes Cloudflare terminate TLS and hides the real `Host`, so Codeberg can't
> issue its cert or route. Grey cloud also keeps Cloudflare out of the data path.
>
> **deSEC synergy:** TAPPaaS already uses **deSEC for DNS-01 ACME**, so `deSEC + self-hosted Caddy on
> TAPPaaS` is the natural sovereign end state (apex A/AAAA → the site's public IP or the ADR-010
> satellite; Caddy issues certs via deSEC) — no Cloudflare or Codeberg in the path. Treat the
> Cloudflare→deSEC move as its own step; don't combine it with the site cutover.

Steps:

1. **Lower the TTL** on the `tappaas.org` record ~24h ahead (fast propagation + fast rollback).
2. **Promote v2** to the production Pages content on Codeberg; add `tappaas.org` (+ optional `www`)
   as the **primary** entry in `.domains`.
3. **Flip the apex DNS** GitHub Pages → Codeberg (ALIAS/flatten or A/AAAA). Codeberg auto-issues the
   Let's Encrypt cert for `tappaas.org`.
4. **Verify**, then **retire GitHub Pages** (drop its workflow/CNAME). Keep the GitHub repo intact a
   while so **rollback = repoint the apex back** to GitHub.

`staging.tappaas.org` stays as the permanent staging environment. **Trust note:** on Codeberg Pages,
Codeberg terminates TLS for `tappaas.org` — acceptable for a public static site; the later hop to
**self-hosted Caddy on TAPPaaS** (A/AAAA to the site's public IP, or via the ADR-010 satellite
`reverse-proxy`) removes Codeberg from the TLS path and is the *same* repoint operation.

### 10.2 Tasks

- [ ] Public build pins to `stable`; 2.0 content lives on staging until go-live.
- [ ] Write the "stable vs main / what is 2.0 (ADR-007)" page.
- [ ] Confirm the DNS provider's apex capability (ALIAS/flatten vs A/AAAA) for `tappaas.org`.
- [ ] Execute the §10.1 cutover runbook (repoint prod to 2.0; retire 1.x — no archive).
- [ ] Sequence the ADR-007 content publish to coincide with the `stable` merge (ties to WS4 §8.3).

---

## 11. Proposed information architecture (target)

A candidate top-level nav after the upgrade (audience-first):

```
Home            → live landing (WS1/WS2)
Why TAPPaaS     → who/what/why + Digital Sovereignty + Examples (WS2)
Install         → macro stages + hardware personas + stable/main (WS3, WS6)
Operate         → run a live system: scripts, updates, firewall, backup, health, tenants (WS4)
Develop         → architecture (ADR-007 spine), CICD, module authoring, ADRs, ArchiMate (WS4)
Roadmap         → thin narrative + live milestones (WS5)
About           → people, logo, inspiration, license
```

This replaces the current `Intro / Manual / Architecture / Appendix` split with the clearer
`Why / Install / Operate / Develop` audience tracks.

---

## 11a. WS-S — Staging / pre-release environment (the first enabler)

**Goal:** be able to develop and *review changes on a real URL* before they go live on tappaas.org.
This is the first thing to stand up — every other workstream benefits from a safe place to preview.

**Current state:** push to `main` → GitHub Pages at **tappaas.org** (via
[`.github/workflows/deploy.yml`](../.github/workflows/deploy.yml), `docs/CNAME`). Pull requests build
with `mkdocs build --strict` but **do not deploy** — the only preview is local `mkdocs serve`. There
is no shared staging URL for reviewers.

### 11a.1 Sovereignty constraint (decisive)

The source code will move **off GitHub to Codeberg (Forgejo)**, and eventually the site should be
**hostable on a TAPPaaS system itself** — so all CI/runners and hosting must work in an
**open-source, self-hostable** setup (Codeberg runs Forgejo; its CI is **Woodpecker**, which we can
also self-host on TAPPaaS). A site *about* digital sovereignty should be built and served sovereignly.

This **rules out Cloudflare Pages and Netlify** as the destination: they are convenient (Cloudflare
Pages even has a free tier) but are **US-proprietary SaaS that cannot be self-hosted** and would have
to be torn out at the Codeberg/TAPPaaS step. We avoid that lock-in from the start.

**European / open options considered:** **Codeberg Pages** (free, German non-profit, runs on
Forgejo, custom domains + auto Let's Encrypt) · **Bunny.net** (Slovenia, cheap CDN/storage, paid) ·
Hetzner / Scaleway / OVH / Infomaniak (EU VPS/object storage) · **self-hosted Caddy on a TAPPaaS
module** (TAPPaaS already ships Caddy + ACME — the ultimate end state).

### 11a.2 Options (portable path)

The site output is just static files (`mkdocs build` → `site/`). Keep **build and publish decoupled**
so each migration hop swaps only the *publish target*, never the content or the build:

- **Option A — Portable static pipeline (recommended).** Structure the pipeline as *build → static
  `site/` → pluggable publish*. Realise it in three hops:
  1. **Now (GitHub):** keep prod on GitHub Pages; add staging/preview via the portable publish step —
     no proprietary preview SaaS.
  2. **Bridge (Codeberg):** CI = **Woodpecker CI** ("Codeberg CI" — checkout, pip, **Kroki service
     container**, `mkdocs build --strict`); hosting = **Codeberg Pages** for prod +
     a branch for `staging.tappaas.org`. Fully EU/sovereign, free.
  3. **End state (TAPPaaS):** static site served by **Caddy on a TAPPaaS module**, built by a
     **self-hosted Woodpecker** instance, with **self-hosted per-PR previews** at
     `pr-<n>.staging.tappaas.org` (Caddy + TAPPaaS's existing ACME).
- **Option B — Jump straight to Codeberg Pages.** Mirror/move the repo to Codeberg now and use
  Codeberg Pages for prod + staging immediately. Fastest route to sovereign hosting; couples the
  website move to the (not-yet-scheduled) source move.
- **Option C — Self-host on TAPPaaS now.** Stand up the Caddy-served build on a TAPPaaS box today.
  Maximum dogfooding, but highest upfront effort and ops burden before the rest of the rework lands.

**Recommendation:** **Option A** — build the pipeline **host-agnostic today** and migrate the publish
target GitHub → Codeberg Pages → self-hosted Caddy as the source move and TAPPaaS hosting mature.
Adopt **Woodpecker CI** as the CI target: it is **the CI Codeberg actually offers** ("Codeberg CI"),
it is open-source and self-hostable, and it is **the same engine we run on TAPPaaS at the end state**
— so the CI system never changes across the migration. Kroki already runs as a self-hosted service
container (Woodpecker supports `services:`), so there is no proprietary dependency to remove.

> **Decision (open decision #7): Option B — move the Documentation repo to Codeberg now.** Rationale:
> it gives us a sovereign place to **build, debug and review this major (2.0) upgrade** on Codeberg
> Pages **while GitHub keeps publishing the live 1.x tappaas.org untouched**. This is the cleanest
> realisation of the #5 cutover (1.x stays live until 2.0 is ready). Concrete shape:
>
> - **Set up the Codeberg `TAPPaaS` org fully** (ready to be the long-term sovereign home).
> - **Move `TAPPaaS/Documentation` to Codeberg as its primary** and do all upgrade work there, with
>   **Woodpecker CI (Codeberg CI)** building **staging + per-PR previews** on **Codeberg Pages**.
> - **Keep the GitHub `Documentation` repo as the production publisher** of tappaas.org (1.x) during
>   the transition — the live site does not change until the one-time 2.0 cutover (WS6 §10).
> - **Do *not* move the TAPPaaS source code yet — it stays on GitHub.** The WS0 sync-runner therefore
>   fetches source **cross-forge from GitHub** (public repo, pinned ref). Only `Documentation` lives
>   on Codeberg for now; the source follows GitHub until a later, separately-scheduled move.
>
> Net effect: we skip the "interim previews on GitHub" hop of Option A and go straight to the Codeberg
> bridge for *this repo*, because that is precisely where the risky work needs a safe review surface.

### 11a.3 Environments model (transition state)

Three tiers. During the transition, **production lives on GitHub (1.x)** and **staging/preview live
on Codeberg (2.0)** — a deliberate split so the live site is never at risk while we build:

| Tier | Forge / host | Trigger | URL | TAPPaaS source pin (WS0/WS6) |
|------|--------------|---------|-----|------------------------------|
| **Preview** | Codeberg → Codeberg Pages | any open PR | per-PR preview URL | target branch |
| **Staging** | Codeberg → Codeberg Pages | `staging`/`next` branch | `staging.tappaas.org` | GitHub `main`/next — preview 2.0 / ADR-007 |
| **Production (1.x)** | GitHub → GitHub Pages | push to `main` | `tappaas.org` | GitHub `stable` |

At **cutover** (WS6 §10), production is repointed to the Codeberg-built 2.0 site (Codeberg Pages, or
later self-hosted Caddy), and the GitHub `Documentation` repo/publish is retired. Post-cutover all
three tiers live on Codeberg (then progressively on self-hosted Caddy).

This dovetails with **WS6**: staging is exactly the `main`/next preview build (open decision #6) — it
previews upcoming **2.0 / ADR-007** content *and* upcoming TAPPaaS source before prod cutover.

> **Publish rule (decided).** [`CLAUDE.md`](../CLAUDE.md) currently says commit straight to `main` and
> it auto-deploys. Under staging: **small edits may commit straight to the working branch; substantial
> changes go PR → Codeberg preview → review → merge.** Update `CLAUDE.md` to this once the
> Codeberg/staging move lands. **CI = Woodpecker (Codeberg CI)** (confirmed).

### 11a.4 Tasks

- [ ] **Set up the Codeberg `TAPPaaS` org** (accounts, teams, org settings) as the sovereign home.
- [ ] **Move `Documentation` to Codeberg as primary** (import repo + history); leave GitHub
      `Documentation` in place as the 1.x production publisher during transition.
- [ ] Port the build to a **Woodpecker pipeline** (`.woodpecker.yml`) on Codeberg CI (checkout, pip,
      **Kroki `services:` container**, `mkdocs build --strict`); keep it host-agnostic (build → static
      `site/` → pluggable publish).
- [ ] Enable **Codeberg Pages** for staging + per-PR previews; add `staging.tappaas.org` DNS + TLS
      (`CNAME staging → tappaas.codeberg.page.`, Cloudflare **grey cloud / DNS-only**; `.domains` file).
- [ ] Wire PR builds to publish a preview and comment the URL on the PR.
- [ ] Confirm WS0 sync-runner **fetches TAPPaaS source cross-forge from GitHub** (public, pinned ref).
- [ ] Leave GitHub `main` → GitHub Pages publishing **unchanged** for 1.x production.
- [ ] Update `CLAUDE.md` + `README.md`: work happens on Codeberg; production still on GitHub until cutover.
- [ ] Define the cutover step (repoint prod to Codeberg Pages / self-hosted Caddy; retire GitHub publish).

### 11a.5 Codeberg CI / Pages bring-up — as-built checklist

Reproducible path for standing up staging (and, later, the `tappaas.org` production cutover, which
walks the same steps). `[x]` = done during first bring-up (2026-07-10).

- [x] Create Codeberg org `TAPPaaS`; migrate `Documentation` repo from GitHub (New Migration).
- [x] Add SSH key to Codeberg (reused `~/.ssh/id_rsa`); `ssh -T git@codeberg.org` greets you.
- [x] Repoint local remotes: `origin` → Codeberg (SSH), `github` → GitHub; branch tracks `origin`.
- [x] Add [`.woodpecker.yml`](../.woodpecker.yml) (build MkDocs + Kroki service → publish `site/` to
      the `pages` branch) and [`.domains`](../.domains) (`staging.tappaas.org`) — Codeberg-only commits.
- [x] Enable **Codeberg CI** for the repo at **ci.codeberg.org** (separate app, not codeberg.org settings).
- [x] Add Woodpecker secret **`codeberg_token`** (Codeberg application token, **repo write** scope) in
      the repo's settings on ci.codeberg.org; allow it on the `push` event.
- [x] First pipeline run: clone → build → deploy green; `pages` branch auto-created.
- [x] Cloudflare DNS: `CNAME staging → tappaas.codeberg.page`, **grey cloud (DNS-only)**.
- [ ] **Codeberg on-demand TLS cert for `staging.tappaas.org`** — *pending* (see gotchas / status).

**Gotchas learned (save future-us the pain):**

1. **Woodpecker secret syntax** — use `environment: { VAR: { from_secret: name } }` (Woodpecker 2.x/3.x);
   the old top-level `secrets: [ ... ]` list was removed → pipeline won't parse.
2. **Manual runs** fire `event: manual`; if `when:` only lists `push`/`pull_request` you get
   *"no matching workflow found"*. Include `manual`.
3. **Services aren't on `localhost`** — reach them by service name (`http://kroki:8000`); the build
   `sed`s `mkdocs.yml` (which defaults to `localhost:8000` for the GitHub build).
4. **Service exit code 143** (= 128+SIGTERM) is **normal** container teardown, not a failure.
5. **DNS negative cache** — after adding the CNAME, flush macOS
   (`sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`) **and** Firefox's DNS cache, or
   you'll see "server not found" even though public resolvers (dig `@1.1.1.1`) already resolve it.
6. **Cloudflare must be grey cloud (DNS-only)** — orange-cloud proxy makes Cloudflare terminate TLS
   and hide the `Host`, breaking Codeberg's cert issuance and routing.
7. **Do NOT hammer HTTPS while the cert issues.** Codeberg uses **on-demand TLS**; Let's Encrypt caps
   **failed validations at 5/hour/hostname**. Aggressive polling or browser-reloading *exhausts the
   quota and blocks issuance*. Probe at most every ~15 min; if stuck, **back off ~1h** to let the
   window clear. (We tripped this on first bring-up.)
8. **No CAA record** on `tappaas.org` that would block Let's Encrypt (verified — apex has no CAA).

**Test status — 2026-07-10:**

| Check | Result |
|-------|--------|
| Woodpecker pipeline (clone/build/deploy) | ✅ green |
| Content at `tappaas.codeberg.page/Documentation/` | ✅ serves (redirects to staging canonical) |
| DNS `staging.tappaas.org` → `tappaas.codeberg.page` → `217.197.84.141` | ✅ resolves globally |
| HTTP (:80) | ✅ 302 → https (domain recognised, `.domains` read) |
| HTTPS (:443) cert | ⏳ pending — issuance rate-limited; backing off ~1h then re-checking |

---

## 12. WS0 — Source-sync mechanism (cross-cutting enabler)

Both WS3 and WS4 depend on pulling content from the TAPPaaS repo. Build one reusable pipeline:

- A **CI step** (runs in **Woodpecker / Codeberg CI**) that fetches TAPPaaS **cross-forge from
  GitHub** — the source code stays on GitHub for now (open decision #7), so the runner clones/pulls
  `github.com/TAPPaaS/TAPPaaS` at a **pinned ref** (`stable` for prod content, `main`/next on
  staging) — reads an **allow-list** of files (`INSTALL.md`, `INSTALL-ENVIRONMENT.md`, selected
  `src/**/README.md`, `docs/ADR/ADR-007*`), and **transforms** them into site pages: rewrite
  relative links, inject front matter/nav, prepend a "generated from `<ref>` — edit upstream" banner.
  (When the source later moves to Codeberg, only the fetch URL changes.)
- **Guardrails:** fail the build if an expected source file is missing/moved (catches drift), and
  keep the allow-list explicit so internal/WIP docs don't leak.
- Options for the mechanism: git submodule + `mkdocs` snippets, a `fetch+transform` script in CI, or
  the `mkdocs-multirepo`/`monorepo` plugin. Prefer a **small explicit script** for full control over
  transforms and banners.

This is the highest-leverage early build: it turns "installation and manual drift" from a recurring
chore into a solved problem.

---

## 13. Phasing

**Phase 0 — Enablers (do first)**
- WS-S: set up Codeberg `TAPPaaS` org; move `Documentation` to Codeberg; Woodpecker (Codeberg CI) +
  Codeberg Pages for staging + per-PR previews (GitHub keeps publishing 1.x production).
- WS0 source-sync pipeline (skeleton; fetches TAPPaaS cross-forge from GitHub, pinned to `stable`).
- WS1 framework spikes (A vs B) and decision — built on the Codeberg/Woodpecker pipeline.
- Import presentation assets from Nextcloud into `docs/assets/` (unblocks WS2).

**Phase 1 — Public face**
- WS2 messaging + front page + Examples.
- WS3 installation macro-stages + hardware personas (consuming WS0).
- WS6 stable-vs-main page.

**Phase 2 — Reference depth**
- WS4 Operate/Develop split + README sync + ADR-007 architecture spine.
- WS5 roadmap rewamp.

**Phase 3 — Polish & cutover**
- One-time flip: repoint production to ADR-007 / 2.0 content when it hits `stable` (retire 1.x, no archive).
- Design-system consistency pass, performance, analytics.

---

## 14. Open decisions / inputs needed

1. ~~**Presentation assets — where are they?**~~ **Resolved.** Located in Nextcloud at
   `.../RossenConsulting/TAPPaaS/Marketing`: promo script + teleprompter (storyline SSOT), three
   slide PNGs, and three decks (see WS2 §6.2). The promo script is now the canonical front-page
   narrative. Remaining sub-question: **confirm which named-adopter claims are cleared for public use.**
2. ~~**Framework direction:** confirm we run the A-vs-B spike?~~ **Resolved — yes, run the spike**
   (deferred until planning is signed off; it's the first Phase 0 build action). Sub-question kept
   open: whether decoupled Option B (two toolchains) is operationally acceptable — to be judged *from
   the spike results*, not decided up front.
3. ~~**Install content model:** sync-runner vs reference-out?~~ **Resolved — sync-runner**
   (on-site, always current, generated from pinned source). This is WS0.
4. ~~**Hardware personas:** review the categories.~~ **Resolved — two-axis model** (§7.3): size tier
   (Evaluation / Home / SMB / Scale-out) × capability options (± local AI, ± local backup, ± local
   public IP), with the **satellite (ADR-010)** as the no-IP / no-local-backup escape hatch. Structure
   confirmed; **no budget bands** (spec-only); **GPU/VRAM guidance added** (§7.3 — unified-memory APU
   reference + discrete-GPU path, sized by model×quantization). *Caveat:* ADR-010/satellite is still
   **draft/scaffolding upstream** — the docs should track its readiness, not imply it's shippable
   before it is.
5. ~~**Versioning scope:** preserve 1.x after 2.0?~~ **Resolved — no.** Clean flip, no `mike`/
   multi-version tooling. But keep 1.x **live until 2.0 is ready**: prod stays 1.x, 2.0 builds on
   staging, then a one-time cutover repoints prod (WS6 §10).
6. ~~**`main` preview build:** wanted or public-only?~~ **Resolved implicitly by #7** — yes: the
   Codeberg **staging** tier *is* the `main`/next preview build (pinned to GitHub `main`/next),
   separate from GitHub production (1.x).
7. ~~**Migration timing:** A / B / C?~~ **Resolved — Option B, scoped to `Documentation` only.** Move
   the `Documentation` repo to **Codeberg now** (dev/staging/preview on Codeberg Pages via Woodpecker
   / Codeberg CI) as a safe surface to build & review the 2.0 upgrade, while **GitHub keeps publishing
   live 1.x**. Set up the Codeberg `TAPPaaS` org fully, but **keep the TAPPaaS source code on GitHub**
   for now (WS0 syncs cross-forge). See WS-S §11a.2 decision box.
8. ~~**CI target:** Forgejo Actions vs Woodpecker?~~ **Resolved — Woodpecker CI** (switched from
   Forgejo Actions): it is **the CI Codeberg actually offers** ("Codeberg CI"), open-source and
   self-hostable, and the **same engine we run on TAPPaaS at the end state** — so the CI never changes
   across the migration. Build ported to a `.woodpecker.yml`; Kroki stays a `services:` container.
9. ~~**Publish policy:** direct-to-main vs PR→preview→review?~~ **Resolved — both, by change size.**
   Small edits may commit straight to the working branch; **substantial changes go PR → Codeberg
   preview → review → merge.** `CLAUDE.md` to be updated to this once the Codeberg/staging move lands.

---

## Relationship to the old `ARCHITECTURE_PLAN.md`

`ARCHITECTURE_PLAN.md` was an earlier, largely generic plan that assumed a Heroku/Kubernetes-style
PaaS (CLI reference, REST/GraphQL APIs, Helm charts, multi-tenant app scaling) that **does not match
what TAPPaaS is**. Its useful ideas (audience personas, progressive disclosure, hub pages, templates,
cross-linking discipline) are folded into this ADR; its inaccurate feature assumptions are dropped.
It has been **sunset (removed from the repo)** in favour of this ADR to avoid confusion — the prior
content remains recoverable from git history.

---

## Version history

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-07-09 | Draft | Initial upgrade plan |
