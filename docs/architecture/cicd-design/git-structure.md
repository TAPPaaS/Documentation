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

    local -->|pull| stable
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

    local -->|pull| stable
    comm_local -->|pull| comm_main
```

*To be documented.*

---

## Downstream Repositories

```mermaid
flowchart LR
    subgraph Sources[" "]
        direction TB
        subgraph TAPPaaS[TAPPaaS Repository]
            stable[stable]
            unstable[unstable]
        end
        subgraph Community[Community Repository]
            comm_main[main]
        end
    end

    subgraph Downstream[Downstream Repository]
        down_main[main]
    end

    subgraph Instances[" "]
        direction TB
        subgraph InstanceA[TAPPaaS Instance A]
            localA[tappaas-cicd/Downstream]
        end
        subgraph InstanceB[TAPPaaS Instance B]
            localB[tappaas-cicd/Downstream]
        end
    end

    down_main -->|pull| unstable
    down_main -->|pull| comm_main
    localA -->|pull| down_main
    localB -->|pull| down_main
```

*To be documented.*

---

## Private Repositories

```mermaid
flowchart LR
    subgraph Sources[" "]
        direction TB
        subgraph Downstream[Downstream Repository]
            down_main[main]
        end
        subgraph Private[Private Repository]
            priv_main[main]
        end
    end

    subgraph Instances[" "]
        direction TB
        subgraph InstanceA[TAPPaaS Instance A]
            localA[tappaas-cicd/Downstream]
        end
        subgraph InstanceB[TAPPaaS Instance B]
            localB[tappaas-cicd/Downstream]
            localB_priv[tappaas-cicd/Private]
        end
    end

    localA -->|pull| down_main
    localB -->|pull| down_main
    localB_priv -->|pull| priv_main
```

*To be documented.*


