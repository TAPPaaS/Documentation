---
title: Develop a Module
description: >
  Port your application to TAPPaaS — from copying the 00-Template to a module
  that installs, updates, backs up and health-checks itself.
---

# Develop a Module

You have an application; you want it running on TAPPaaS. What you build is a **module**:
your app plus a small json contract and a few lifecycle scripts, running in its own VM.
In return the platform gives you — without further work — VM provisioning, network zones
and firewall rules, a public URL behind the reverse proxy, scheduled updates, backup,
and health monitoring.

This page is the path, in order. The depth lives one click away at each step.

## 1. Before you start

- **A TAPPaaS to develop against.** Ideally a test instance; a sufficiently stand-alone
  module can be developed on a production system — its own VM and, if you want, a
  dedicated zone keep experiments away from production. See
  [Git & Repository Topology](../generated/design/cicd-git.md) for the dev-instance setup.
- **Decide where your module will be maintained** — the open-source TAPPaaS repo (via
  pull request), a community repository, or a private one. This shapes your git workflow:
  [Git & Repository Topology](../generated/design/cicd-git.md).
- **Know how your app ships.** The default module VM is **NixOS** (configured
  declaratively in a `.nix` file); Debian cloud-images, ISO installs and even Windows
  are supported when your app needs them.

## 2. Quick start — template to running VM

Work on the CICD mothership (`tappaas-cicd`), in its checkout of the source repo:

```bash
cd ~/TAPPaaS/src/apps
cp -r 00-Template myapp && cd myapp
mv README-template.md README.md
mv template.json myapp.json        # + template.nix -> myapp.nix, or delete it
```

Edit `myapp.json` — at minimum a free `vmid`, sizing (`cores`, `memory`, `diskSize`)
and the zone (`zone0`, typically `srv`). Then:

```bash
module-manager module add myapp
```

The platform creates the VM, wires its network, and runs your `install.sh`. The
[Module Template](../generated/module-template.md) walks every file you just copied.

## 3. Make it run your application

- **`install.sh`** — called once with the module name; puts your software in the VM.
  For NixOS modules the default `install.sh` rebuilds the VM from `myapp.nix` — porting
  your app is mostly writing that nix configuration.
- **`update.sh`** — called on the platform's update schedule; keeps the app patched
  without operator attention.
- **`test.sh`** — your regression check, run via `module-manager module test myapp`;
  the same tests gate updates.

## 4. The module contract

The json file is the whole interface between your module and the platform:

- **Every field, defined once:** [Schemas](../generated/schemas.md) — sizing, image
  selection (`imageType`/`image`/`os`), networking, HA.
- **Dependencies:** declare `dependsOn` (e.g. `cluster:vm`, `network:proxy`) and the
  platform provisions them in order — your module can also **provide** services others
  depend on: [Module Template → Providing a service](../generated/module-template.md).
- **A public URL:** depend on `network:proxy` and set `proxyPort` — Caddy publishes
  `myapp.<your-domain>` with TLS.
- **Where it runs:** modules live in zones inside Environments —
  [Network Zones](../generated/zones.md).
- **Backup:** data-bearing modules opt in with `backup:vm`; foundation-reproducible
  ones deliberately don't — [Backup design](../generated/design/backup.md).

## 5. Iterate and debug

```bash
module-manager module test myapp        # run your test.sh
module-manager module reconcile myapp   # re-apply the current config to the VM
module-manager module modify myapp      # release update: snapshot + test + merge
module-manager module delete myapp      # --archive by default
```

Can't SSH in? The [Module Template](../generated/module-template.md) shows how to take
a VM console screenshot through Proxmox — works on any OS, including mid-install.

## 6. How installation actually works *(optional reading)*

You don't need this to ship a module — read it when you're curious what the automation
does with your json:

- [CICD Mothership](../generated/design/cicd-mothership.md) — the control plane:
  managers decide, controllers do (What → Design).
- [Module Manager](../generated/managers/module-manager.md) — the full verb and script
  reference (Operate).
- [Module Dependencies](../generated/module-dependencies.md) — the dependency graph the
  install order is derived from.
- [Meta Model](../what/meta-model.md) — how deployable units compose (ADR-009).

## 7. Ship it

A finished module is a **good platform citizen**: it updates unattended, its tests pass,
its data is backed up, it reports into health, and it carries its own `README.md` (what
it is) and `INSTALL.md` (what automation can't do for you).

Then contribute it — via pull request to the
[TAPPaaS source repo](https://codeberg.org/TAPPaaS/TAPPaaS), a community repository, or
keep it private ([where modules live](../generated/design/cicd-git.md)). Good first
step: open an issue describing the app — someone may already be packaging it. See the
[contribution guide](../community/contributing.md).
