---
name: usecase-diagram
description: "Generate production-grade UML 2.5 Use Case diagrams (PlantUML) with system boundaries, domain package grouping, and verified relationship semantics (include/extend/generalization). Bundles a cross-platform Python rendering engine and automated coverage audit gates. Trigger whenever the user asks to create, update, or audit a use case diagram for a feature or system scope."
version: "1.0.0"
tags:
  - diagram
  - uml
  - usecase
  - plantuml
  - business-analysis
  - active-skill
  - visual-spec
license: MIT
---

# Universal Use Case Diagram Generator (`usecase-diagram`)

Self-contained skill for producing, rendering, and auditing production-grade **UML 2.5 Use Case Diagrams** using native PlantUML. Combines business-first actor elicitation, automated cross-platform rendering (Windows/Linux/macOS), and embedded architectural review gates.

---

## When to Activate

Activate when the user requests:
- Creating a visual Use Case diagram for a new feature, module, or product kickoff.
- Mapping system boundary, primary/secondary actors, and domain use case clusters.
- Modeling formal UML relationship semantics (`<<include>>`, `<<extend>>`, actor/use case generalization).
- Updating, auditing, or refactoring existing `.puml` use case diagrams and their index documentation.
- Commands or prompts like: `/usecase-diagram`, `draw usecase diagram`, `map feature actors`, `vẽ sơ đồ usecase`.

> **Do NOT trigger for:**
> - Step-by-step procedural interaction sequences (use sequence diagram).
> - Multi-lane process execution flows (use activity swimlane or BPMN).
> - Detailed textual use case prose specifications (use Cockburn-style `/usecase` text authoring).

---

## Embedded Governance & Rules

All executions must strictly adhere to the following inlined governance policies:

### 1. Human-in-the-Loop (HITL) Approval Gates
- **L1 Plan Preview (Mandatory before creating files):**
  Before writing `.puml` or index files, present a clear, business-readable summary table detailing:
  1. Target output paths (`.puml`, `.svg`, index markdown).
  2. Actor count and categories (Primary vs Secondary/External).
  3. Total use cases and proposed domain package groupings.
  4. Explicit list of `<<include>>` and `<<extend>>` relationships with rationale.
  *Wait for user confirmation (`Y` / `yes`) before writing.*
- **L2 Diff Preview (Mandatory when updating existing files):**
  When modifying an existing diagram, display unified diffs highlighting modified actors, nodes, or links.

### 2. IT-BA Business Framing
- **Business Language Only:** Ask only about business roles, external service partners, trigger events, and observable outcomes.
- **Prohibited Technical Jargon:** Never prompt the user for database column names, REST endpoints, JSON payloads, or authentication token mechanics.

### 3. UML 2.5 Structural Discipline
- **Mandatory System Boundary:** All use cases must reside inside `rectangle "System: <Name>" { ... }`. Zero actors inside the boundary.
- **Domain Package Grouping:** When $\ge 8$ use cases or multiple business domains exist, group cases into logical `package "<Sub-domain>" { ... }` blocks.
- **Verified Relationship Semantics:**
  - `<<include>>`: Mandatory sub-routine. Base points to Included: `(Base) .> (Included) : <<include>>`.
  - `<<extend>>`: Optional/conditional branch. Extension points to Base: `(Extension) .> (Base) : <<extend>>`.
  - Every relationship must have an explicit business rationale in the documentation table.

---

## Execution Workflow Pipeline

```
Context & Input ──► Actor & UC Mining ──► L1 Plan Gate ──► Synthesize .puml ──► Render Engine ──► Review Gate ──► Final Index Emit
```

### Stage 1: Context Resolution & Discovery
1. Identify the target feature slug:
   - Extract from `--feature <slug>` argument, or auto-detect from working directory (`docs/{feature}/`).
   - If ambiguous, ask the user to specify the feature slug.
2. Mine upstream facts (if available):
   - Scan `docs/{feature}/usecases/` or `srs/{feature}-spec.md` for existing actor mentions and use case titles.
   - If no upstream files exist, conduct a brief business interview to capture actors and core goals.

### Stage 2: Actor & Use Case Classification
1. **Classify Actors:**
   - *Primary (Human initiators)*: Placed on the left.
   - *Secondary / System (External services, payment, notification)*: Placed on the right with `<<System>>` stereotype.
