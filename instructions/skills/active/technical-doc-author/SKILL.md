---
name: technical-doc-author
description: "Use when authoring, restructuring, or auditing software engineering specs and operational docs across 8 archetypes (SRS/PRD, SDD, ADR, RFC, Tech Report/Benchmark, Postmortem/RCA, API Spec, Runbook/SOP) requiring Diataxis isolation, abstraction-layer locks, POLA namespaced UIDs, and trade-off/traceability closure. Do NOT trigger for standalone prose de-AI/humanizing (use humanizer or de-aigc-skills), generic collaborative drafting without doc-type governance (use doc-coauthoring), pure diagram rendering (use markdown-mermaid-writing or diagram skills), coding EARS workflows (use sdd), or application coding/debugging."
version: "4.0.0"
tags:
  - technical-documentation
  - srs
  - sdd
  - adr
  - rfc
  - benchmark-report
  - postmortem
  - api-spec
  - runbook
  - diataxis
  - pola-uid
  - traceability
license: MIT
compatibility: "Platform-agnostic (Claude, Codex, Gemini, Cursor, Antigravity). Standalone portable with zero hardcoded workspace paths; respects active workspace rules when present."
---

# Technical Document Author

> Author and audit 8 industrial engineering document archetypes (`DOC-1` to `DOC-8`) with strict Diataxis isolation, abstraction-layer locks, POLA namespaced identifiers, and empirical traceability closure.

## When to Activate

Activate when the user requests creating, restructuring, or auditing:
1. `DOC-1`: Software / Product Requirements Specification (SRS / PRD).
2. `DOC-2`: Software / System Design Description (SDD / Architecture Overview).
3. `DOC-3`: Architecture Decision Record (ADR).
4. `DOC-4`: Engineering Proposal / Request for Comments (RFC).
5. `DOC-5`: Technical Investigation / Benchmark Evaluation Report.
6. `DOC-6`: Incident Postmortem / Root Cause Analysis (RCA).
7. `DOC-7`: API Specification / Data Schema Contract.
8. `DOC-8`: Operational Runbook / Standard Operating Procedure (SOP).
- Keywords: `"SRS"`, `"PRD"`, `"SDD"`, `"design doc"`, `"ADR"`, `"RFC"`, `"benchmark report"`, `"postmortem"`, `"RCA"`, `"API spec"`, `"runbook"`, `"SOP"`, `"Diataxis"`, `"POLA"`.

Do NOT activate for:
- Standalone prose de-AI, tone humanizing, or watermark/metadata scrubbing -> delegate to `humanizer` or `de-aigc-skills`.
- Generic collaborative context gathering or fresh-reader testing without engineering archetype governance -> delegate to `doc-coauthoring`.
- Standalone diagram syntax, PlantUML/D2/BPMN rendering, or scientific Markdown styling -> delegate to `markdown-mermaid-writing` or specialized diagram skills (`diagram-skills`, `mermaid-diagram`, `mermaid-architect-guide`, `plantuml-guide`, `excalidraw-diagram-guide`).
- Coding-oriented EARS feature workflows (`spec/intent.md -> tasks.md`) -> delegate to `sdd`.
- Application source coding or runtime debugging.

## Overview

General-purpose writing and diagram skills handle prose polish, co-authoring facilitation, and chart syntax, but they do not enforce industrial engineering document boundaries. This skill supplies the missing structural governance:
1. **Diataxis & Abstraction Lock**: Separates Problem (`WHAT`), Solution (`HOW`), Decision (`WHY`), Proposal (`PROPOSAL`), Empirical (`EVALUATION`), Retrospective (`POSTMORTEM`), Interface (`CONTRACT`), and Procedure (`PROCEDURE`) without cross-phase or textbook leakage.
2. **POLA Namespaced Identifiers**: Enforces domain-namespaced headings (`### X.Y [UID]: [Entity Name]`) and static parent context inheritance.
3. **Trade-Off & Breaking Point Realism**: Blocks "costless perfection" proposals by requiring >= 3 engineering trade-off axes and quantitative saturation limits.
4. **Cross-Modal & Traceability Closure**: Guarantees <= 9-node tiered diagrams, discrete `<Verb> + <Object>` goals, 0 phantom diagram entities, and closed bidirectional traceability.

