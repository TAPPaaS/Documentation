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

| Layer | Elements |
|-------|----------|
| **Business** | `Business_Actor`, `Business_Role`, `Business_Process`, `Business_Service`, `Business_Object` |
| **Application** | `Application_Component`, `Application_Service`, `Application_Function`, `Application_DataObject` |
| **Technology** | `Technology_Node`, `Technology_Device`, `Technology_SystemSoftware`, `Technology_Artifact`, `Technology_Path` |
| **Strategy** | `Strategy_Resource`, `Strategy_Capability`, `Strategy_Course_Of_Action` |

## ArchiMate Relationships Reference

| Relationship | Syntax |
|-------------|--------|
| Composition | `Rel_Composition(from, to, "label")` |
| Aggregation | `Rel_Aggregation(from, to, "label")` |
| Assignment | `Rel_Assignment(from, to, "label")` |
| Realization | `Rel_Realization(from, to, "label")` |
| Serving | `Rel_Serving(from, to, "label")` |
| Access | `Rel_Access(from, to, "label")` |
| Triggering | `Rel_Triggering(from, to, "label")` |
| Flow | `Rel_Flow(from, to, "label")` |
| Association | `Rel_Association(from, to, "label")` |

## PlantUML Alternatives

Since ArchiMate macros require remote includes that may not work reliably with Kroki, we use standard PlantUML syntax:

| ArchiMate Concept | PlantUML Alternative |
|-------------------|---------------------|
| Business Actor | `actor "Name" as alias` |
| Application Component | `[Component Name] as alias` |
| Technology Node | `node "Name" as alias { }` |
| Technology Artifact | `database "Name" as alias` |
| Package/Grouping | `package "Name" { }` |
| Cloud/External | `cloud "Name" as alias { }` |

## Resources

For complete documentation, see:

- [Archimate-PlantUML reference](https://github.com/plantuml-stdlib/Archimate-PlantUML)
- [PlantUML documentation](https://plantuml.com/)
- [ArchiMate specification](https://pubs.opengroup.org/architecture/archimate3-doc/)
