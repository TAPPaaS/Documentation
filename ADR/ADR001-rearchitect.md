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
- [x] Spike A: a redesigned MkDocs landing (custom template + CSS/JS + motion) on a branch.
- [x] Spike B: a small Astro/Next landing that links into the existing docs.
- [x] Side-by-side review; decide A / B / C and record the decision in this file.
      **Decided (2026-07-10, Lars): Option B** — see the decision box in §5.5.
- [x] Define the shared design tokens (color, type, spacing) so marketing + docs stay consistent
      *(first cut: identical `--tap-*` token values in both spikes — teal/amber palette, radius,
      type scale; to be extracted into a shared tokens file once A/B is decided).*

> **Decision (2026-07-10, Lars): Option B — decoupled Astro landing + MkDocs docs**, with three
> design constraints from the review:
>
> 1. **Less "black"** — drop the dark cinematic palette for a lighter visual language closer to the
>    docs theme (light surfaces, teal accents; dark mode follows the visitor's preference).
> 2. **Smooth the landing → docs transition** — shared palette/typography and a "explore the
>    documentation" bridge on the landing, so crossing into the docs doesn't feel like a site
>    change. Lars notes this pull, taken to its end, *implies drifting toward Option C* (one
>    unified framework); we accept that as a **possible later evolution** (Astro → Starlight is a
>    natural path) but do **not** migrate the docs corpus now — revisit only if the docs
>    experience itself becomes the bottleneck (consistent with §5.2).
> 3. **Clarity over spectacle** — TAPPaaS explains complex information; the front page must make
>    navigation obvious (clear section nav, explicit paths into Install/Docs), not add confusion.

> **Graduated (2026-07-10):** after the light restyle was approved, the Option B landing was
> promoted to `main` — the staging root now serves the Astro landing with the MkDocs docs under
> `/docs/`. The landing build is path-relative (no Astro `base`; CI relativizes asset URLs), so one
> artifact serves staging, the codeberg.page sub-path, and branch previews. `spike-b` merged and
> deleted; `spike-a` kept as the A-reference.

> **Decision revised (2026-07-10 review, Lars): converge the frameworks.** Living with the
> two-site split showed the seam: landing → docs-home → nav was not one logical structure. New
> direction: **one framework (MkDocs Material) serving one site** — the landing *is* the home
> page, rendered by a custom Material home template that carries the approved Option-B visual
> design. Requirements from the review:
>
> 1. The site root **is** the landing; the separate "documentation home" page and the `Home` nav
>    tab are gone — the logo/title click returns to the landing.
> 2. **Top navigation for sections, side navigation for real content** (Material tabs + sidebar).
> 3. **Header is a single line**: brand, section menus, and search together (custom header
>    partial that inlines the tab links; the separate tabs bar is dropped).
>
> Consequences: the Astro `landing/` app and its CI step are **retired** (design ported into
> `overrides/home.html` + `landing.css`); docs move back from `/docs/` to the site root (inbound
> links are explicitly not a concern — the site is new). Astro Starlight remains the eventual
> Option-C path only if the docs experience itself ever demands it.

### 5.5 Spike status (2026-07-10) — reviewed, Option B chosen

Both spikes are live on branch previews, built by the sovereign Woodpecker/Codeberg pipeline
(per the §5.2 decision box). **Copy is identical** (promo storyline §6.1) so the review compares
frameworks, not content:

| Spike | Branch | Preview URL | Shape |
|-------|--------|-------------|-------|
| **A — MkDocs Material, enhanced** | `spike-a` | <https://tappaas.codeberg.page/Documentation/spikes/spike-a/> | Custom `home.html` template (`theme.custom_dir`) + `landing.css`/`landing.js`. One toolchain; landing lives inside the Material shell (header/tabs/search kept). |
| **B — Decoupled Astro landing** | `spike-b` | <https://tappaas.codeberg.page/Documentation/spikes/spike-b/> | Astro 5 app in `landing/` (zero extra deps) at the site root; untouched MkDocs site built to `/docs/` behind it. Two toolchains in one pipeline (extra `node` CI step, ~1–2 min). |

Observed trade-offs to weigh in the review (§5.3 criteria):

- **A**: cheapest to run and author (Markdown + one template); visual ceiling is real — the landing
  sits inside Material's header/nav chrome, shares its fonts/breakpoints, and fights the theme's
  CSS specificity. Material's *instant navigation* also constrains per-page JS/CSS tricks.
- **B**: full design freedom (own typography, header, interactions) and a clean seam — the docs
  corpus, Kroki pipeline and search are untouched under `/docs/`. Costs: a second toolchain
  (npm/Astro) in CI, a visual seam between landing and docs (mitigated by shared tokens), and two
  places to keep brand assets until a design-token file is extracted.
- **Long-run lean (to validate in review):** B, because it also de-risks a later Option C — the
  landing framework (Astro) is the same family as Astro Starlight, so if the docs experience ever
  needs migrating, the marketing layer is already there; meanwhile MkDocs keeps serving the 90-page
  corpus unchanged.

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

- [x] Rewrite `docs/index.md` around the promo storyline (§6.1); delete generic-PaaS copy.
      *(2026-07-10: the marketing story now lives on the graduated Astro landing (site root); the
      MkDocs home at `/docs/` became a clean documentation hub. Generic-PaaS copy deleted.)*
- [x] Copy/export the marketing assets (§6.2) into `docs/assets/`; establish an assets convention.
      *(Done 2026-07-10: slide-1..3 downscaled 4K→1920 px in `docs/assets/marketing/`; script +
      slides-pptx sources in `marketing-material/5min-pitch/` — published exports in `docs/`, editable
      sources in `marketing-material/`, bulky decks stay in Nextcloud. See
      `marketing-material/5min-pitch/README.md`.)*
- [ ] Redraw continuum + four-blocks diagrams as Kroki/Mermaid (theme-aware) where worthwhile.
      *(Deferred: the Why page uses the slide PNG exports for now; the landing draws the continuum
      in HTML/CSS. Revisit when the design-token pass lands (Phase 3).)*
- [x] Consolidate `intro/*` into a lean set (kill duplication with the front page).
      *(2026-07-10: `intro/` = Why TAPPaaS (full storyline + slides) · Digital Sovereignty ·
      Examples. `vision.md`/`problem.md`/`approach.md` retired — their substance folded into the
      Why page (audiences, curation/integration/automation, platform democracy, principles).)*
- [x] Present the four building blocks consistently with the ADR-007 taxonomy (align with WS4 §8.3).
      *(The Why page names Site · Workloads · People · Environments and links them explicitly to
      the technical taxonomy + Architecture section.)*
- [x] Build the Examples gallery from real `src/apps` modules (the "running today" proof).
      *(`intro/examples.md`: 12 real modules incl. Vaultwarden, NetBird, Windows Server —
      verified against `src/apps` on `main` 2026-07-10 — grouped by story, each linking its
      install guide or module source; plus multi-tenant (INSTALL-VARIANT) and 00-Template hooks.)*
- [x] Copy-review pass: no "CLI/scale/multi-tenant/ship faster" unless literally true.
      *(Grep-verified: only remaining hit is a factual "Cloud-native" descriptor of Zitadel.)*
- [ ] Get sign-off before publishing any named-adopter/logo claim.
      *(Nothing to sign off yet — the site says "first adopters" generically, no names/logos.)*

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

- [x] Build the WS0 sync-runner for `INSTALL.md` + `INSTALL-ENVIRONMENT.md`.
      *(Skeleton done 2026-07-10: [`scripts/sync-source.py`](../scripts/sync-source.py) — see §12.
      Upstream reality check: `INSTALL-ENVIRONMENT.md` is now `INSTALL-VARIANT.md`, and `stable`
      has **neither** file yet — so the sync pins to `main` until 2.0 lands on `stable`.)*
- [x] Restructure `installation/index.md` around the 7 macro stages with a progress model.
      *(2026-07-10: overview table (stage / you'll need / done when) + per-stage sections, each
      with prerequisites, "done when", and links to the existing pages + synced INSTALL.md.)*
- [x] Rewrite `hardware-selection.md` around the two-axis model (size tier × capability options).
- [x] Add a "Choose hardware" **decision flow** (the 4 steps above) with per-tier sizing tables.
- [x] Add the **GPU/VRAM guidance** table for local AI; sync model/throughput numbers from `vllm-amd`.
      *(Numbers hand-verified against the `vllm-amd` README 2026-07-10 (50 tok/s 7B FP16, 20 tok/s
      30B GPTQ, gpt-oss-120B largest tested, no FP8 on gfx1151) with a provenance note on the page;
      the automated WS0 sync of these figures is still to do.)*
- [x] Document the **satellite (ADR-010)** as the no-public-IP / no-local-backup path.
      *(Documented with an explicit "upstream status: design phase" warning — verified 2026-07-10
      that upstream has only ADR-010 + implementation design, **no module yet**, so there is no
      README/INSTALL to sync; the page links the upstream docs and tracks readiness.)*
- [x] Add the multi-tenant/Environments path for Scale-out.
      *(Via the synced `INSTALL-VARIANT.md` — upstream renamed `INSTALL-ENVIRONMENT.md` — linked
      from the install overview, the hardware page's Scale-out tier, and Examples.)*
- [x] Add stable-vs-main install guidance (WS6) at the top of the install flow.
      *(Warning box atop `installation/index.md`: install 1.x from `stable`; `main` = 2.0/ADR-007
      preview for evaluators/contributors. The full WS6 explainer page is still open.)*

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

> **2026-07-10 review (Lars): the Operate content must reflect the manager/controller paradigm.**
> The first WS4 pass synced from `main`, which still had the old standalone-scripts world — but
> 2.0 (branch `ADR007`, soon `stable`) replaces it: **managers** realize the taxonomy domains
> (site-, people-, module-, environment-, network-, backup-, health-, satellite-manager) and
> **controllers** wrap concrete systems (opnsense, proxmox, identity, backup, ap, switch,
> node-provisioner); the old `install-module.sh`-style scripts now live *inside* managers.
> Actions: re-pin WS0 to `ADR007` (§12.1); **delete** the 19 hand-written `manual/scripts/*`
> pages and the stale module/update/backup/opnsense manual pages; rebuild Operate around the
> glob-synced manager/controller READMEs.

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

- [x] Design the Operate vs Develop nav (see §10) and migrate existing pages into it.
      *(2026-07-10: nav = Home · Why TAPPaaS · Install · Operate · Develop · Roadmap · About.
      **Paths kept** — Operate is `manual/*`, Develop is `architecture/*` + ArchiMate — so no URLs
      break; only nav labels and section pages changed. `appendix/index.md` stub retired.)*
- [x] Extend WS0 to sync an allow-listed set of `src/**` reference docs into Operate/Develop pages.
      *(Synced: ZONES.md, CONFIGURATION.md, opnsense-controller README → Operate;
      ADR-007 taxonomy, 00-Template README → Develop. The script now handles upstream paths with
      spaces and `[x](<angle bracket>)` links. Evaluated-and-skipped: `src/README.md` and
      `src/foundation/README.md` — 2-line stubs pointing back at tappaas.org.)*
- [x] Rebuild the architecture overview around the ADR-007 taxonomy.
      *(`architecture/index.md` now opens with the Site + 3-domains + Health-lens model (accurate
      to upstream ADR-007 v2.3, incl. "Health is a lens, not a domain"), maps it to the front-page
      four-blocks wording, flags 2.0 status honestly, and links the synced ADR text.)*
- [x] Fold the ArchiMate appendix into Develop (it's contributor-facing reference).
- [x] Add a contributor "author a module" guide from the `00-Template` + schemas.
      *(`architecture/author-a-module.md`: 5-step path — template copy, module contract/schemas,
      environments/zones placement, install/update/test scripts, good-citizen criteria — linking
      the synced template README and field-definition JSONs.)*

---

## 9. WS5 — Roadmap

**Goal:** a roadmap that stays current with near-zero maintenance.

The page already links to [GitHub milestones](https://codeberg.org/TAPPaaS/TAPPaaS/milestones); the
problem is the *hand-maintained* timeline and status note that go stale. Options:

- **Replace** the static timeline with a short "how we plan" explainer + a live pointer to
  milestones/issues (optionally auto-embedded via CI). Lowest maintenance.
- **Rewamp**: keep a light phase narrative (Framework → MVP → 2.0/ADR-007 → Growth) but remove all
  dated status claims, and let milestones carry specifics.

**Recommendation:** rewamp to a thin, dateless phase narrative anchored to the 2.0/ADR-007 milestone,
plus a CI-refreshed milestone list. Remove the "on track for Q1 2026" style claims entirely.

### 9.1 Tasks

- [x] Strip dated status assertions from `roadmap/index.md`.
      *(2026-07-10: dateless phase timeline (Framework → MVP → 1.x → 2.0/ADR-007 → Growth); the
      only status claim left — "1.x released and running on real systems" — is date-free and true.)*
- [x] Add a short "how we plan / where to look" section pointing at milestones + this upgrade plan.
- [ ] (Optional) CI job to render current open milestones into the page at build time.
      *(Deliberately skipped for now: unauthenticated GitHub API calls from shared CI runners are
      rate-limit-flaky and would make builds nondeterministic. Revisit with a token if wanted.)*

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
v2 on Codeberg). **Proven end-to-end (2026-07-21) by `staging.tappaas.org` and `www.tappaas.org`:**
CNAME → routing → per-domain deployment → auto TLS → serving, all on the same target that will serve
production.

**Codeberg git-pages specifics (as-proven):**

- The CNAME target is **`documentation.tappaas.codeberg.page`** — the *new* git-pages server encodes
  `<repo>.<owner>` in that subdomain and **routes custom domains by resolving that CNAME target**.
  The legacy **`.domains` file is deprecated** and no longer used.
- **Deployments are per-domain** — the docs' *"deploy your website to both domains (i.e. set up two
  separate webhooks)"* is load-bearing. Each hostname needs its own deploy trigger: a Forgejo-style
  push webhook POSTed **to that hostname's own URL**. A domain that is routed but never deployed
  serves HTTP 302s **but never gets a TLS cert** — this cost us a day on `www` (misdiagnosed as
  Let's-Encrypt backoff) until a single hand-fired webhook answered `created` and the cert issued
  within ~2 minutes. The pipeline's `notify()` list in [`.woodpecker.yml`](../.woodpecker.yml) now
  POSTs to every served domain on each deploy (canonical + staging + www; apex line ready).
- **Cert issuance happens as part of a domain's deployment** — not on browser demand. If HTTPS gives
  `tlsv1 alert internal error` while HTTP :80 302s, the domain is routed-but-undeployed: fire its
  webhook (over `http://` — TLS isn't up yet), don't wait.
- **Cloudflare proxy must be OFF (grey cloud / DNS-only)** on every record pointing at Codeberg — an
  orange-cloud proxy terminates TLS at Cloudflare and hides the real `Host`, so Codeberg can't issue
  its cert or route. Corollary: never grey-cloud a record *still pointing at GitHub Pages* — GitHub
  has no cert for the bare domain and HTTPS breaks instantly (this briefly took production down).
- **Authorization TXT (`_git-pages-repository.<host>`)**: not needed for a subdomain whose CNAME
  target already encodes the repo (`www`/`staging` work without it). It **is** the documented
  mechanism when DNS doesn't reveal the repo — i.e. **the apex**: Cloudflare's flattening answers
  A/AAAA and hides the CNAME target from external queries, so add
  `TXT _git-pages-repository.tappaas.org = "https://codeberg.org/TAPPaaS/Documentation.git"`.

**Apex wrinkle.** `tappaas.org` is an apex; DNS forbids a real CNAME there. On **Cloudflare** (current
provider) **CNAME-flattening** fakes it — enter a CNAME at `@` and it serves A/AAAA at query time
while still tracking Codeberg's IP (but hidden from external queries, hence the TXT above).

Steps (Cloudflare) — `www` completed 2026-07-21, apex remaining:

1. **Lower the TTL** on the record ~a few hours ahead (fast flip + fast rollback). *(done)*
2. **Note the current A/AAAA values** (GitHub Pages) so rollback = re-create them. *(done)*
3. **Repoint DNS** — delete the apex **A + AAAA** records and add a single
   **`CNAME @ → documentation.tappaas.codeberg.page`, grey cloud** (a CNAME can't coexist with
   A/AAAA; the apex relies on flattening). Add the **`_git-pages-repository` TXT** (above).
   *(www: done, works)*
4. **Deploy to the domain** — uncomment the apex `notify` line in `.woodpecker.yml` and push, or
   hand-fire the webhook once at `http://tappaas.org` (expect `created`). The Let's Encrypt cert
   issues within minutes of the deployment. Verify with one request, not a reload-storm (failed
   validations are capped at 5/hour/hostname).
5. **Canonicalize** — add **`docs/_redirects`** so `www` redirects to the apex
   (`//www.tappaas.org/* https://tappaas.org/:splat 302!` — the trailing `!` is required).
6. **Verify** `https://tappaas.org` serves the 2.0 site, then **retire GitHub Pages** (remove
   `docs/CNAME` + the Pages custom-domain setting). Keep the GitHub repo intact as rollback.

`staging.tappaas.org` stays on the same target, so it and `tappaas.org` serve **identical** content
until/unless staging is split onto its own branch/deployment. **Trust note:** on Codeberg Pages,
Codeberg terminates TLS for `tappaas.org` — acceptable for a public static site.

> **Fronting note (2026-07-21):** a third party CNAME-ing their own domain at
> `documentation.tappaas.codeberg.page` *and* deploying to it could serve our (public, unmodified)
> content under their name — Codeberg's countermeasure is the per-domain webhook + DNS authorization
> above; the `_redirects` canonical rule further bounces stray hosts to `tappaas.org`. Low risk for
> a public docs site; noted for completeness.

**Cloudflare → deSEC later (apex catch — decided guidance).** `www` (a subdomain) keeps its CNAME on
any provider. The **apex is the problem**: **deSEC has no CNAME-flattening**, so `tappaas.org` would
need **A/AAAA to Codeberg's Pages IPs** — but git-pages identifies the repo from the **CNAME target**,
so a bare A/AAAA apex loses that routing hint and **may not resolve to the Documentation repo at all**
(verify apex support in `docs.codeberg.org/codeberg-pages/` at the time). Therefore **the deSEC move
pairs naturally with self-hosting the site on TAPPaaS**: apex A/AAAA → the site's own public IP (or
the ADR-010 satellite `reverse-proxy`), with **Caddy** serving the static build and issuing TLS via
**deSEC DNS-01** (already used by TAPPaaS) — removing both Cloudflare and Codeberg from the path. Do
**not** move DNS to deSEC while still depending on a Codeberg *apex* CNAME; `www` can move anytime.

### 10.2 Tasks

- [ ] Public build pins to `stable`; 2.0 content lives on staging until go-live.
      *(Blocked upstream: `stable` (1.x) has no INSTALL.md / ADR-007 files to sync — the pin flips
      via `TAPPAAS_SOURCE_REF=stable` at cutover; see §12.1.)*
- [x] Write the "stable vs main / what is 2.0 (ADR-007)" page.
      *(2026-07-10: `installation/versions.md` — branch table, the 2.0 taxonomy in brief, status
      honesty note, and the cutover story; linked from the install-flow warning box and nav.)*
- [x] Confirm the DNS provider's apex capability (ALIAS/flatten vs A/AAAA) for `tappaas.org`.
      *(Cloudflare flattens CNAME at apex ✓; and the staging bring-up established the git-pages
      recipe — repo-qualified CNAME target + optional `_git-pages-repository` TXT — which is the
      same recipe the apex cutover will use, §11a.5 fact 4.)*
- [x] Execute the §10.1 cutover runbook (repoint prod to 2.0; retire 1.x — no archive).
      *(**Done 2026-07-21**: apex flipped to the flattened CNAME + `_git-pages-repository` TXT,
      apex deployment webhook answered `created`, LE cert issued in ~3 min, `https://tappaas.org`
      serves the 2.0 site from Codeberg. `www` cut over the same day; `_redirects` canonicalizes
      www→apex. GitHub Pages + its workflow retired; the GitHub repo remains as a frozen archive.)*
- [ ] Sequence the ADR-007 content publish to coincide with the `stable` merge (ties to WS4 §8.3).

---

## 11. Proposed information architecture (target)

> **Realised 2026-07-10** — the nav below is now live on staging (URLs kept: Operate = `manual/*`,
> Develop = `architecture/*` + ArchiMate; only labels/section pages changed).

> **Evolved 2026-07-11 (Lars review):** the IA split further into
> `Why · What · Install · Operate · Develop · Stacks · Roadmap · About` — all URLs kept:
>
> - **Why** (renamed from "Why TAPPaaS"): story, sovereignty, examples.
> - **What** (new): Capabilities · Principles (Design Principles + Software Selection, the latter
>   moved out of Solution Design) · Categories & Ontology (taxonomy moved from Develop, merged with
>   the newly-synced upstream `ontology.md` — resolving ADR-013 open question 3) · Foundation (the
>   rest of Solution Design, retitled) · ADRs (new overview page pointing at the source repo).
> - **Develop** now concentrates on module development: Author a Module + "How the CICD works"
>   (renamed CICD Design) + Meta Model + ArchiMate; overview rewritten around the module/CICD story.
> - **Stacks** (new): the Module Designs pages, one per stack (Foundation/AI/Productivity/Home/DevOps).

> **Install restructure (2026-07-11 review):** Install = Overview · Hardware Selection ·
> Preparation (completely rewritten as one concise checklist, with **Branch Selection** — ex
> "Stable vs Main" — as its sub-page, incl. a transitional "Migrating from ADR007 to 2.0"
> subsection to delete after promotion) · **Install Foundation** (the synced INSTALL.md, retitled) ·
> **Add an Environment** (synced INSTALL-ENVIRONMENT + the satellite pages) · **Add Stacks** ·
> and the stage model became: hardware → prepare → bootstrap (now including network cut-over,
> DNS/TLS and switch management) → grow → **add environments (incl. satellites)** → add stacks →
> operate. The 8 hand-written 1.x-era `installation/foundation/*` pages were deleted as outdated.
> Upstream split: INSTALL.md (working tree, pending commit) lost its Prepare section — preparation
> lives on the site, INSTALL.md concentrates on installing. Synced pages: no "From Source" nav
> grouping and no reader-visible banner — provenance is now an HTML comment; titles are real
> ("Install Foundation", "Add an Environment", "Taxonomy", "Glossary", …).
>
> **Architecture & Stacks catalog (2026-07-11 review):** What → Ontology renamed **Architecture**
> and took Meta Model + ArchiMate Diagrams from Develop (kept as separate items). What → Foundation
> gained **Module Dependencies** — a mermaid graph now *computed from the module jsons* by a new
> upstream script (`src/generate-module-dependencies.sh`, with `--check` for CI) and synced; the
> hand-drawn stale graph is retired. The **Stacks** menu became a catalog: per-stack pages (incl.
> new IoT + honest DevOps-planned) whose entries link the **module READMEs**, now glob-synced
> (`src/foundation/*/README.md`, `src/apps/*/README.md` — new modules auto-appear). Upstream, the
> foundation capability diagrams moved into their module READMEs (names corrected) and the README
> template gained an optional "Alternatives considered" section, populated only where documented
> rationale exists. Develop now contains exactly: Overview · Author a Module · How the CICD works.

> **Add Stacks = module INSTALL.md (2026-07-11):** each stack item is now the module's synced
> INSTALL.md (vllm-amd/litellm/openwebui · nextcloud/n8n · hass/deconz); the seven hand-written
> pages were reconciled first (truth preserved upstream in DESIGN/ADMIN files, inconsistencies
> resolved by reality) and deleted. **ollama** (251-line page, no module — retired approach; its
> kernel became a LiteLLM "other backends" note) and **karakeep** (no module) have no pages;
> stack overview pages rewritten with honest statuses (n8n = placeholder) and correct zones.

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

### 11a.3 Environments model

**Post-cutover (as of 2026-07-21)** — all tiers live on Codeberg git-pages:

| Tier | Forge / host | Trigger | URL |
|------|--------------|---------|-----|
| **Preview** | Codeberg → git-pages | `spike-*` branch push | `tappaas.codeberg.page/Documentation/spikes/<branch>/` |
| **Production (2.0)** | Codeberg → git-pages | push to `main` | `tappaas.org` (+ `www`, `staging.tappaas.org`, the codeberg.page URL — same build) |

`staging.tappaas.org` currently serves the same deployment as production; splitting it onto its own
branch/deployment is possible later if a separate staging tier is wanted again. The next hop remains
**self-hosted Caddy on TAPPaaS** (§10.1 deSEC guidance).

*Transition-era model (historical): production 1.x stayed on GitHub Pages while 2.0 was built and
reviewed on Codeberg — the deliberate split that kept the live site risk-free during the rework.*

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
- [x] Update `CLAUDE.md` + `README.md`: work happens on Codeberg; production still on GitHub until cutover.
      *(Done 2026-07-10 — environments table, small-edit vs preview-branch publish rule, WS0 note.)*
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
- [x] **Temporary direct URL** (2026-07-10): the build is directly reachable at
      **<https://tappaas.codeberg.page/Documentation/>** — see the git-pages findings below for the
      mechanics. `.domains` is temporarily not published (with it present, the codeberg.page URL
      307-redirects to the TLS-broken staging canonical); staging is parked until the DNS fix below.
- [x] **Branch previews**: `spike-*` branches publish into `spikes/<branch>/` sub-directories of the
      single `pages` branch, served at `https://tappaas.codeberg.page/Documentation/spikes/<branch>/`.
      (The new git-pages server deploys **only** `refs/heads/pages` — the legacy `@branch` URL scheme
      is gone; sub-directories are the preview mechanism now.)

**Root cause found (2026-07-10, supersedes the Let's-Encrypt-rate-limit theory):** Codeberg is
migrating Pages to a **new "git-pages" server, mandatory for new orgs** — mid-bring-up, the legacy
server started answering **400 "new users/orgs are not allowed to use the old pages server"** for
everything. The staging cert never issued because the new server didn't know the site at all, not
because of LE rate limits. New-server facts (from <https://codeberg.page> + experiment):

1. **Deployment is webhook-driven, one webhook per deploy target (domain)**: a Forgejo push
   webhook targeting `https://<org>.codeberg.page/<Repo>` deploys the codeberg.page site; a second
   webhook targeting `https://staging.tappaas.org` deploys the same content to the custom domain.
   No webhook → no site. Creating webhooks via API needs a **repo-admin** token — the CI
   `codeberg_token` is write-only (`403 user should be an owner or a collaborator with admin write`),
   so the **deploy step self-notifies**: it POSTs the push payload to each target URL itself
   (unauthenticated; needs `ref: refs/heads/pages` + `repository.clone_url`; answers `created`).
   Optionally add the real webhooks by hand in repo Settings → Webhooks later — either works.
2. **Only `refs/heads/pages` deploys** (per-target allowlist); other refs are rejected, and
   `@branch` preview URLs are not supported — hence the `spikes/<branch>/` sub-directory scheme.
3. **~600 s edge cache** on served content — freshly deployed pages can lag up to 10 minutes.
4. **Custom domains are authorized in DNS, `.domains` is deprecated** (removed from this repo —
   with one present, the codeberg.page URL redirects to the "canonical" domain, which caused the
   earlier 307s). Empirically, the **repo-qualified CNAME is sufficient authorization**: with
   `CNAME staging.tappaas.org → documentation.tappaas.codeberg.page` (grey cloud), the deploy
   POST to `https://staging.tappaas.org` answered `202 updating` and the site went live — no TXT
   record was needed. The official docs
   ([using-custom-domain](https://docs.codeberg.org/codeberg-pages/using-custom-domain/)) instead
   describe `CNAME → codeberg.page.` **plus**
   `TXT _git-pages-repository.staging.tappaas.org → "https://codeberg.org/TAPPaaS/Documentation.git"`;
   adding that TXT anyway is cheap future-proofing should the CNAME-derived path change.
   The staging TLS cert was issued 2026-07-10 11:57 UTC. **Staging is live** ✦ the same DNS recipe
   applies to the production cutover later (WS6 §10.1, apex flattened-CNAME + TXT).

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
9. **Custom domain gets no cert but HTTP :80 302s?** It's **routed but never deployed** — git-pages
   deployments (and cert issuance) are **per-domain**; POST the push webhook to *that hostname's own
   URL* (over `http://`, TLS isn't up yet; expect `created`). This — not the rate limit — was the
   real cause of the multi-day `www.tappaas.org` cert failure (solved 2026-07-21; see §10.1).

**Test status — 2026-07-10:**

| Check | Result |
|-------|--------|
| Woodpecker pipeline (clone/build/deploy) | ✅ green |
| **`https://staging.tappaas.org/`** | ✅ **LIVE** — 200, valid LE cert (issued 2026-07-10 11:57 UTC) |
| Content at `tappaas.codeberg.page/Documentation/` | ✅ 200, serves directly (`.domains` removed — no more redirect) |
| DNS `staging.tappaas.org` CNAME → `documentation.tappaas.codeberg.page` | ✅ (Lars, 2026-07-10) — repo-qualified target doubles as deploy authorization |
| Optional TXT `_git-pages-repository.staging.tappaas.org` | ▫ not required in practice; add for doc-compliance when convenient (value: `https://codeberg.org/TAPPaaS/Documentation.git`) |
| Spike previews `…/Documentation/spikes/spike-a/`, `…/spikes/spike-b/` | ✅ build & serve via sub-directory preview pipeline |

> Transient Woodpecker failures observed twice: pipeline #3 (`clone` step died before any repo code
> ran) and pipeline #21 (the **kroki service failed to start**, so the build's wait-loop aborted
> with "Kroki did not become ready in time"). Both passed unchanged on re-run — if a pipeline fails
> in `clone` or in the kroki wait, just re-run it (empty commit or manual run) before debugging.

---

## 12. WS0 — Source-sync mechanism (cross-cutting enabler)

Both WS3 and WS4 depend on pulling content from the TAPPaaS repo. Build one reusable pipeline:

- A **CI step** (runs in **Woodpecker / Codeberg CI**) that fetches TAPPaaS **cross-forge from
  GitHub** — the source code stays on GitHub for now (open decision #7), so the runner clones/pulls
  `codeberg.org/TAPPaaS/TAPPaaS` at a **pinned ref** (`stable` for prod content, `main`/next on
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

### 12.1 As built (skeleton, 2026-07-10)

[`scripts/sync-source.py`](../scripts/sync-source.py), run by CI before `mkdocs build` (stdlib-only
Python, no git needed — fetches the GitHub tarball):

- **Allow-list** (in the script): `INSTALL.md`, `INSTALL-VARIANT.md` → `docs/generated/*` (git-ignored,
  regenerated every build), in the nav under *Installation → From Source (synced)*.
- **Transforms:** front-matter title; "generated from source — edit upstream" banner linking the
  upstream file at the pinned ref; relative links/images rewritten to absolute GitHub blob/raw URLs.
- **Guardrail:** build fails if an allow-listed file is missing at the ref (drift alarm).
- **Pin:** `TAPPAAS_SOURCE_REF` env var. **Default `ADR007` since the 2026-07-10 review** (was
  `main`): the docs must describe the manager/controller paradigm that ships as 2.0, and Lars will
  promote `ADR007` → `stable` per the roadmap. On that promotion, flip the default to `stable` and
  this note retires. (File-name whiplash for the record: `INSTALL-ENVIRONMENT.md` on `ADR007`,
  renamed `INSTALL-VARIANT.md` on `main`, absent on `stable` (1.x) — the allow-list tracks the
  pinned ref's names.)
- **Glob rules** (2026-07-10 review): besides exact files, the script expands patterns —
  `manager/*/README.md` and `controller/*/README.md` under `src/foundation/tappaas-cicd/` map to
  `generated/managers/<name>.md` / `generated/controllers/<name>.md`, and the script emits a
  `SUMMARY.md` per directory that **mkdocs-literate-nav** consumes — so a *new* manager or
  controller upstream appears in the nav on the next build with **zero docs-repo changes**.

> **Upstream governance (2026-07-10):** the sync model below is being sanctioned upstream as
> **ADR-013 — Documentation Structure and Standards** (drafted on the `ADR007` branch, from
> TAPPaaS/TAPPaaS#362): source-repo docs are the SSOT per audience; the site publishes curated
> narrative + allow-list/glob-synced source pages. Once ADR-013 is accepted, module/manager/
> controller READMEs are *by rule* public web pages — internal notes belong in DESIGN.md or issues.

### 12.2 Keeping synced content fresh (the "how do we keep it updated" answer)

Three layers, from automatic to one-time setup:

1. **Changed upstream content** — nothing to do. Every CI build re-fetches the pinned ref, so any
   push to this docs repo republishes current upstream content. The build **fails loudly** if an
   allow-listed file disappears (drift alarm) rather than silently serving stale pages.
2. **New upstream content** — the glob rules (§12.1) pick up new `manager/*`/`controller/*`
   READMEs automatically, including nav entries (generated `SUMMARY.md` + literate-nav). Content
   outside the glob shapes (a brand-new doc type) still needs one allow-list line in
   [`scripts/sync-source.py`](../scripts/sync-source.py) — deliberate, so internal/WIP docs can't
   leak onto the site.
3. **Rebuilds without docs pushes** — upstream-only changes don't trigger our CI. Fix: a
   **Woodpecker nightly cron** on `main`. The pipeline already accepts `event: cron`; the cron
   itself is created once in the Woodpecker UI (ci.codeberg.org → repo → Settings → Crons, e.g.
   `nightly` @ `0 4 * * *` on branch `main`) — **one-time manual step for Lars** (needs repo-admin,
   which the CI token doesn't have). Until then, any push or manual run refreshes.

---

## 13. Phasing

**Phase 0 — Enablers (do first)** — ✅ **complete 2026-07-10**
- [x] WS-S: Codeberg `TAPPaaS` org; `Documentation` on Codeberg; Woodpecker CI + git-pages for
  staging (live at staging.tappaas.org) + `spikes/<branch>/` previews (GitHub keeps publishing 1.x).
- [x] WS0 source-sync pipeline (skeleton; fetches TAPPaaS cross-forge from GitHub — pinned to
  `main` until 2.0 reaches `stable`, see §12.1).
- [x] WS1 framework spikes (A vs B) and decision (**Option B**, §5.5) — built on the pipeline.
- [x] Import presentation assets from Nextcloud into `docs/assets/marketing/` (unblocks WS2).

**Phase 1 — Public face**
- [x] WS2 messaging + front page + Examples *(2026-07-10: Astro landing graduated to staging root;
  Why-TAPPaaS storyline page + Examples gallery live; generic-PaaS copy retired. Open: diagram
  redraw deferred; named-adopter sign-off not yet needed).*
- [x] WS3 installation macro-stages + hardware personas (consuming WS0) *(2026-07-10: 7-stage
  install overview + two-axis hardware page live; open: automated vllm-number sync, satellite
  module sync once it ships upstream).*
- [x] WS6 stable-vs-main page *(2026-07-10: `installation/versions.md`; remaining WS6 items are
  cutover-time actions, §10.2).*

**Phase 2 — Reference depth** — ✅ **content complete 2026-07-10**
- [x] WS4 Operate/Develop split + source-doc sync + ADR-007 architecture spine + author-a-module
  guide *(open: more `src/**` READMEs can join the allow-list as upstream matures).*
- [x] WS5 roadmap rewamp *(dateless; optional CI milestone-render skipped — rate-limit flakiness).*

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
| 0.2 | 2026-07-10 | Lars review + build | Phases 0–2 built. Review corrections: (a) framework **convergence** — landing becomes the Material home page, Astro layer retired, single-line header (§5.5); (b) content re-pinned to **`ADR007`** — Operate rebuilt on the manager/controller paradigm, script pages deleted, glob-sync + literate-nav + nightly-cron freshness model (§8, §12.1–12.2) |