## Language Policy

- Follow these English instructions for all internal reasoning, validation gates, and reference lookups.
- Emit all user-facing documents and explanations in the user's requested language (default English if unspecified).
- Keep the document strictly monolingual: do NOT append English glosses in parentheses after translated terms (`Tổng quan (Overview)`), except standard international proper nouns or protocol names (`gRPC`, `PostgreSQL`, `OAuth 2.0`).

## Instructions (4-Phase Sequential Workflow)

### Phase 1: Archetype Framing & Abstraction Lock

1. **Classify Archetype & Diataxis Quadrant**: Read `references/document-types-matrix.md` and lock the document to 1 archetype (`DOC-1` to `DOC-8`) and 1 Diataxis quadrant per section. When requests blur archetypes, triage by primary intent: single architectural choice -> `DOC-3` ADR; proposed cross-team evolution -> `DOC-4` RFC; complete system blueprint -> `DOC-2` SDD; split multi-domain requests into sequential artifacts.
2. **Enforce Information Domain Boundaries**:
   - `DOC-1` (SRS/PRD, `WHAT`): State actors, business invariants, goal-oriented use cases, and technology-agnostic error validations. **Forbid** OOD patterns, class/method signatures, library calls, exception class names, and SQL schemas, even if the user provided code snippets as background.
   - `DOC-2` (SDD, `HOW`): Specify topology, protocols, storage, and breaking points; cite `REQ-`/`BR-` UIDs instead of copying SRS narrative prose.
   - `DOC-3` / `DOC-4` (ADR / RFC): Mandate >= 2 rejected alternatives with explicit disqualification criteria, >= 3 trade-off axes, and negative operational consequences.
   - `DOC-5` (Benchmark): Require reproducible hardware/workload specs, percentiles (`P50`, `P95`, `P99`), and variance; reject unsupported claims.
   - `DOC-6` (Postmortem/RCA): Enforce blameless UTC timeline, 5-Whys fault chain, and remediation items with owner, priority, target date, and ticket UID.
   - `DOC-7` (API Spec): Require typed nullable/bounded payloads and standardized error contracts (e.g., RFC 7807 / gRPC codes).
   - `DOC-8` (Runbook/SOP): Require prerequisites, imperative commands, **stdout/stderr verification check per step**, **explicit rollback for destructive actions**, and escalation path. **Forbid** background theory essays inside operational steps.
3. **Zero Textbook & Proportional Rigor**: Omit pedagogical lectures (e.g., Miller's or Conway's law) and spurious predicate calculus ($\forall, \exists$) on routine business CRUD logic.
4. **Evolution Blast Radius Check**: When modifying an existing document, trace impacted upstream/downstream UIDs and preserve existing verified numerical thresholds, invariants, and accepted SLA/SLO targets. If changes introduce breaking trade-offs, halt to summarize the blast radius and align with the user before rewriting.

### Phase 2: Skeleton, POLA UIDs & Technical Thesis

1. **Enforce POLA Heading Syntax**: Every traceable entity section MUST use `### X.Y [PREFIX]-[DOMAIN]-[NN]: [Title]` (e.g., `### 2.1 BR-FIN-01: Balance Preservation`, `### 3.1 REQ-NET-01: Ingress Rate Limiting`).
   - **Prohibited**: Flat linear IDs (`UC01`, `FR01`, `ID01`, `FIND01`) and parenthetical trailing IDs (`### 3.1 Rate Limiting (REQ-01)`).
2. **Enforce Static Context Inheritance**: Sub-sections inherit parent context automatically; open directly with local facts, invariants, or tables without repeating project background.
3. **Require Technical Thesis & Trade-Offs (`DOC-2`, `DOC-3`, `DOC-4`, `DOC-5`)**: Open with a concise thesis (target problem, workload envelope, accepted constraints), >= 3 trade-off dimensions, and a quantitative Breaking Point.
4. **Close Traceability Loops**: Verify bidirectional closure (`Goal <-> BR <-> FR/UC <-> Test` for specs; `Hypothesis <-> Setup <-> Data <-> Finding <-> Rec` for reports; `Symptom <-> Timeline <-> 5-Whys <-> Action` for postmortems) with 0 orphaned entities.

