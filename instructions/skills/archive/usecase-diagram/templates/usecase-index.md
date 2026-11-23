# Use Case Specification & Index: {{FEATURE_NAME}}

> Feature Slug: `{{FEATURE_SLUG}}`  
> Last Updated: `{{LAST_UPDATED}}`  
> Status: `Draft`

---

## 1. System Scope & Boundary

- **System Name**: `{{SYSTEM_NAME}}`
- **Scope Overview**: {{SCOPE_DESCRIPTION}}
- **Domain Subsystems**:
{{DOMAIN_PACKAGES_LIST}}

---

## 2. Use Case Diagram

<p align="center">
  <img src="{{FEATURE_SLUG}}-usecase-diagram.svg" alt="UML Use Case Diagram: {{FEATURE_NAME}}">
</p>

*Source file*: [`{{FEATURE_SLUG}}-usecase-diagram.puml`]({{FEATURE_SLUG}}-usecase-diagram.puml)

---

## 3. Actors Inventory

| Actor Name | Category | Stereotype | Responsibilities / Triggers | Source / Reference |
|---|---|---|---|---|
| {{ACTOR_1}} | Primary | None | {{ACTOR_1_ROLE}} | {{ACTOR_1_SRC}} |
| {{ACTOR_2}} | Secondary / External | `<<System>>` | {{ACTOR_2_ROLE}} | {{ACTOR_2_SRC}} |

---

## 4. Use Cases Summary

| UC ID | Use Case Name | Package / Domain | Primary Actor | Business Goal Summary |
|---|---|---|---|---|
| UC-01 | {{UC_1_NAME}} | {{UC_1_PACKAGE}} | {{UC_1_ACTOR}} | {{UC_1_GOAL}} |
| UC-02 | {{UC_2_NAME}} | {{UC_2_PACKAGE}} | {{UC_2_ACTOR}} | {{UC_2_GOAL}} |

---

## 5. Relationships & Business Rationale

| Type | From Element | To Element | Business Rationale & Preconditions |
|---|---|---|---|
| `<<include>>` | {{FROM_UC}} | {{TO_UC}} | {{INCLUDE_RATIONALE}} |
| `<<extend>>` | {{FROM_UC}} | {{TO_UC}} | {{EXTEND_RATIONALE}} |
| `Generalization` | {{CHILD_ACTOR}} | {{PARENT_ACTOR}} | {{INHERITANCE_RATIONALE}} |
