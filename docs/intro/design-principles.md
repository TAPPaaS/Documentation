---
title: Design Principles
description: >
  The seven principles TAPPaaS is built on — risk first, then cost, then
  capability — and the honest boundary of what TAPPaaS is not.
---

# Design Principles

Seven principles guide every TAPPaaS decision — which software gets curated in, how
modules must behave, what ships enabled and what stays off. They are ordered the way
our users evaluate platforms: **risk first, then cost, then capability**. They also
serve as the evaluation filter for new [modules](../architecture/author-a-module.md).

## 1. Digital sovereignty — you stay in control

Your data, your infrastructure, your rules. TAPPaaS runs fully local, across a
cluster, or hybrid alongside cloud services. No dependency on external vendors: you
decide where your data lives and who can access it.
*Directly relevant for government, healthcare, and SMBs subject to GDPR / NIS2 —
see [Digital Sovereignty](digital-sovereignty.md).*

## 2. Security by design — zero trust

Security is not a configuration step; it is the foundation. Every component follows
zero-trust principles: **access is denied by default, everything must be explicitly
granted**. Designed to align with NIS2 and modern cybersecurity standards — without
requiring a security specialist to operate.

## 3. Locked down and safe by default

Exposing a service to the network requires an active, deliberate decision. The safe
choice is always the default — protecting admins and users from accidental
misconfiguration, one of the leading causes of security incidents in self-hosted
environments. *Most platforms expose everything by default; TAPPaaS does the
opposite.*

## 4. Open source — no vendor lock-in

Fully open source (MPL 2.0). No subscriptions, no per-seat pricing, no egress fees,
no cloud-provider dependency. You can inspect, audit, fork, or migrate at any time —
and it meets open-standard requirements for public-sector procurement.

## 5. Predictable cost — hardware versatility

Runs on commodity x86 hardware: new, old, or mixed. Existing machines can be
repurposed instead of replaced, extending asset lifecycles and reducing capital
expenditure. Combined with zero subscription cost, this points to a significantly
lower total cost of ownership than cloud or traditional enterprise platforms.
*Honest nuance: older hardware draws more power — the net benefit depends on
hardware age and workload.*

## 6. One platform — lower operational overhead

One platform covers deployment, updates, identity and access, monitoring, backup and
lifecycle — no stitching together ten separate tools. Configuration is **declarative
JSON**, consistent across every module.

## 7. Enterprise-grade stability, without enterprise complexity

Built on mature, actively maintained open-source components. Works offline.
Accessible from mobile. Scales from a single node to a multi-node HA cluster —
enterprise reliability without an enterprise budget or a platform-engineering team.

---

## What TAPPaaS is *not*

TAPPaaS is not a general-purpose PaaS for large engineering teams. It is
purpose-built for **prosumers, SOHO, SMBs, and local or regional government IT** —
organisations that need modern cloud capabilities without cloud dependency or cloud
complexity. If you run a hundred-developer product organisation, you want a
different tool.

---

*These principles are the yardstick for [module decisions](../architecture/author-a-module.md)
and roadmap trade-offs. Where the story came from: [Why TAPPaaS](index.md).*