### Phase 3: Focused Authoring & Portable Modeling

1. **Apply Blueprints**: Follow the structural outline for the selected `DOC-1` to `DOC-8` in `references/document-types-matrix.md`.
2. **Quantify Criteria Without Fabrication**: Replace qualitative adjectives (`fast`, `scalable`, `reliable`, `secure`) with numeric thresholds and tolerances. Never fabricate unprovided benchmark metrics, P99 SLAs, or incident timestamps; halt to ask for blocking empirical baselines (`DOC-5`, `DOC-6`), or flag unconfirmed operational targets outside the emitted deliverable for stakeholder ratification.
3. **Enforce Portable Visual & Syntax Standards**: Always read `references/visual-and-gate-contract.md` before finalizing:
   - Limit each diagram to **<= 9 nodes** (subgraphs do NOT exempt a diagram from the 9-node cap; split into Tier 1 Context <= 9 nodes + Tier 2 Subsystem <= 9 nodes).
   - Name behavioral units as `<Active Verb> + <Direct Object>`; eliminate `"Manage X"` / `"Quản lý X"` CRUD bundles.
   - Maintain 100% Cross-Modal Parity (0 phantom nodes) and attach a Component Contract Table under each architecture/pipeline diagram.
   - Use neutral 3rd-person POV (`The service`, `The operator`; imperative verbs in `DOC-8` Runbooks), zero 1st/2nd-person pronouns (`we`, `our`, `you`), self-contained body prose (isolate external citations under `## References` only when requested), `\|` for literal pipes in table math or code spans (never `&#124;`), 0 `---` thematic breaks in body text, and 0 em-dash (`—`) punctuation outside code spans.

### Phase 4: Portable Quality Gate Audit

1. Audit the finished document against all 8 gates (`G1`–`G8`) in `references/visual-and-gate-contract.md`.
2. If the current workspace provides active documentation or formatting rules (e.g., Markdown layout, modeling, or technical writing rules), apply those local physical formatting checks as final precedence before delivery.
3. For optional post-draft prose polish or fresh-reader verification, hand off to the companion skills listed below.

## Ecosystem Delegation

Discover companion skills dynamically within the active workspace runtime (`.agents/`, `.claude/`, `.codex/`, or host skill registry) by skill name without assuming repository paths:

| Task Need | Companion Skill | Handoff Contract |
| :--- | :--- | :--- |
| Remove AI prose tells, tune voice, or run deterministic n-gram/watermark checks | `humanizer` or `de-aigc-skills` | Run **after** `technical-doc-author` locks structure, UIDs, and numbers; preserve all UIDs, metrics, tables, and diagrams. |
| Interactive stakeholder context dump or fresh-reader blind test | `doc-coauthoring` | Use for multi-round discovery or Stage 3 reader testing while keeping `DOC-1..8` schema and abstraction locks intact. |
| Advanced Mermaid types, PlantUML/D2/BPMN rendering, or SVG/PNG export | `markdown-mermaid-writing` or diagram skills (`diagram-skills`, `mermaid-diagram`, `mermaid-architect-guide`, `plantuml-guide`, `excalidraw-diagram-guide`) | Enforce `<= 9` node cap, `<Verb> + <Object>`, Component Contract Table, and strip any decorative H2 emojis. |
| Coding feature EARS specification (`intent -> reqs -> design -> tasks`) | `sdd` | Route here when the user wants repo-local coding task scaffolding rather than `DOC-1..8` engineering documentation. |

## Output Contract

Resolve blocking missing baselines or breaking conflicts in Phase 1/3 before emission. Publish the completed technical document inside a single standalone Markdown code block using an outer fence longer than any inner fence (4 backticks ````` ````markdown ````` whenever the document contains Mermaid or code blocks), with zero preamble or postamble around the block; append only non-blocking unconfirmed stakeholder targets after the block when explicitly requested to deliver a draft scaffold.

## Examples

Input: `"Write an SRS requirement for money transfer using Currency.add() and throwing BalanceError when balance < amount; use UC01."`

