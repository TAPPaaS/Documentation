---
title: Approach
description: How TAPPaaS assembles open source components into an integrated platform
---

# Our Approach

TAPPaaS is an open-source initiative that assembles existing FOSS components into an integrated platform rather than building from scratch. Most of the vision can be realized using existing open source software - our job is to curate, integrate, and automate.

---

## Core Design Principles

The project adheres to several key guidelines:

### 1. Free and Open Source Software

All components must be Free and Open Source Software. No proprietary dependencies, no vendor lock-in.

### 2. Deliberately Limited Options

We limit options to reduce barriers for new users. Rather than offering every possible choice, we make opinionated decisions that work well together.

### 3. Mature, Actively Maintained Software

We prioritize software that has proven itself in production environments and has an active community maintaining it.

### 4. Seamless Integration and Automation

Every module must integrate seamlessly with the others. Automation is built-in from the start, not bolted on afterward.

### 5. Distinct User Experiences

We create distinct experiences for different roles:

- **Developers** - Building and extending the platform
- **Installers** - Deploying TAPPaaS for users
- **Maintainers** - Keeping systems running day-to-day
- **End Users** - Using the services without worrying about infrastructure

### 6. Mobile Accessibility

The platform must be accessible from mobile devices. Modern users expect to manage their digital lives from anywhere.

### 7. Offline Functionality

Systems must work even when internet connectivity is limited or unavailable. Local resilience is a core requirement.

---

## Development Roadmap

The team follows a phased approach:

### Spring 2025

- Framework establishment
- CI/CD pipeline creation
- Core architecture decisions

### Summer 2025

- Minimum viable product
- Manual installation process
- Focus on home use cases

### Fall 2025

- Automation of installation
- Expansion of home-use capabilities
- Documentation and guides

### 2026 and Beyond

- Small business support
- Broader platform expansion
- Community growth

!!!info "Current Status"
    The project has advanced beyond the framing phase and is actively developing the MVP.

---

## Assembly Over Creation

Rather than reinventing the wheel, TAPPaaS focuses on:

| Activity | Description |
|----------|-------------|
| **Curation** | Selecting the best open source tools for each function |
| **Integration** | Configuring components to work together seamlessly |
| **Automation** | Scripting installation and maintenance tasks |
| **Documentation** | Making the platform accessible to non-experts |

This approach lets us move faster and build on the collective work of the open source community.

---

## License

TAPPaaS is licensed under the **Mozilla Public License 2.0** (MPL-2.0).

This license:

- Allows commercial use
- Requires sharing modifications to MPL-licensed files
- Permits combining with proprietary code
- Protects contributor patents

See the [License page](../about/license.md) for full details.

---

## Next Steps

- [Vision & Problem](vision.md) - Understand what problems we're solving
- [Architecture Overview](architecture.md) - See how the platform is structured
- [Installation Guide](../installation/index.md) - Get started with TAPPaaS
