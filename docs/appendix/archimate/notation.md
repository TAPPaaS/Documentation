---
title: ArchiMate Notation
description: Reference guide for creating ArchiMate diagrams
---

# ArchiMate Notation

This page provides a reference guide for creating ArchiMate diagrams in the TAPPaaS documentation.

## Diagram Rendering

The diagrams are created using [PlantUML with ArchiMate support](https://github.com/plantuml-stdlib/Archimate-PlantUML) and rendered via the Kroki service.

## Creating New Diagrams

To add new ArchiMate diagrams:

1. Use PlantUML syntax with the ArchiMate include
2. Wrap the diagram in a `kroki-plantuml` code fence
3. Reference the ArchiMate library from the PlantUML stdlib

### Basic Example

```markdown
```kroki-plantuml
@startuml
title My Diagram

package "Layer" {
  [Component A] as a
  [Component B] as b
}

a --> b : relationship

@enduml
```                (close fence here)
```

## ArchiMate Elements Reference

All ArchiMate diagrams must include the ArchiMate library:

```plantuml
!include <archimate/Archimate>
```

### Strategy Layer Elements

| Element | Syntax | Description |
|---------|--------|-------------|
| Capability | `Strategy_Capability(id, "Name")` | An ability that an organization possesses |
| Resource | `Strategy_Resource(id, "Name")` | An asset owned or controlled |
| Course of Action | `Strategy_CourseOfAction(id, "Name")` | An approach to achieve goals |

### Business Layer Elements

| Element | Syntax | Description |
|---------|--------|-------------|
| Actor | `Business_Actor(id, "Name")` | A person or organization |
| Role | `Business_Role(id, "Name")` | Responsibility for behavior |
| Process | `Business_Process(id, "Name")` | A sequence of activities |
| Service | `Business_Service(id, "Name")` | Externally visible functionality |
| Object | `Business_Object(id, "Name")` | A business concept or entity |

### Application Layer Elements

| Element | Syntax | Description |
|---------|--------|-------------|
| Component | `Application_Component(id, "Name")` | Encapsulated application functionality |
| Service | `Application_Service(id, "Name")` | Service exposed by components |
| Function | `Application_Function(id, "Name")` | Internal behavior of a component |
| Data Object | `Application_DataObject(id, "Name")` | Data structured for processing |

### Technology Layer Elements

| Element | Syntax | Description |
|---------|--------|-------------|
| Node | `Technology_Node(id, "Name")` | Computational resource (VM, server) |
| Device | `Technology_Device(id, "Name")` | Physical hardware |
| System Software | `Technology_SystemSoftware(id, "Name")` | Software platform (OS, middleware) |
| Artifact | `Technology_Artifact(id, "Name")` | Physical data (file, script) |
| Service | `Technology_Service(id, "Name")` | Infrastructure service |

## ArchiMate Relationships Reference

All relationships follow the pattern: `Rel_Type(from, to)` or `Rel_Type(from, to, "label")`

### Structural Relationships

| Relationship | Syntax | Description |
|-------------|--------|-------------|
| Composition | `Rel_Composition(parent, child)` | Part is integral to whole |
| Aggregation | `Rel_Aggregation(parent, child)` | Part groups into whole |
| Assignment | `Rel_Assignment(from, to)` | Allocation of responsibility |
| Realization | `Rel_Realization(from, to)` | Implementation of abstraction |

### Dependency Relationships

| Relationship | Syntax | Description |
|-------------|--------|-------------|
| Serving | `Rel_Serving(provider, consumer)` | Provider supports consumer |
| Access | `Rel_Access(from, to, "label")` | Ability to perform on data |
| Association | `Rel_Association(from, to)` | Unspecified relationship |

### Dynamic Relationships

| Relationship | Syntax | Description |
|-------------|--------|-------------|
| Triggering | `Rel_Triggering(from, to)` | Temporal/causal dependency |
| Flow | `Rel_Flow(from, to, "label")` | Transfer of objects |

### Directional Variants

Relationships can include direction for layout control:

- `Rel_Serving_Up(from, to)` - Arrow points up
- `Rel_Serving_Down(from, to)` - Arrow points down
- `Rel_Serving_Left(from, to)` - Arrow points left
- `Rel_Serving_Right(from, to)` - Arrow points right

## Example Diagram

```plantuml
!include <archimate/Archimate>

title Example: Application realizes Capability

Strategy_Capability(cap, "Chat Interface")
Application_Component(app, "OpenWebUI")
Application_Service(svc, "Chat Service")
Technology_Node(vm, "NixOS VM")

Rel_Realization(app, cap)
Rel_Realization(app, svc)
Rel_Assignment(vm, app)
```

## Resources

For complete documentation, see:

- [Archimate-PlantUML reference](https://github.com/plantuml-stdlib/Archimate-PlantUML)
- [PlantUML documentation](https://plantuml.com/)
- [ArchiMate specification](https://pubs.opengroup.org/architecture/archimate3-doc/)
