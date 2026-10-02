---
title: Roadmap
description: >
  What TAPPaaS is building now, what comes next, what has landed, and in which version.
---

# Roadmap

What we are building now, what comes next, and what has already landed.

**The current plan is security and stability.** It is built in waves: first make upgrades
safe, then make the breaking changes while few sites depend on today's shapes, then harden the
network, then stability, then new capabilities. **Now** is being built, **Soon** is planned, and
a date means it is built and running on the unstable channel. Every two weeks the next version
is cut for staging and reaches production two weeks later; the version on a landed item is the
one that carries it.

<div class="tap-roadmap">

<div class="tap-rm tap-rm--now">
  <div class="tap-rm__when">Now</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">One NixOS baseline</p>
    <p>Every app VM builds on the same hardened base configuration, instead of each module carrying its own copy.</p>
    <span class="tap-rm__tag">wave 1</span>
  </div>
</div>

<div class="tap-rm tap-rm--now">
  <div class="tap-rm__when">Now</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Module blueprint check</p>
    <p>A check that every module ships what it should, and apps grouped by stack in the repository.</p>
    <span class="tap-rm__tag">wave 1</span>
  </div>
</div>

<div class="tap-rm tap-rm--now">
  <div class="tap-rm__when">Now</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Recovery you have rehearsed</p>
    <p>Restores practised on the test system, and a documented, tested way to rebuild a firewall or a node.</p>
    <span class="tap-rm__tag">wave 1</span>
  </div>
</div>

<div class="tap-rm tap-rm--now">
  <div class="tap-rm__when">Now</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">VM lifecycle &amp; capacity</p>
    <p>Memory and disk defaults based on measurement, drift detection, clean shutdowns and a sensible boot order.</p>
    <span class="tap-rm__tag">wave 3</span>
  </div>
</div>

<div class="tap-rm tap-rm--now">
  <div class="tap-rm__when">Now</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">App module fixes</p>
    <p>Home Assistant, Nextcloud Talk, LiteLLM and friends: the known rough edges fixed, and tested so they stay fixed.</p>
    <span class="tap-rm__tag">wave 3</span>
  </div>
</div>

<div class="tap-rm tap-rm--soon">
  <div class="tap-rm__when">Soon</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Secrets &amp; privileged access</p>
    <p>One interface for secrets — simple first, OpenBao behind it later — and Proxmox hardened to its guide.</p>
    <span class="tap-rm__tag">wave 1</span>
  </div>
</div>

<div class="tap-rm tap-rm--soon">
  <div class="tap-rm__when">Soon</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Firewall hardening</p>
    <p>Tighter defaults: the admin GUI only from management, anti-spoofing always on, no zone-wide gateway rule — each change shown as a dry-run diff before it applies.</p>
    <span class="tap-rm__tag">wave 2</span>
  </div>
</div>

<div class="tap-rm tap-rm--soon">
  <div class="tap-rm__when">Soon</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Sturdier DNS</p>
    <p>DNSSEC, a clear IPv6 stance, public DNS that follows a dynamic WAN address, and optional blocklists.</p>
    <span class="tap-rm__tag">wave 2</span>
  </div>
</div>

<div class="tap-rm tap-rm--soon">
  <div class="tap-rm__when">Soon</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Single sign-on, everywhere</p>
    <p>Every app wired to the identity provider the same way, with a login page that shows your site.</p>
    <span class="tap-rm__tag">wave 3</span>
  </div>
</div>

<div class="tap-rm tap-rm--soon">
  <div class="tap-rm__when">Soon</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Production-grade AI stack</p>
    <p>LiteLLM and Open WebUI tested, sized to their defaults, and kept current.</p>
    <span class="tap-rm__tag">wave 3</span>
  </div>
</div>

<div class="tap-rm tap-rm--soon">
  <div class="tap-rm__when">Soon</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Easier first install</p>
    <p>An installer that can resume, shows its progress, and only asks what applies to your hardware.</p>
    <span class="tap-rm__tag">wave 3</span>
  </div>
</div>

<div class="tap-rm tap-rm--soon">
  <div class="tap-rm__when">Soon</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Alerting</p>
    <p>Be told when a node drops out or the cluster loses quorum, with a second cluster link for resilience.</p>
    <span class="tap-rm__tag">wave 4</span>
  </div>
</div>

<div class="tap-rm tap-rm--soon">
  <div class="tap-rm__when">Soon</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Finer-grained publishing</p>
    <p>Publish only some paths of an app, or only to some zones or source addresses.</p>
    <span class="tap-rm__tag">wave 4</span>
  </div>
</div>

<div class="tap-rm tap-rm--soon">
  <div class="tap-rm__when">Soon</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Storage &amp; devices</p>
    <p>Network storage for the cluster (NFS first), and modules for physical devices on your network.</p>
    <span class="tap-rm__tag">wave 4</span>
  </div>
</div>

