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

Further if you are Developing modules for TAPPaaS or developing applications that are to be deployed as modules then there are further variations which is documented at the end

---

## Basic TAPPaaS GitOps

This is the basic setup that you will get if you follow the installation guide. The default upstream TAPPaaS repository is the Open Source REPO references on this documentation page top right corner. You can install the standard modules that comes from the TAPPaaS project.

you have to decide if you want to pull form the stable or unstable branch (the latter is really only for testing and staging)

```mermaid
flowchart RL
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
flowchart RL
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
flowchart RL
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
flowchart RL
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

## Developing TAPPaaS Modules

So you want to contribute to TAPPaaS. We are honoured, thank you.

Essentially when developing modules you want a test TAPPaaS Instance in parallel with your production instance. If the module you are developing is sufficiently seperate from other modules then you can do module development on a production system. More on that below

What you want is a setup like the one below. The actual running instance of TAPPaaS can be achieved in any of the above scenarios but hte essenst is to have a private branch, likely on a private git system that will be upstream from the development instance of TAPPaaS

```mermaid
flowchart RL
    subgraph Sources[" "]
        direction TB
        subgraph Upstream[Upstream Repository]
            up_stable[stable]
            up_unstable[unstable]
        end
        subgraph Development[Development Repository]
            dev_main[main]
        end
    end

    subgraph Instances[" "]
        direction TB
        subgraph InstanceProd[TAPPaaS Instance Prod]
            localProd[tappaas-cicd/Upstream]
        end
        subgraph InstanceDev[TAPPaaS Instance Dev]
            localDev[tappaas-cicd/Upstream]
            localDev_dev[tappaas-cicd/Development]
        end
    end

    localProd -->|pull| up_stable
    localDev -->|pull| up_unstable
    localDev_dev -->|pull| dev_main
```

---

## Developing applications to be deployed on TAPPaaS

