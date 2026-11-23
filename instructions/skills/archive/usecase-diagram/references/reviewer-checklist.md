# Quality Gate: Use Case Diagram Reviewer Checklist

> Persona: **UseCase_Auditor**  
> Focus: Structural UML 2.5 compliance, boundary integrity, relationship semantics, and business coverage.

---

## 1. Audit Principles

1. **Syntactic validity is necessary but insufficient:** Compiling to SVG proves only that PlantUML parsed the text; it does not prove the diagram represents valid system boundaries or accurate business scope.
2. **Strict Scope Demarcation:** In UML 2.5, a use case diagram defines system boundaries. Actors reside outside the system; use cases reside inside.
3. **No Functional Decomposition:** A use case represents a complete end-to-end user goal delivering observable value, not an isolated UI step or function call.

---

## 2. Review Checklist (Countable & Mechanical)

### Dimension A: Scope & Boundary Enclosure
- [ ] **System Boundary Present:** All use cases must be enclosed within a declared system boundary:
  ```plantuml
  rectangle "System: <Feature Name>" { ... }
  ```
- [ ] **Actors Outside Boundary:** Zero actors are declared inside the system boundary rectangle.
- [ ] **Domain Package Grouping:** If the feature contains $\ge 8$ use cases or spans multiple business sub-domains (e.g., Catalog, Checkout, Admin, Fulfillment), use cases must be clustered into named packages inside the boundary.

### Dimension B: Actor Classification & Orientation
- [ ] **Primary Actors:** Human users who initiate goals placed on the left side (`left to right direction`).
- [ ] **Secondary / System Actors:** Supporting services or downstream recipients placed on the right side. External services must use the `<<System>>` or `<<External Service>>` stereotype.
- [ ] **No Actor-to-Actor Associations:** Actors must never be linked directly to other actors via association lines (generalization `<|--` between actors is the only exception).

### Dimension C: Relationship Semantics & Arrow Directions
- [ ] **Actor Association:** Solid undirected line (`Actor -- (Use Case)`). No arrows on primary association lines.
- [ ] **`<<include>>` Direction (Base $\rightarrow$ Included):**
  - Dependency: The base use case unconditionally requires the included use case.
  - Arrow orientation: Dotted open arrow pointing **from Base to Included**:
    ```plantuml
    (Place Order) .> (Validate Cart) : <<include>>
    ```
- [ ] **`<<extend>>` Direction (Extension $\rightarrow$ Base):**
  - Optionality: The extension use case conditionally augments the base use case at an extension point.
  - Arrow orientation: Dotted open arrow pointing **from Extension to Base**:
    ```plantuml
    (Apply Promo Coupon) .> (Place Order) : <<extend>>
    ```
- [ ] **Relationship Evidence & Rationale:** Every `<<include>>` and `<<extend>>` relationship must be accompanied by an explicit business rationale in the metadata documentation table.

### Dimension D: Graph Completeness & Orphan Prevention
- [ ] **Zero Orphan Use Cases:** Every use case in the diagram must either connect directly to an actor OR be connected to another use case via `<<include>>`, `<<extend>>`, or generalization.
- [ ] **Observable Value Test:** No use case should represent a single atomic screen action (e.g., "Enter OTP" or "Click Submit" must be part of the authentication use case flow, not a standalone bubble).

---

## 3. Severity Rubric

### 🔴 BLOCKING (Must be fixed before finalizing)
1. Missing system boundary rectangle (unscoped diagram).
2. Actors drawn inside the system boundary.
3. Inverted `<<include>>` or `<<extend>>` arrows.
4. Orphan use cases completely disconnected from the graph.
5. Direct association line between two actors.

### 🟡 WARNING (Requires explicit confirmation or justification)
1. Flat diagram with $> 8$ use cases without domain package clustering.
2. Missing business rationale for `<<include>>` or `<<extend>>` associations.
3. External system actor missing `<<System>>` stereotype.

### 🟢 SUGGESTION (Optional aesthetic polish)
1. Excessive line crossings (resolve by using hidden direction hints `-[hidden]-`).
2. Label clarity improvements.

---

## 4. Auditor Report Output Contract

When invoked as a subagent or during a self-review pass, format findings as follows:

```markdown
### Use Case Quality Gate Audit
- **Status**: [PASS | FAIL]
- **Metrics**: Actors: {N} | Use Cases: {M} | Packages: {K} | Includes: {I} | Extends: {E}

#### Findings:
- [BLOCKING | WARNING | SUGGESTION] Item description
  - *Location*: Node or relationship name
  - *Violation*: Exact checklist rule violated
  - *Remediation*: Concrete PlantUML snippet fix
```
