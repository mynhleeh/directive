---
trigger: always_on
description: "End-to-end task orchestration pipeline: classification, dynamic skill discovery, risk-based planning, scaffold-first unit construction with FIFO/LIFO ordering, direct-by-default subagent policy, whole-scope sweep, and evidence-backed handover."
---

# Task Workflow & Construction Lifecycle

Standard execution pipeline for any task, integrating incremental scaffold-first construction with six-phase task orchestration and collaborative draft review.

## 1. Six-Phase Execution Pipeline

### Phase 0: Classification & Grounding

1. Classify the request into one primary type: `SPECIFY`, `DESIGN`, `CODE`, `REVIEW`, `RESEARCH`, `EXPLAIN`, `MAINTAIN`, or `MIXED` (split `MIXED` into typed units).
2. Resolve the active workspace scope (`ACTIVE_BRANCH`) and rank available grounding sources per `knowledge-grounding-and-citation.rule.md`.
3. If an authoritative source is missing or requirements are ambiguous, stop and ask 1 focused question per message (R2); otherwise proceed immediately.

### Phase 1: Dynamic Skill Discovery

1. Scan available skill `description` fields dynamically at task start and at every phase boundary; never rely on a cached skill list.
2. Apply every matching skill (preferring the strongest fit among overlapping skills) and announce each activation: `"Using [skill] to [purpose]"`.
3. Do not invoke skills whose trigger conditions do not match, and do not invoke multi-agent orchestration skills automatically unless permitted under Section 3.

### Phase 2: Planning, Risk Class & Decision Gate

1. Decompose work into coherent units (1 document subsection, 1 model/module, or 1 paired unit + test), specifying unit order, verification command, and Risk Class:
   - High Risk: alters a business rule, formula, requirement/traceability identifier, or system architecture (treat unclear risk as High).
   - Low Risk: alters only formatting, cross-references, table alignment, or lint hygiene.
2. Perform a Two-Way Ripple Check (R7) on every planned unit to identify upstream spec impacts and downstream derivative impacts.
3. Request user plan approval before Phase 3 whenever the plan adds, removes, or renames an identifier or exceeds **3 units**. Small low-decision plans start immediately.
4. Present any unsettled policy, formula, or scope choice using a 4-part decision prompt: `(a) issue nature, (b) concrete numeric/date example, (c) options comparison table, (d) grounded recommendation`. Never record a recommendation as a decision before user confirmation.

### Phase 3: Unit Execution Loop

Execute 1 unit per turn (R1), applying the Scaffold-First Construction Protocol (Section 2) for new content or surgical edits for existing content, followed by mandatory verification and review before locking `DONE`.

### Phase 4: Whole-Scope Sweep

1. After all units finish, search the entire active workspace scope for every modified or deprecated identifier and term; unhandled matches MUST equal **0** (keep command + count as evidence).
2. Report out-of-scope matches to the user without silently modifying unrelated files.
3. Re-run all checks of `markdown-formatting-and-layout.rule.md` across every Markdown file created or edited in the session, since later edits can invalidate earlier passes.

### Phase 5: Handover

Report per unit: final status, exact verification command with observed output (R3), open findings, and recommended next step.

## 2. Scaffold-First Construction Protocol

Applies whenever creating a new document, major section (`H2`/`H3`), or code module from zero. Generating multi-unit or complete monolithic deliverables in one response is prohibited.

### 2.1. Mandatory 5-Step Collaborative Loop

1. **Step A - Knowledge Grounding:** Identify verified sources (Tier 1, Tier 3, or external) for the unit.
2. **Step B - Scaffold Construction:** Emit only the skeletal headings and labeled placeholders declaring each unit's objective and completion boundary (exempt from the 1-unit limit because no body content is generated).
3. **Step C - Scope Alignment:** Clarify boundaries, assumptions, and edge cases with the user.
4. **Step D - Draft Preview Gate:** Present the single unit's concrete draft in chat or scratchpad for review. Never write Step E without explicit user approval of Step D.
5. **Step E - Surgical Write:** Write at most 1 approved unit to the target file and execute verification.

### 2.2. Queue (FIFO) vs. Stack (LIFO) Dependency Ordering

1. Queue (FIFO): build independent peer units strictly in the declared Step B sequence (`A -> B -> C`); never reorder arbitrarily.
2. Stack (LIFO): when drafting unit `A` reveals an unfinished prerequisite `B`, immediately mark `A` as `BLOCKED`, push `B` onto the active stack, complete `B` through Steps A to E + Verification (nesting further if `B` depends on `C`), and pop `A` only after `B` reaches `DONE`.
3. Always state explicitly whether Queue or Stack is active and why. Never bypass a missing prerequisite by emitting `[TBD]` placeholder prose inside dependent sections.

### 2.3. Explicit Unit State Machine & Post-Build Gate

Track every unit in chat using explicit states: `PENDING`, `SCAFFOLDED`, `BLOCKED`, `DISCUSSED`, `DRAFTED`, `APPROVED`, `DONE`. Before transitioning any unit to `DONE`, complete and log evidence for all 4 post-build checks:
1. **Verify:** Execute the domain-appropriate check (test suite, linter, regex/awk counts, diff) and record actual output.
2. **Quality Assurance:** Cross-check the unit against its Step B scaffold and Step A sources (0 unfilled items).
3. **Rule Compliance:** Audit against all active workspace rules (0 violations).
4. **Optimize:** Tighten clarity/structure without altering meaning, re-verify, or record `0 findings` with check evidence.

## 3. Subagent Delegation & Review Loops

1. Direct-by-Default Execution: execute research, drafting, editing, and verification directly in the primary turn unless **(a)** the user explicitly requests subagents, or **(b)** an active agent or skill protocol explicitly authorizes isolated subagents (e.g., > 40,000-token context isolation or fresh-context stranger review).
2. Isolation Invariants (when subagents are used): assign strictly independent units; forbid shared mutable state; forbid parallel writes to the same file; forbid subagents from spawning recursive subagents; never assign review to the subagent that authored the unit.
3. Convergence: fix every evidence-backed finding (location, quoted text, count) and re-verify until `0` findings remain. If identical findings repeat across rounds, halt and escalate the root conflict to the user.

## 4. Safety & Editing Hygiene

- Read any target file immediately before editing; modify only the smallest region required by the unit (except formatting sweeps on files touched in the current session).
- Never rely on remembered paths from earlier turns; inspect the current directory tree before acting.

## 5. Rationalization Blockers & Red Flags

| Rationalization Under Pressure | Mandatory Counter-Rule |
| --- | --- |
| "Stakeholder needs the spec in 10 minutes; emit Sections 2 and 3 with `[TBD]` tags for the unwritten Section 4." | Violates LIFO Stack ordering and Step D approval. Halt dependent Section 2, mark `BLOCKED`, scaffold the full doc, and complete Section 4 first. |
| "It is faster to draft all 5 sections together and let the user edit." | Monolithic generation hides compound errors. Emit the scaffold first (Step B), then build 1 approved unit per turn. |

**Red Flags:** writing prose for a `BLOCKED` unit using assumed contracts; skipping Step D draft approval; declaring `DONE` without post-build verification output.

*Provenance: Consolidated and generalized from `pfms_oop-prj_mng/.agents/rules/05-scaffold-first-construction.rule.md`, `06-general-workflow.rule.md`, and `00-core-charter.rule.md [R8]`.*
