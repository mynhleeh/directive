---
trigger: glob
globs: "**/requirements/**, **/analysis/**, **/design/**, **/*.puml, **/*.mmd"
description: "Object-oriented analysis and design boundaries: strict separation of Requirements (WHAT), OOA (domain mechanics), and OOD (layered realization), Inside-Out dependencies, SOLID, purposeful design patterns, goal-oriented use cases, and UML notation."
---

# Software Architecture & Modeling Standards

Enforces clean abstraction boundaries across requirements, object-oriented analysis (OOA), and object-oriented design (OOD), keeping domain models decoupled from storage, UI, and language details.

## 1. Strict Three-Layer Abstraction Boundaries

| Phase / Layer | Core Focus | Mandatory Boundaries & Prohibitions |
| --- | --- | --- |
| **Requirements (SRS / PRD)** | Business goals, actors, invariants, technology-agnostic error flows (**WHAT**) | MUST contain **0** class names, repository/ORM names, GoF pattern tags, database schemas, or language method signatures, even inside parentheses as developer hints |
| **Analysis (OOA)** | Language-independent domain mechanics and conceptual structures | Separate **Entities** (unique identity and mutable lifecycle) from **Value Objects** (immutable, attribute-defined, zero independent identity); avoid framework specifics |
| **Design (OOD)** | Realization into cohesive software modules and patterns (**HOW**) | Link every component back to Tier 2 requirement identifiers; enforce inward-pointing dependencies (Section 2) |

## 2. Inside-Out Architectural Layering

Structure system realizations in 4 concentric layers where outer layers depend strictly inward on inner abstractions:

1. **Layer 1 - Domain Core:** Entities, Value Objects, and Domain Exceptions. Zero dependencies on I/O, databases, frameworks, or transport protocols.
2. **Layer 2 - Repository & Port Interfaces:** Pure interface contracts defining persistence queries and external gateway ports.
3. **Layer 3 - Domain Services & Use Cases:** Business transaction coordination, cross-entity invariants, and domain calculations. Depends only on Layer 1 and Layer 2 abstractions.
4. **Layer 4 - Controllers, Gateways & UI Adapters:** Input parsing, validation, serialization, and view rendering. Depends inward on Layer 3 without leaking transport details into domain models.

## 3. Goal-Oriented Use Cases & Diagram Complexity

1. **Goal-Oriented Naming:** Name every use case, process step, and behavioral node using `<Action Verb> + <Object>` delivering measurable actor value (e.g., `Schedule Appointment`, `Cancel Reservation`).
2. **Zero CRUD Bundles:** Split generic catch-all actions labeled `"Manage X"` into distinct goal-oriented use cases with explicit preconditions and failure paths. Count of `"Manage..."` use cases MUST equal **0**.
3. **Diagram Node Cap:** Limit each single diagram to at most **9** nodes. When a workflow spans more than 9 nodes or mixes synchronous user flows with asynchronous background tasks, decompose into a Tier-1 overview diagram plus focused Tier-2 sub-diagrams.
4. **Semantic Relationship Integrity:** Model mutually exclusive paths as separate flows (never abuse optional extension links for exclusive branches), and maintain 100% parity between diagram elements and body text (zero undocumented phantom nodes).

## 4. SOLID Discipline & Purposeful Patterns

1. **Single Responsibility (SRP):** Assign each module or class one cohesive reason to change (decouple calculation algorithms from entity state or persistence).
2. **Open/Closed (OCP):** Extend behavioral variants via interfaces and polymorphism rather than modifying tested conditional chains.
3. **Liskov Substitution (LSP):** Subtypes MUST honor supertype preconditions, postconditions, and invariants without unexpected exceptions or weakened contracts.
4. **Interface Segregation (ISP):** Prefer small, client-specific port interfaces over monolithic interfaces.
5. **Dependency Inversion (DIP):** High-level services MUST depend on Layer 2 abstractions, never concrete storage or driver classes.
6. **Purposeful Pattern Selection:** Apply GoF patterns only when a concrete structural driver exists:
   - Strategy: interchangeable calculation or policy algorithms.
   - Factory: encapsulating polymorphic creation of variant domain objects.
   - State: governing explicit entity lifecycle transitions and valid state rules.
   - Observer: decoupled propagation of domain events across independent handlers.

## 5. UML Diagram Standards (Mermaid & PlantUML)

1. **Class Diagrams:** Declare explicit member visibility (`+` public, `-` private, `#` protected), exact multiplicity on associations, and accurate relationship symbols: Inheritance (`<|--`), Interface Realization (`<|..`), Aggregation (`o--`), Composition (`*--`), and Dependency (`..>`).
2. **Sequence Diagrams:** Distinguish synchronous from asynchronous calls and delimit branches, iterations, and optional flows explicitly using `alt`, `loop`, and `opt` blocks.

## 6. Rationalization Blockers & Red Flags

| Rationalization Under Pressure | Mandatory Counter-Rule |
| --- | --- |
| "Put repository and factory class names in parentheses inside the SRS so developers do not have to guess." | Leaks Design (HOW) into Requirements (WHAT). Put technology-agnostic outcomes in the SRS and map classes in OOD deliverables only. |
| "Combine login, CRUD, notifications, billing, and audit into 1 big flowchart so stakeholders see everything." | Violates the 9-node cap and mixes sync/async concerns. Split into focused diagrams per goal. |

**Red Flags:** `"Manage [Entity]"` headings in SRS; class or method signatures in Requirements specs; single diagrams exceeding **9** nodes; services directly importing database or filesystem drivers.