2. **Cluster Use Cases:**
   - Identify sub-domains (e.g., Browsing, Checkout, Profile, Admin) to form PlantUML packages.
3. **Map Relationships:**
   - Identify shared mandatory actions (`<<include>>`) and conditional augmentations (`<<extend>>`).

### Stage 3: L1 Approval Gate
Present the proposed diagram plan to the user in prose/table format. Do NOT write any files until the user approves.

### Stage 4: Synthesize PlantUML (`.puml`)
1. Create `docs/{feature}/usecases/{feature}-usecase-diagram.puml` applying the standard skinparam styling from `references/plantuml-syntax-guide.md`.
2. Format:
   ```plantuml
   @startuml
   !theme plain
   skinparam roundCorner 10
   skinparam defaultFontName "Inter", "Segoe UI", sans-serif
   left to right direction

   actor "Customer" as Customer
   actor "Payment Gateway" as PaymentGW <<System>>

   rectangle "System: {feature}" {
       package "Ordering" {
           usecase "Place Order" as UC_PlaceOrder
           usecase "Validate Cart" as UC_ValidateCart
           usecase "Apply Coupon" as UC_Coupon
       }
   }

   Customer -- UC_PlaceOrder
   UC_PlaceOrder .> UC_ValidateCart : <<include>>
   UC_Coupon .> UC_PlaceOrder : <<extend>>
   UC_PlaceOrder -- PaymentGW
   @enduml
   ```

### Stage 5: Cross-Platform Compile & Render
Execute the bundled Python rendering engine:
```bash
python instructions/skills/active/usecase-diagram/scripts/render.py docs/{feature}/usecases/{feature}-usecase-diagram.puml
```
- If compilation fails, inspect the error output from stderr, correct the `.puml` syntax, and retry (maximum 2 retries).

### Stage 6: Embedded Quality Gate (Reviewer)
Run an architectural review against `references/reviewer-checklist.md`:
- If subagent tools (`invoke_subagent` / `define_subagent`) are available, dispatch a fresh reviewer agent with the generated diagram and fact list.
- Otherwise, execute a strict **Pass-2 Self-Audit**:
  - [ ] System boundary present and encompassing all use cases?
  - [ ] Actors situated strictly outside the boundary?
  - [ ] `<<include>>` arrows pointing Base $\rightarrow$ Included?
  - [ ] `<<extend>>` arrows pointing Extension $\rightarrow$ Base?
  - [ ] Zero orphan use cases?
- Fix any `BLOCKING` issues before finalizing.

### Stage 7: Emit & Link Specification Index
1. Create or update `docs/{feature}/usecases/{feature}-usecase-index.md` using `templates/usecase-index.md`.
2. Embed the rendered `.svg` image and populate the Actors, Use Cases, and Relationships tables.
3. Report completion to the user with paths to the `.svg`, `.puml`, and index markdown.

---

## Anti-Patterns & Common Failure Modes

| ❌ Anti-Pattern | Why It Fails | ✅ Required Behavior |
|---|---|---|
| **Missing System Boundary** | Fails UML scope definition; confuses internal vs external responsibilities. | Wrap all use cases in `rectangle "System: <Feature>" { ... }`. |
| **Inverted `<<include>>` Arrow** | Pointing from included to base implies the included action depends on the caller. | Base points to Included: `(Base) .> (Included) : <<include>>`. |
| **Inverted `<<extend>>` Arrow** | Extension must point to the base it decorates, not vice versa. | Extension points to Base: `(Extension) .> (Base) : <<extend>>`. |
| **Micro-Step Use Cases** | Treating UI clicks ("Click Button", "Enter Password") as use cases creates clutter. | Consolidate steps into single user goals delivering business value. |
| **Direct Actor-to-Actor Lines** | Actors do not interact directly in use case diagrams. | Remove link; use sequence diagram if inter-actor communication matters. |
| **Skipping L1 Plan** | Unvetted file creation leads to churn and misaligned business boundaries. | Always show L1 plan and obtain explicit confirmation before writing files. |

---

## Tooling & Component References

- **Render Script**: `scripts/render.py` (Pure Python 3 standard library, cross-platform compiler).
- **Syntax Cheatsheet**: `references/plantuml-syntax-guide.md` (Styling parameters, layout hints).
- **Review Checklist**: `references/reviewer-checklist.md` (Countable audit gates and severity rubric).
- **Index Template**: `templates/usecase-index.md` (Standardized markdown documentation wrapper).