<div class="tap-rm tap-rm--done">
  <div class="tap-rm__when">27 Sep 2026</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Security scan</p>
    <p>After every update, TAPPaaS lists what runs — machines, containers, nodes and firewall — as a CycloneDX SBOM, checks it against CVE databases, and tells the owner what needs a fix.</p>
    <span class="tap-rm__tag">2.2</span>
  </div>
</div>

<div class="tap-rm tap-rm--done">
  <div class="tap-rm__when">25 Sep 2026</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Nextcloud 35</p>
    <p>Nextcloud moves to version 35. The Talk stack for calls ships with it and is still being finished end to end (see App module fixes).</p>
    <span class="tap-rm__tag">2.2</span>
  </div>
</div>

<div class="tap-rm tap-rm--done">
  <div class="tap-rm__when">25 Sep 2026</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">NixOS 26.05</p>
    <p>The whole estate moves to NixOS 26.05. A release move is staged for the next boot, never half-applied to a running machine.</p>
    <span class="tap-rm__tag">2.1</span>
  </div>
</div>

<div class="tap-rm tap-rm--done">
  <div class="tap-rm__when">23 Sep 2026</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Release channels</p>
    <p>Unstable, staging and production: a site takes a change only after it has run on the channel before it.</p>
    <span class="tap-rm__tag">2.1</span>
  </div>
</div>

<div class="tap-rm tap-rm--done">
  <div class="tap-rm__when">22 Sep 2026</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">A control plane that checks itself</p>
    <p>The management VM checks itself after every update, and rolls back when the check fails.</p>
    <span class="tap-rm__tag">2.1</span>
  </div>
</div>

<div class="tap-rm tap-rm--done">
  <div class="tap-rm__when">21 Sep 2026</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Site-wide settings</p>
    <p>Time zone, keyboard, location and time source set once for the site, and applied to every machine.</p>
    <span class="tap-rm__tag">2.1 · wave 1</span>
  </div>
</div>

<div class="tap-rm tap-rm--done">
  <div class="tap-rm__when">20 Sep 2026</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">One module contract</p>
    <p>Every module has the same shape, and its version and status claims mean something.</p>
    <span class="tap-rm__tag">2.1 · wave 1</span>
  </div>
</div>

<div class="tap-rm tap-rm--done">
  <div class="tap-rm__when">19 Sep 2026</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Backups where you want them</p>
    <p>You choose where backups go, hosts get file-level backups, and existing Debian machines can be brought under management.</p>
    <span class="tap-rm__tag">2.1 · wave 1</span>
  </div>
</div>

<div class="tap-rm tap-rm--done">
  <div class="tap-rm__when">16 Sep 2026</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Safe upgrades</p>
    <p>Versioned config migrations with a backup and a dry run, and a failed install that cleans up after itself.</p>
    <span class="tap-rm__tag">2.1 · wave 0</span>
  </div>
</div>

<div class="tap-rm tap-rm--done">
  <div class="tap-rm__when">15 Sep 2026</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">Updates you can trust</p>
    <p>Honest pre-update checks, an update window you schedule, and an email to the owner when an update fails.</p>
    <span class="tap-rm__tag">2.1 · wave 0</span>
  </div>
</div>

<div class="tap-rm tap-rm--release">
  <div class="tap-rm__when">21 Jul 2026</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">TAPPaaS 2.0</p>
    <p>One model for people, apps, environments and health, a new website, and a migration path from 1.x.</p>
    <a class="tap-rm__tag" href="https://codeberg.org/TAPPaaS/TAPPaaS/releases/tag/v2.0">v2.0</a>
  </div>
</div>

<div class="tap-rm tap-rm--release">
  <div class="tap-rm__when">13 Apr 2026</div>
  <div class="tap-rm__card">
    <p class="tap-rm__title">TAPPaaS 1.0</p>
    <p>The first release: automated installation for a home or a small business, running on real systems.</p>
    <a class="tap-rm__tag" href="https://codeberg.org/TAPPaaS/TAPPaaS/releases/tag/v1.0.0">v1.0.0</a>
  </div>
</div>

</div>

## How we plan

- **The order comes from one plan.** The
  [security & stability plan](https://codeberg.org/TAPPaaS/TAPPaaS/src/branch/main/docs/design/security-and-stability-plan.md)
  groups every open issue into the waves above and says why they come in that order.
- **Which version carries what** is in
  [RELEASES.md](https://codeberg.org/TAPPaaS/TAPPaaS/src/branch/main/RELEASES.md): every version,
  and the day it reached staging and production.
- **Decisions are written down first**, as
  [ADRs in the source repository](https://codeberg.org/TAPPaaS/TAPPaaS/src/branch/main/docs/ADR).
- **The details live on Codeberg**: [milestones](https://codeberg.org/TAPPaaS/TAPPaaS/milestones)
  and [issues](https://codeberg.org/TAPPaaS/TAPPaaS/issues). To influence the direction, see
  [Contributing](../community/contributing.md).
