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

```mermaid
flowchart LR
    subgraph Repos[" "]
        direction TB
        subgraph TAPPaaS[TAPPaaS Repository]
            stable[stable]
            unstable[unstable]
        end
        subgraph Community[Community Repository]
            comm_main[main]
        end
    end

    subgraph Instance[TAPPaaS Instance]
        local[tappaas-cicd/TAPPaaS]
        comm_local[tappaas-cicd/Community]
    end

    stable --> local
    comm_main --> comm_local
```

*To be documented.*

---

## Downstream Repositories

```mermaid
flowchart LR
    subgraph Repos[" "]
        direction TB
        subgraph TAPPaaS[TAPPaaS Repository]
            stable[stable]
            unstable[unstable]
        end
        subgraph Community[Community Repository]
            comm_main[main]
        end
        subgraph Downstream[Downstream Repository]
            down_main[main]
        end
    end

    subgraph Instance[TAPPaaS Instance]
        local[tappaas-cicd/TAPPaaS]
        comm_local[tappaas-cicd/Community]
        down_local[tappaas-cicd/Downstream]
    end

    stable --> local
    comm_main --> comm_local
    down_main --> down_local
```

*To be documented.*

---

## Private Repositories

*To be documented.*


