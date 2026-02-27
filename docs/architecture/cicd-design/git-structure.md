---
title: Git Structure
description: TAPPaaS Git repository structure and organization
---

# Git Structure

This page documents the Git repository organization and GitOps workflow for TAPPaaS.

Fundamentally TAPPaaS uses a GitOps pull setup. on a regular schedule a TAPPaaS solution will pull the latest update from an upstream repository and then performs an update operation on the running TAPPaaS instance based on the new updated TAPPaaS configuration.

This is done by the "tappaas-cicd" module, which as a consequence will maintain a git clone of the TAPPaaS upstream repository

There are several ways this can be set up, but there are 4 basic patterns or use cases, which we are going through below
The actual setup for your TAPPaaS is configured in config/configuration.json on the tappaas user on the tappaas-cicd module
there is a command "repository.sh" that will change the configuration.

---

## Basic TAPPaaS GitOps

This is the basic setup that you will get if you follow the installation guide. The default upstream TAPPaaS repository is the Open Source REPO references on this documentation page top right corner. You can install the standard modules that comes from the TAPPaaS project.

you have to decide if you want to pull form the stable or unstable branch (the latter is really only for testing and staging)

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

---

## Community Repositories

The next step up is adding the Community Repository to the mix, this expands the actual modules you can install.

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

---

## Downstream Repositories

If you manage a set of TAPPaaS Instances you might want to "inject" a staging repository between the open source repositories and your installation. that way you can control what modules are available, and change default values to mach you deployment needs

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

---

## Private Repositories

Finally you can add you own private repositories to the mix.

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