Output excerpt inside standalone fence:

````markdown
### 2.1 BR-FIN-01: Non-Negative Balance Preservation
All transfer computations MUST use exact base-10 arithmetic (`0` rounding drift). When `balance < amount`, the system MUST reject the request with business code `ERR-FIN-INSUFFICIENT-BALANCE` and commit `0` state mutations.

### 3.1 UC-TXN-01: Transfer Account Funds
- Main Success Flow: Validates ownership, verifies `balance >= amount`, and settles debit/credit records atomically.
````

## Anti-Examples

| ❌ Avoid | ✅ Prefer | Why |
| :--- | :--- | :--- |
| SRS mentions `Currency.add()`, `BalanceError`, or `ledger_entries` SQL columns | SRS specifies precision invariant (`BR-FIN-01`) and zero-mutation rejection on insufficient balance (`FR-TXN-01`) | Keeps Problem (`WHAT`) free of implementation leakage (`HOW`) |
| `### 3.1 Manage User Accounts (UC01)` | `### 3.1 UC-ACC-01: Provision Customer Account` and `### 3.2 UC-TXN-01: Transfer Account Funds` | Enforces POLA namespacing, heading placement, and atomic `<Verb> + <Object>` goals |
| Single 12-node Mermaid diagram wrapped in 4 subgraphs | Tier 1 System Context (<= 9 nodes) + Tier 2 Event Pipeline (<= 9 nodes) + Component Contract Table | Preserves cognitive load cap; subgraphs do not mask clutter |
| ADR omits negative trade-offs and breaking points to look persuasive | ADR lists >= 3 quantitative trade-off axes, >= 2 disqualified options, negative consequences, and saturation threshold | Prevents costless perfection bias in architecture governance |
| Runbook drops verification/rollback steps and embeds a WAL theory paragraph | Runbook pairs every step with stdout/stderr check, adds rollback for destructive steps, moves theory out | Ensures zero-ambiguity execution under production outage stress |

## Common Issues & Discipline Guardrails

**Violating the letter of these rules is violating the spirit of these rules.** No exceptions when the user supplies tight deadlines, code snippets, flat IDs, or "keep it short" requests.

| Rationalization Under Pressure | Non-Negotiable Reality |
| :--- | :--- |
| "User gave application classes/SQL tables and asked for an SRS in 20 min, so include them for clarity." | Code and table names leak `HOW` into `WHAT`. Translate user-supplied mechanics into technology-agnostic business rules and constraints. |
| "User asked for simple IDs like `UC01` and `FR01` so PMs scan faster." | Flat IDs destroy subsystem boundaries. Keep readable 3-part POLA UIDs (`UC-ACC-01`, `FR-ACC-01`) in `### X.Y [UID]: [Name]` headings. |
| "Leadership wants a persuasive ADR without downsides and 1 diagram with all 12 services." | Hiding trade-offs and breaking points invalidates the ADR. Split diagrams into <= 9-node tiers and publish >= 3 trade-off axes + saturation limits. |
| "ChatOps incident Runbook must be short, so skip verification/rollback and explain WAL for juniors." | Unverified destructive commands cause cascading outages, and theory slows triage. Keep stdout checks + rollback; drop theory essays from `DOC-8`. |

**Red Flags (STOP and fix before output):** code/exception/SQL names in `DOC-1` SRS; `UC01`/`FR01` flat IDs; `"Manage X"` headings; > 9 nodes in one diagram; ADR/SDD/RFC lacking breaking point or >= 2 rejected options; `DOC-8` Runbook lacking verification or destructive-step rollback; fabricated SLO numbers; running an internal multi-agent prose de-AI loop instead of delegating to `humanizer` / `de-aigc-skills`.

## References

- `references/document-types-matrix.md`: Read in Phase 1 and Phase 3 for Diataxis quadrant boundaries, canonical POLA prefix registry, `DOC-1` to `DOC-8` blueprints, RTM, Trade-off Matrix, and Lifecycle Graph.
- `references/visual-and-gate-contract.md`: Read in Phase 3 and Phase 4 when authoring diagrams/tables or verifying the portable 8-gate compliance contract (`G1`–`G8`).
