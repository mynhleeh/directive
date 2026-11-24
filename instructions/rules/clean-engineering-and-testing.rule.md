---
trigger: glob
globs: "**/src/**, **/test/**, **/tests/**, **/*.java, **/*.py, **/*.ts, **/*.js, **/*.go, **/*.cs, **/*.rs"
description: "Language-agnostic clean engineering and testing discipline: micro-unit inside-out delivery, pre-implementation alignment gate, zero-guesswork halting, precision decimal arithmetic, 5-group edge-case test matrix, and dual-verification gate."
---

# Clean Engineering & Testing Discipline

Establishes incremental construction, code hygiene, exact-precision arithmetic, and automated verification standards across software implementation tasks.

## 1. Micro-Unit Delivery & Pre-Implementation Alignment Gate

1. **Single Micro-Unit Per Turn (R1):** Author or modify at most **1** coherent unit per turn: `(a)` 1 immutable Value Object with its test suite, `(b)` 1 Domain Entity with its test suite, `(c)` 1 Repository/Port interface, or `(d)` 1 Service method/handler with its targeted tests. Bulk multi-layer generation (`Entity + Service + Controller`) in a single turn is prohibited.
2. **Inside-Out Build Order:** Construct from Layer 1 Domain Core outward to Layer 4 Controllers/UI per `software-architecture-and-modeling.rule.md`.
3. **Mandatory Alignment Gate:** Before writing or editing production source code, state a concise alignment block in chat:
   - *Target Coordinates:* File path, module/package, and exact type or function signature.
   - *Public Contract:* Constructors/factories, parameter types, return types, and explicit error types.
   - *Invariants & Traceability:* Non-null, range, and domain invariants mapped to Tier 2 requirement IDs.
   - *Blast Radius & Test Plan:* Target test file and specific boundary cases to verify in the same turn.
4. **Zero-Guesswork Halting:** When any formula, rounding rule, validation threshold, or status default is absent or ambiguous in Tier 2, HALT before authoring code and present an Option A vs. Option B trade-off table for user decision.

## 2. Clean Code Hygiene

1. **Cohesive Function Cap:** Keep functions <= **25** lines of code; extract nested branches or multi-step transformations into clearly named private helper functions whenever a function exceeds 25 lines.
2. **Self-Documenting Code:** Eliminate comments that restate syntax (`// get balance`, `// return list`). Reserve inline comments for non-obvious algorithms and explicit Tier 2 business rule IDs; limit docstrings to public API contracts and interfaces.
3. **Contextual Naming:** Prohibit vague identifiers (`temp`, `res`, `data`, `val1`, or opaque 1-to-2-letter names outside conventional tiny loop indices). Use explicit domain-paired names (`sourceAccount` vs. `targetAccount`).

## 3. Precision Arithmetic & Domain Invariants (Conditional)

Apply strictly whenever implementing monetary balances, billing fees, interest rates, taxes, currency conversions, or exact-decimal quantities:

1. **Zero Binary Floating-Point:** Prohibit `float`, `double`, and IEEE-754 floating-point `number` operations for exact monetary or rate arithmetic.
2. **Explicit Scale & Rounding Policy:** Use arbitrary-precision decimal types (`BigDecimal`, Python `Decimal`, dedicated decimal libraries) or integer minor units. Every division or rounding step MUST explicitly specify scale and rounding mode: use banker's rounding (`HALF_EVEN`) when Tier 2 explicitly selects standard financial rounding or delegates rounding policy to engineering standards; if Tier 2 is silent on a domain rounding rule, halt per Section 1.4 and confirm `HALF_EVEN` vs. the domain alternative with the user.
3. **Boundary & Temporal Types:** Enforce strict positivity invariants where required (`amount > 0`), validate against negative or invalid intervals (`used > total`, reversed dates), and use standard immutable calendar/date-time types (`java.time`, `datetime.date`, ISO 8601 libraries) instead of raw string slicing or float timestamps.

## 4. Five-Group Edge-Case Test Matrix & Isolation

Every domain model, value object, and service unit requires a paired automated test suite structured in **Given-When-Then** (Arrange-Act-Assert) form covering all applicable groups below (parameterized where inputs vary):

| Test Group | Mandatory Coverage Scenarios |
| --- | --- |
| **1. Happy Path** | Nominal valid inputs, standard state transitions, balanced post-operation invariants |
| **2. Boundary & Precision** | Minimum representable units (`0.01` or `1` minor unit), large values (`10^12+`), exact midpoint rounding cases (`HALF_EVEN` tie-to-even verification) |
| **3. Negative, Zero & Limits** | Explicit rejection of zero or negative quantities where invalid, out-of-range bounds (`used > total`), overdraft/capacity denials |
| **4. Temporal & Calendar** | Leap days (Feb 29, 365 vs. 366-day bases), month-end boundaries (28 to 31), reversed start/end intervals, and any Tier 2 day-count convention |
| **5. State, Null & Idempotency** | Closed/frozen entity rejections, null/blank/malformed inputs, duplicate request or transaction ID idempotency |

**Isolation Boundary:** Test pure Domain Entities and Value Objects directly **without mocks**. Use mocks or fakes in Service tests solely to isolate Layer 2 repositories and external I/O ports.

## 5. Dual-Verification Gate (Mandatory Before `DONE`)

No code micro-unit may be marked complete until both gates pass after the final edit:

1. **Gate 1 - Automated Test Execution Log:** Run the project's test suite (`mvn test`, `pytest`, `npm test`, `go test`, etc.) and record the actual terminal summary proving **0** failures, **0** errors, and **0** skipped tests.
2. **Gate 2 - Upstream Spec & Design Alignment:** Confirm 100% parity between implemented types, signatures, invariants, and error flows against Tier 2 requirements and OOD models. If implementation exposes an upstream flaw, stop and apply R7 backward synchronization before finalizing.

## 6. Rationalization Blockers & Red Flags

| Rationalization Under Pressure | Mandatory Counter-Rule |
| --- | --- |
| "`float` is built-in and fast for a quick prorated fee script." | Binary floats introduce silent rounding drift in money/rate math. Always use exact decimal or integer minor units with explicit rounding. |
| "One happy-path `assert` is enough; the formula is obvious." | Obvious formulas fail at midpoints, leap years, zero/negative bounds, and frozen states. Cover all 5 matrix groups. |
| "Skip running tests or pick a default rounding mode to meet the deadline." | Guessing business rules violates R2, and claiming readiness without test output violates R3. |

**Red Flags:** using `float`/`double` for currency; writing only 1-to-2 happy-path assertions; generating `Entity + Service + Controller` together; declaring code ready without a post-edit test runner log.
