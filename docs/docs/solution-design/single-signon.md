---
title: Single Sign-On
description: TAPPaaS identity and authentication design
---

# Single Sign-On Design

## Overview

Single Sign-On (SSO) enables users to access multiple applications with one set of credentials, improving user experience while centralizing security management and simplifying administration.

---

## Open Source SSO Solutions

Seven major platforms compete in this space:

| Solution | Key Features |
|----------|-------------|
| **Keycloak** | Most popular and widely adopted; supports OIDC, SAML, OAuth2, LDAP, social logins and enterprise features |
| **Authentik** | Modern interface with OIDC, SAML, LDAP support; gaining popularity for flexibility |
| **Authelia** | Lightweight authentication portal focusing on MFA and access policies |
| **Gluu** | Enterprise-ready with strong federation capabilities but more complex setup |
| **Zitadel** | Cloud-native, developer-friendly, modern approach to SSO |
| **IdentityServer** | Popular in .NET environments for API and microservices |
| **CAS (Apereo CAS)** | Mature platform with strength in academic and enterprise sectors |

---

## Why Authentik

TAPPaaS uses **Authentik** as the preferred SSO solution due to its:

- Modern, user-friendly interface
- Comprehensive protocol support (OIDC, SAML, LDAP)
- Flexibility and ease of configuration
- Active development and growing community
- Lightweight resource requirements suitable for self-hosted environments

---

## Bitwarden/VaultWarden Integration

Bitwarden functions as a secure password manager that integrates with the SSO solution, allowing centralized authentication while maintaining a secure vault for credentials that cannot yet leverage SSO.

---

## Combined Strategy

Using both platforms creates a complete identity solution:

- **Authentik** manages modern SSO access across compatible applications
- **VaultWarden** securely stores credentials for legacy systems and external services lacking SSO support
