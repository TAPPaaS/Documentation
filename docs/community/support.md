---
title: Support
description: Get help with TAPPaaS - documentation, community support, and issue reporting
---

# Getting Support

Need help with TAPPaaS? Here's how to find answers and get assistance.

---

## Before You Ask

Many questions are already answered in our documentation:

1. **Search the Docs** - Use the search bar at the top of any page
2. **Check the FAQ** - Common questions are answered in our [FAQ](faq.md)
3. **Read Tutorials** - Step-by-step guides for common tasks in [Tutorials](../install/index.md)
4. **Review FAQ** - Common issues and solutions in [FAQ](faq.md)

---

## Community Support

### Codeberg Issues

The best place to ask questions and get help from the community.

[:octicons-comment-discussion-24: Ask a Question](https://codeberg.org/TAPPaaS/TAPPaaS/issues/new){ .md-button .md-button--primary }

**Tips for getting help:**

- Search existing issues first
- Use a clear, descriptive title
- Include relevant details (version, environment, error messages)
- Share what you've already tried
- Format code and logs properly

### Labelling your issue

When you open an issue, add a label so maintainers can triage it:

| Label | Use For |
|-------|---------|
| **question** | Technical questions about using TAPPaaS |
| **enhancement** | Feature suggestions and enhancement ideas |
| **bug** | Something isn't working as documented |

---

## Reporting Issues

Found a bug? Please report it on Codeberg Issues.

[:octicons-issue-opened-24: Report a Bug](https://codeberg.org/TAPPaaS/TAPPaaS/issues/new){ .md-button }

### What to Include

!!! info "Bug Report Checklist"
    - [ ] TAPPaaS version (`tappaas version`)
    - [ ] Steps to reproduce the issue
    - [ ] Expected vs actual behavior
    - [ ] Error messages and logs
    - [ ] Environment details (cloud provider, OS, etc.)

### Support bundles from your site

When something goes wrong — a failed update, a lost cluster quorum, a host gone silent —
your TAPPaaS site mails you an alert, and for the problems a maintainer could look into it
attaches a **support bundle**: the logs of the event, the state of the site and its
configuration, with names, e-mail and street addresses, public IP addresses and secrets
replaced. Domains, private addresses and module names are kept: they are what we debug
with. `manifest.json` inside lists what is there and what was replaced, and the table to
decode the replacements stays on your site, in `/var/lib/tappaas/support/`.

Nothing is sent to us by itself — you decide. The bundle still shows your domains and how
your network is built, so **do not attach it to a public issue**: open the issue with a
description, and say that you have a bundle.

The alert says to forward the mail to your site's support address. That address is empty
after an install; set it, as a day-two step, when you have a support contact:

```bash
site-manager site modify --set supportEmail=<address>
```

TAPPaaS support plans, with the address to use, are still to come; this page will name
it then.

To see what a bundle looks like, and that alert mails reach you at all, run
`tappaas-support-bundle.sh --test` on the mothership: it sends a test alert with a bundle,
then its all-clear.

---

## Feature Requests

Have an idea for improving TAPPaaS?

[:octicons-light-bulb-24: Request a Feature](https://codeberg.org/TAPPaaS/TAPPaaS/issues/new){ .md-button }

Before submitting:

- Search existing issues to avoid duplicates
- Check the [About page](../about/index.md) for project information
- Describe the problem you're trying to solve
- Explain why this would benefit other users

---

## Security Issues

!!! warning "Security Vulnerabilities"
    **Do not** report security vulnerabilities through public issues.

    Please email security concerns to the maintainers for responsible disclosure.

---

## Response Times

TAPPaaS is a community-driven open source project. Response times vary based on:

- Complexity of the issue
- Availability of maintainers
- Clarity of the report

**Typical response times:**

| Type | Response |
|------|----------|
| Security issues | Within 48 hours |
| Critical bugs | Within 1 week |
| General issues | Best effort |
| Feature requests | Varies |

---

## How to Help Others

Want to give back? Help answer questions in Codeberg Issues!

- Share your knowledge and experience
- Provide working examples and solutions
- Be patient and welcoming to newcomers
- Follow our [Code of Conduct](code-of-conduct.md)

---

## Related Resources

- [Contributing Guide](contributing.md) - How to contribute to TAPPaaS
- [FAQ](faq.md) - Frequently asked questions and common solutions
