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

Essentially when developing modules you want a test TAPPaaS Instance in parallel with your production instance. If the module you are developing is sufficiently separate from other modules then you can do module development on a production system. More on that below

What you want is a setup like the one below. The actual running instance of TAPPaaS can be achieved in any of the above scenarios but hte essen is to have a private branch, likely on a private git system that will be upstream from the development instance of TAPPaaS

```mermaid
flowchart RL
    subgraph Development[Development Repository]
        dev_unstable[unstable]
    end
    subgraph Upstream[Upstream Repository]
        up_stable[stable]
        up_unstable[unstable]
    end

    subgraph Instances[" "]
        direction TB
        subgraph InstanceDev[TAPPaaS Instance Dev]
            localDev[tappaas-cicd/Upstream]
            localDev_dev[tappaas-cicd/Development]
        end
        subgraph InstanceProd[TAPPaaS Instance Prod]
            localProd[tappaas-cicd/Upstream]
        end
    end

    localProd -->|pull| up_stable
    localDev -->|pull| up_unstable
    localDev_dev -->|pull| dev_unstable
    dev_unstable --> |PR| up_unstable
```

The module in the development REPO will be tested on the development system and when considered ok it can be submitted to the upstream repository through a Pull request (PR). UPstream can be the the TAPPaaS proper, the TAPPaaS Community repositories, or it can be keep as a private repository

If the module being developed is sufficiently stand alone then it can be developed on a production system. TAPPaaS allows many kinds of isolation to ensure errors on development is not affecting production. The two most important parts of separation are:

- A module will as default get its own VM with a well defined resource envelope
- a module can also be deployed in a separate zone: a developer can enable a dedicated zone in parallel to "srv" so not traffic of the development module will interfere with production

A question that would be natural to ask: Can the Development repository be hosted on TAPPaaS: certanly. it would require that a Git system is installed. TAPPaaS decided to implement Forgejo (the software behind CodeBerg) as part of the DevOps stack (not available yet)

---

## Developing applications to be deployed on TAPPaaS

Developing TAPPaaS modules is about developing the deployment automation for an application. If you are interested in developing an actual application and yes TAPPaaS as either a Continuous Integration system or as a Continuous Deployment solution for the development activities, then that is certainly possible

The intent is to provide a stack of modules/application that delivers a full devops pipeline. The CD aspect of the pipeline will be the system above, but the CI part will have main ForgeJo, pipeline systems, and binary repositories. The outcome of the CI can be pulled by the CD above

