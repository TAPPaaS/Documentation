---
title: Git Structure
description: TAPPaaS Git repository structure and organization
---

# Git Structure

This page documents the Git repository organization and GitOps workflow for TAPPaaS.

---

## Basic TAPPaaS GitOps

```mermaid
flowchart LR
    subgraph TAPPaaS[TAPPaaS Repository]
        stable[stable]
        unstable[unstable]
    end

    subgraph Instance[TAPPaaS Instance]
        local[tappaas-cicd/TAPPaaS]
    end

    stable --> local
```

*To be documented.*

---

## Community Repositories

*To be documented.*

---

## Downstream Repositories

*To be documented.*

---

## Private Repositories

*To be documented.*


