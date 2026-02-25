---
title: Capabilities
description: TAPPaaS platform capabilities
---

# Capabilities

## Overview

TAPPaaS represents a comprehensive IT solution designed through both top-down analysis of user needs and bottom-up examination of practical implementations.

At a very high level the TAPPaaS solution delivers the following very high level of capabilities. We call it the **TAPPaaS Capability Stacks**

- Private Cloud Foundation Stack: The foundation upon which the other Stacks can function and integrate
- AI Stack: a set of capabilities aiming at providing private AI
- Productivity Stack: Classical capabilities such as file sharing, collaboration tooling, password management, ...
- Home Stack: Capabilities that a private individual or family needs, such as music and video streaming, picture store
- DevOps Stack: the capabilities needed in order to develop, test deploy software

More stacks are planned and not all of the above are implemented yet. TAPPaaS also allow any community or privately modules to be deployed

```mermaid
block-beta
    columns 4
    ai["AI Stack"]:1
    prod["Productivity Stack"]:1
    home["Home Stack"]:1
    devops["DevOps Stack"]:1
    foundation["Private Cloud Foundation Stack"]:4
```

---

## High-Level Structure

The system organizes around four interdependent domains:

```mermaid
classDiagram
    TAPPaaS *-- Security
    TAPPaaS *-- Services
    TAPPaaS *-- Management
    Security ..> Foundation
    Services ..> Foundation
    Management ..> Foundation
```

- **Security** - Protecting the platform and user data
- **Services** - The applications and functionality users interact with
- **Management** - Administration and maintenance capabilities
- **Foundation** - Essential infrastructure supporting all other components

Foundation provides the base infrastructure that Security and Services layers depend upon.

---

## Services

Services is what this is all about: Providing IT functions to the users of TAPPaaS. all the other parts like Foundation, Management and Security is just there to ensure that you can get the IT you need working in a stable, scalable, integrated, secure, private and maintainable way.

What services are essential to each deployment of TAPPaaS will differ, but we define a set of services that TAPPaaS should support based on the typical deployment. You can configure what is relevant for you deployment.

These examples of deployments are just examples, where we try and highlight the essential functionality that you need for that kind of deployment. 

```mermaid
classDiagram
  A Home ..> TAPPaaS
  Small Community ..> TAPPaaS
  Small Business Owner ..> TAPPaaS
  Small SW Development Organization ..> TAPPaaS
  Small Utility Company ..> TAPPaaS
  NGO ..> TAPPaaS
  
```

Note we are using the word "small" a lot. Make no mistake, TAPPaaS as a core architecture can scale up, but our initial design criteria is to cater for the SMB/Home out of the box.

