---
title: Productivity Stack
description: Files, collaboration, office, passwords and call relay.
---

# Productivity Stack

| Module | Role |
|--------|------|
| [Nextcloud](../../generated/modules/nextcloud.md) | Files, calendars, contacts, Talk |
| [Nextcloud HPB](../../generated/modules/nextcloud-hpb.md) | High-performance backend for Talk and push |
| [EURO Office](../../generated/modules/euro-office.md) | Web office suite inside Nextcloud |
| [Vaultwarden](../../generated/modules/vaultwarden.md) | Bitwarden-compatible password manager |
| [Coturn](../../generated/modules/coturn.md) | TURN relay for reliable calls |
| [n8n](../../generated/modules/n8n.md) | Workflow automation *(planned — placeholder module)* |

Install guides live under [Install → Add Stacks](../../installation/productivity-stack/index.md).

## Architecture view

```kroki-plantuml
@startuml
!include <archimate/Archimate>

title TAPPaaS Productivity Stack

' Business Actor
Business_Actor(user, "Platform User")

' Application Components
Application_Component(nextcloud, "Nextcloud")
Application_Component(n8n, "n8n")
Application_Component(vault, "Vaultwarden")

' Application Services
Application_Service(fileSvc, "File Storage")
Application_Service(workflowSvc, "Workflow Automation")
Application_Service(secretSvc, "Secret Management")

' Technology Artifacts (Data)
Technology_Artifact(files, "Files")
Technology_Artifact(db, "Database")

' Components realize services
Rel_Realization(nextcloud, fileSvc)
Rel_Realization(n8n, workflowSvc)
Rel_Realization(vault, secretSvc)

' User uses services
Rel_Serving(fileSvc, user)
Rel_Serving(workflowSvc, user)
Rel_Serving(secretSvc, user)

' Data access
Rel_Access(nextcloud, files)
Rel_Access(nextcloud, db)
Rel_Access(n8n, db)

@enduml
```
