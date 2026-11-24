---
trigger: glob
globs: "**/*.md, **/*.qmd, **/*.markdown"
description: "Ten universal technical documentation principles, anti-AI prose discipline, 2-tier mechanical quality gates, and pre-export deliverable readiness standards."
---

# Universal Technical Writing and Engineering Documentation Principles

Establishes mandatory engineering documentation rules across Markdown artifacts (`.md`, `.qmd`, `.markdown`) to eliminate LLM writing tells, abstraction leakage, table syntax defects, artificial academic ornamentation, and regression during edits.

## 1. Core Purpose, Scope, and Philosophy

### 1.1. Invariant Contract

This specification acts as a binding technical contract between human engineers and AI agents. Every authored engineering document must satisfy its structural, semantic, and countable syntactic thresholds before handover.

### 1.2. Weak-Model-First Philosophy and Countable Boundaries

Every rule uses deterministic Pass/Fail counts, regex-checkable patterns, and structured identifiers rather than subjective style preferences, ensuring even lightweight models can execute and audit compliance reliably.

### 1.3. Target Genres and Explicit Scope Boundaries

Apply the strict `== 0` mechanical prose gates in Sections 2 through 4 specifically to authored engineering documentation across the **8 industrial genres** below and to export-bound formal deliverables:

| # | Genre | Primary Focus |
| --- | --- | --- |
| 1 | Software / Product Requirements Specification (SRS / PRD) | Problem scope, actors, domain invariants, quantitative acceptance criteria (`WHAT`) |
| 2 | Software / System Design Description (SDD / Arch Spec) | Component topology, layering, data/schema models, interaction protocols (`HOW`) |
| 3 | Architecture Decision Record (ADR) | Technical context, evaluated alternatives, selection rationale, trade-offs, consequences |
| 4 | Engineering Proposal (RFC) | Proposed system changes, migration strategy, design critique before approval |
| 5 | Technical Report / Benchmark / Evaluation | Empirical methodology, environment bounds, measured metrics, variance analysis |
| 6 | Incident Postmortem / Root Cause Analysis (RCA) | Objective timeline, telemetry evidence, root causes, preventive actions |
| 7 | API Specification / Data Schema Contract | Endpoints, payloads, boundary constraints, serialization formats, error codes |
| 8 | Runbook / How-to Guide / SOP | Imperative command sequences, configuration steps, verification, rollback |

Workspace AI instruction files (`*.rule.md`, `agent.md`, `SKILL.md`, and catalog `INDEX.md` files) are **exempt** from these 8-genre prose gates so instruction templates can use checklists, rule references, and bilingual filter quotes cleanly. Additionally, pre-export path constraints never restrict agents from accessing, navigating, linking, or citing files and folders across an active workspace or external paths provided by the user.

## 2. Ten Universal Authoring Principles

### 2.1 [U1]: Purpose and Abstraction Layer Discipline

Maintain strict abstraction boundaries matched to document tier:

1. **Requirements / Conceptual Layer (`WHAT`):** Focus on business goals, domain entities, actors, constraints, and technology-agnostic error messages. Prohibit design leakage (class names, GoF pattern labels, ORM/table DDL, programming-language library methods or exception classes).
2. **Logical / Analytical Layer (`LOGIC`):** Specify language- and vendor-independent domain models, relational schemas, functional dependencies, candidate keys, normal forms, and formal state invariants synchronized cleanly with both conceptual specs and physical implementations.
3. **Physical Design / Implementation Layer (`HOW`):** Document concrete module decomposition, DBMS choices, DDL/trigger mechanics, and interfaces without copying detailed requirements prose verbatim; trace every architectural element back via requirement UIDs.
4. **Technical Report / Benchmark Layer:** Ground claims in test hypotheses, environment parameters, measured numbers, and variance analysis rather than marketing rhetoric or textbook prose.
5. **Postmortem / RCA Layer:** Present objective chronological events, metrics, root causes (5 Whys / Fishbone), and systemic fixes without personal blame or abstract theory.
6. **Zero Textbook Syndrome:** Never insert introductory university methodology lectures or cognitive psychology axioms (such as Miller's $7 \pm 2$, Hick's law, or Conway's law) before tables or diagrams; lead directly with specifications, configurations, and domain analysis.

### 2.2 [U2]: Audience Orientation and Functional Diataxis

1. **Four Diataxis Quadrants:** Classify each document or section into exactly one quadrant: Tutorials (learning-oriented hands-on progression), How-to Guides / Runbooks (task-oriented imperative procedures), Reference (dry, exact parameter/API/schema lookup without commentary), or Explanation / Technical Reports (architecture rationale, trade-offs, and empirical findings).
2. **Quadrant Separation:** Never mix quadrants inside the same heading (do not inject API error lookup tables inside a Tutorial, or architectural philosophy inside a Runbook).
3. **Professional Engineering Voice:** Write as a knowledgeable colleague using active voice (`The gateway validates API tokens before forwarding requests`) and direct imperative mood for procedural instructions (`Initialize the partition`, `Verify the exit code`).

### 2.3 [U3]: Single-Language Integrity and Anti-AI Tell Elimination

1. **Single-Language Purity:** Within prose written in a target language (such as Vietnamese), forbid appending redundant English translations inside parentheses right after translated terms (forbid `"Tổng quan (Overview)"`, `"Yêu cầu (Requirement)"`, `"Phân hệ (Subsystem)"`, `"Cấu hình (Configuration)"`; write `"Tổng quan"`, `"Yêu cầu"`, `"Phân hệ"`, `"Cấu hình"`). Exceptions apply strictly to dedicated bilingual glossary columns and untranslatable international proper nouns (`Kafka`, `Docker`, `PostgreSQL`, `gRPC`, `OAuth 2.0`).
2. **Zero Em-Dash Punctuation:** Prohibit em-dashes (`"—"`) and double hyphens (`"--"`) used as sentence-break punctuation outside inline code spans and fenced code blocks (`== 0`). Split long thoughts cleanly with periods, commas, or colons. Table delimiters (`| --- |`), CLI flags (`--verbose`), and verbatim external publication titles wrapped in inline backticks (such as `Reference Standard XYZ — 2nd Edition`) are exempt.
3. **Zero Fake Contrasts:** Prohibit template contrasts (`"Not only X, but also Y"`, `"Không chỉ là X mà còn là Y"`, `"Không đơn thuần là X mà là Y"`). State concrete capabilities and measurements directly.
4. **Zero Forced Triplets:** Prohibit rhythmic three-adjective or three-clause padding (`"scalable, robust, and reliable"`, `"nhanh chóng, linh hoạt và chính xác"`, `"an toàn, hiệu quả và đáng tin cậy"`). Pick one precise engineering term or present a quantitative test table.
5. **Zero Mechanical Bold-Prefix Bullet Lists:** Do not repeat `- **Label:** Sentence.` across every bullet in document body prose. Convert repeating attributes into compact Markdown tables, numbered steps, or fluent technical sentences.
6. **Zero Fractal Repetition:** State each technical fact or requirement once in its canonical location; never write redundant intro summaries, restate them mid-section, and repeat them again in closing recaps.
7. **Three-Tier AI Vocabulary Filter:** Enforce strict lexical thresholds across generated prose:
   - Tier 1 (`== 0` occurrences): `"delve"`, `"tapestry"`, `"landscape"` (metaphorical), `"pivotal"`, `"foster"`, `"robust"` (vague metaphorical), `"leverage"` (verb), `"seamless"`, `"groundbreaking"`, `"game-changer"`, `"bức tranh tổng thể"`, `"đòn bẩy"`, `"toàn diện và sâu sắc"`, `"trực quan sinh động"`, `"chìa khóa vàng"`.
   - Tier 2 (banned filler phrases): `"như chúng ta đã biết"`, `"để đảm bảo tính toàn diện"`, `"dưới đây là nội dung chi tiết"`, `"tóm lại hệ thống sẽ mang lại"`, `"đóng vai trò then chốt"`, `"là giải pháp tối ưu hàng đầu"`, `"as we all know"`, `"in order to ensure comprehensiveness"`, `"below are the detailed contents"`.
   - Tier 3 (abstract connector density `<= 2` per 500 words): `"nhằm mục đích"`, `"qua đó"`, `"từ đó"`, `"thông qua việc"`, `"notably"`, `"furthermore"`.
8. **Direct RFC 2119 Keywords:** Apply normative keywords (`"MUST"` / `"BẮT BUỘC"`, `"MUST NOT"` / `"KHÔNG ĐƯỢC PHÉP"`, `"SHOULD"` / `"NÊN"`, `"OPTIONAL"` / `"TÙY CHỌN"`) directly inside rule statements without meta-explanations defining what RFC 2119 means.

### 2.4 [U4]: Structured Namespaced Identifiers (POLA)

1. **UID Syntax and Header Placement:** Place traceable UIDs immediately after section numbers separated by a colon (`### X.Y [UID]: [Standard Title]`). Never append UIDs in trailing parentheses (`### 3.1 Instance Balancing (REQ-NET-01)`).
2. **Namespaced Prefixes:** Follow `[TYPE]-[DOMAIN/SUBSYS]-[NN]` (`BR-[DOMAIN]-[NN]`, `REQ-[SUBSYS]-[NN]`, `UC-[SUBSYS]-[NN]`, `US-[SUBSYS]-[NN]`, `CMP-[SUBSYS]-[NN]`, `ADR-[NNN]`, `RFC-[NNN]`, `HYP-[TOPIC]-[NN]`, `FIND-[TOPIC]-[NN]`, `REC-[TOPIC]-[NN]`, `MET-[TOPIC]-[NN]`, `INC-[DATE]-[NN]`, `ACT-[TOPIC]-[NN]`, `FAIL-[TOPIC]-[NN]`). Prohibit flat un-namespaced IDs (`ID01`, `REQ01`, `UC01`, `RULE01`, `FIND01`).
3. **Concise Sub-Table Headers:** Omit redundant parent-category words inside sub-table column headers (write `| Parameter | Type | Required | Constraints | Default |`, never `| API Parameter Name | Parameter Data Type |`).

### 2.5 [U5]: Multi-Layer Syntax Defense and Markdown Engineering

1. **Table Pipe and Math Escaping:** Never place bare `|` characters inside LaTeX math inside Markdown tables (`== 0`); use `\lvert ... \rvert`, `\lVert ... \rVert`, or `\mid`. Escape literal pipes inside table text or inline code cells as `\|` (never use numeric HTML pipe entities, maintaining parity with `markdown-formatting-and-layout.rule.md`).
2. **Code Fences, Clean Escapes, and Heading Characters:** Write opening fence language tags directly after the three backticks with zero space (such as `mermaid`, `json`, or `bash` attached immediately to the opening fence), leave `0` raw escaped control sequences (`\n\n`, `\r\n`, `\t`), and write raw `&`, `<`, `>` in headings (`# API Design & Data Gateway`) rather than HTML entities (`&amp;`, `&lt;`, `&gt;`) that break TOC anchor slugs.
3. **GFM Callout Discipline:** Use only standard GitHub callout tags (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`), never nested and never placed back-to-back without intervening content.

### 2.6 [U6]: Tiered Visuals, Cross-Modal Parity, and Goal-Oriented Modeling

1. **Two-Tier Visual Decomposition:** Separate complex system visuals into Level 1 (System Context / High-Level Dataflow) and Level 2 (Subsystem Internals / Sequences / State Transitions / Root-Cause Trees).
2. **Cognitive Load Cap (`<= 9` Nodes):** Limit every single diagram to at most **9** nodes; group or decompose larger models into hierarchical sub-diagrams.
3. **Goal-Oriented Behavioral Naming:** Name every use case or workflow step using `<Action Verb> + <Direct Object>` delivering measurable value. Prohibit CRUD catch-all bundles (`"Manage X"`, `"Quản lý..."`) and UI button clicks (`"Click Save"`, `"Open Edit Screen"`).
4. **Semantic Relationship Accuracy:** Never connect mutually exclusive paths with optional extension (`<<extend>>`) edges, and never model sequential steps using inclusion (`<<include>>`) arrows.
5. **100% Diagram-to-Prose Parity:** Every node, branch, and UID in a diagram must have corresponding text specification (`0` phantom nodes), without forcing artificial 1:1 structural-to-behavioral symmetry.
6. **Diagram Utility and Native Mermaid:** Create diagrams only to resolve concrete structural, permission, state, or failure-mode complexity (never menu-mirroring hub-and-spoke charts), and author maintained doc diagrams in native Mermaid fenced blocks (`flowchart TD`, `sequenceDiagram`, `stateDiagram-v2`, `erDiagram`).

### 2.7 [U7]: Quantitative Verification and Traceability Closure

1. **Measurable Thresholds:** Specify quantitative NFRs, SLOs, benchmarks, and acceptance criteria with explicit tolerances (for example, `P99 latency <= 150ms at 2,000 RPS`, `>= 99.95% availability over 90 days`, `0.00 reconciliation variance`, `RTO <= 30s`, `RPO = 0`). Prohibit qualitative adjectives (`"fast"`, `"smooth"`, `"user-friendly"`, `"optimal"`, `"nhanh"`, `"mượt mà"`, `"bảo mật cao"`, `"tối ưu"`).
2. **Closed Bidirectional Traceability:** Maintain 100% closed links (`Business Goal <-> Business Rule <-> Functional Requirement <-> Test Case` for specs; `Hypothesis <-> Environment <-> Measured Metric <-> Variance <-> Conclusion` for reports; `Alert <-> Timeline <-> Evidence <-> Root Cause <-> Action Item` for RCAs) with `0` orphan items.

### 2.8 [U8]: Technical Thesis, Proportional Rigor, and Trade-Off Realism

1. **Technical Thesis Statement:** Open architectural proposals, RFCs, whitepapers, and system surveys with a concise thesis naming the chosen design, target optimization goal, load envelope, and explicit boundary limits.
2. **Proportional Rigor:** Reserve formal predicate logic and algebraic proofs (IEEE/ACM style) for genuinely complex domains (cryptography, distributed consensus, formal verification, risk modeling); express straightforward business rules directly in plain assertions or numeric tables (`0` spurious precision).
3. **Trade-Off Realism and Breaking Point:** Present every architectural solution alongside at least **3** realistic trade-off axes (latency vs. memory/bandwidth, consistency vs. availability, velocity vs. operational complexity) and explicitly state the load/capacity **Breaking Point** where performance degrades and redesign is required.

### 2.9 [U9]: Document Self-Containment, Neutral Third-Person, and Context Deduplication

1. **Self-Contained Abstraction Scope:** Satisfy the document's declared abstraction scope cleanly without lazy deferrals inside body prose (`0` sentences delegating core definitions to external specs; keep formal external citations isolated in `## References` when required). This governs specification prose only and never blocks cross-folder links inside workspace READMEs, Runbooks, or agent workflows.
2. **Objective Third-Person Voice:** Use concrete technical subjects (`The system`, `The service`, `The operator`, `Hệ thống`), imperative mood for Runbooks/SOPs, `0` first/second-person pronouns (`"we"`, `"us"`, `"our"`, `"I"`, `"you"`, `"chúng tôi"`, `"chúng ta"`, `"tôi"`, `"bạn"`, `"quý vị"`), and `0` subjective praise words (`"fantastic"`, `"superior"`, `"convenient"`, `"tuyệt vời"`, `"ưu việt"`, `"hoàn hảo"`).
3. **Static Context Inheritance and Zero Preambles:** Subsections inherit parent context automatically; begin every subsection directly with its entity, specification, constraint, or table (`0` throat-clearing preambles or parent-goal recaps).

### 2.10 [U10]: End-to-End Impact Analysis, Anti-Regression, and Value Preservation

1. **Blast Radius Audit:** Trace downstream and upstream dependencies across business goals, requirements, data schemas, diagrams, load limits, and test plans before editing existing technical specs.
2. **Value Preservation:** Retain proven optimizations, strict tolerances, and working algorithms (`0` silent standard lowering or logic regressions).
3. **Deliberative Alignment Gate:** When edits introduce major architectural trade-offs or cross-component risks, pause, compare options in a trade-off table, and align with the user before applying changes.

## 3. Comprehensive Enforcement Reference Matrix

| Control Area | Prohibited AI Anti-Pattern | Required Standard | Countable Gate (Pass/Fail) |
| --- | --- | --- | --- |
| Abstraction boundaries | Leaking code methods, library classes, or physical DDL into SRS/PRD | Describe technology-agnostic behavior; separate `WHAT`, `LOGIC`, and `HOW` | `0` downstream implementation keywords in high-level specs |
| Proportional rigor | Spurious first-order logic or equations for trivial rules | Plain technical assertions or numeric tables; formal math only when warranted | `0` passages with decorative formal logic for trivial rules |
| Zero textbook syndrome | Lecturing Miller's law or textbook axioms before tables | Lead with diagrams, data tables, and concrete parameters | `0` methodology lecture paragraphs |
| Diataxis & active voice | Mixing error tables into tutorials; vague passive voice | Strict single-quadrant focus; active subjects or imperative SOPs | `100%` single-quadrant alignment; `0` actorless passive rules |
| Namespaced UIDs | Flat linear IDs (`ID01`, `REQ01`, `UC01`, `FIND01`) | Hierarchical subsystem prefixes (`REQ-NET-01`, `ADR-004`) | `0` un-namespaced flat UIDs |
| Heading UID position | Trailing parenthetical UIDs (`Title (REQ-AUTH-01)`) | Prefix after section number (`### 3.1 REQ-AUTH-01: Title`) | `100%` header UIDs match prefix syntax |
| Goal-oriented modeling | Catch-all CRUD nodes (`"Manage X"`, `"Quản lý..."`) | `<Action Verb> + <Direct Object>` delivering actor value | `0` `"Manage..."` or `"Quản lý..."` use cases/nodes |
| Diagram relationships | Using `<<extend>>` for mutually exclusive flows | Separate exclusive branches; reserve extensions for optional hooks | `0` extension edges bridging exclusive branches |
| Diagram-prose parity | Undocumented phantom nodes added to fill diagrams | Every visual node/UID backed by body specification | `0` phantom diagram elements |
| Structural-behavioral split | Forcing rigid 1:1 module-to-flow mirroring | Allow user journeys to span multiple structural components | `0` artificial 1:1 structural-behavioral couplings |
| Branching semantics | Turning alternative flows into CRUD menu jumps | Alternative flows reach the same goal or handle recovery | `0` CRUD navigation menus inside flow branches |
| Single-language purity | Parenthetical translation echo (`"Tổng quan (Overview)"`) | Clean target-language terms; separate glossary columns if needed | `0` redundant parenthetical English echoes |
| Em-dash punctuation | Sentence-break em-dashes or `--` outside code | Periods, commas, colons; inline code for verbatim titles | `0` unquoted em-dashes or `--` breaks in prose |
| Heading HTML entities | Escaping `&`, `<`, `>` as `&amp;`, `&lt;`, `&gt;` in `#` headers | Raw characters (`# API Design & Data Gateway`) | `0` HTML entities inside heading lines |
| Fake contrasts | `"Not only X, but also Y"` / `"Không chỉ..."` fluff | Direct factual statement with measurements | `0` fake contrast clauses |
| Forced triplets | Rhythmic 3-adjective padding (`"fast, robust, seamless"`) | Single precise term or quantitative metric table | `0` decorative three-adjective triplets |
| Bold-prefix lists | Repeating `- **Label:** Sentence.` on every bullet | Compact tables, numbered procedures, or plain prose | `0` mechanical bold-prefix body bullets |
| Tier 1 AI vocabulary | `"delve"`, `"tapestry"`, `"pivotal"`, `"bức tranh tổng thể"`, `"đòn bẩy"` | Exact domain terms (`parse`, `schema`, `latency`, `throughput`) | `0` Tier 1 banned tokens |
| Table pipes & math | Bare `\|` pipes inside LaTeX math or numeric HTML pipe entities in tables | `\lvert`, `\rvert`, `\mid` in math; `\\|` in table cells | `0` bare math pipes and `0` numeric HTML pipe entities |
| Code fences & escapes | Spaces after opening backticks or raw `\n\n`, `\t` text | Immediate language tag (`json`, `mermaid`) and clean whitespace | `0` spaced fence tags; `0` raw escape artifacts |
| Sub-table header brevity | Repeating parent keyword in every column header | Concise headers (`ID`, `Action`, `Owner`, `Due`, `Status`) | `0` parent-category word repetitions in headers |
| UI button diagrams | Flow steps named `"Click Save"`, `"Enter Password"` | Domain goals (`"Persist Transaction"`, `"Verify Identity"`) | `0` raw UI click steps in architecture/flow diagrams |
| Quantitative NFRs | Qualitative claims (`"fast"`, `"nhanh"`, `"tối ưu"`) | Numeric bounds and tolerances (`P95 <= 200ms at 1,000 RPS`) | `100%` quantitative NFRs and acceptance criteria |
| Trade-off & limits | Claiming a universal solution with zero downsides | Minimum 3 trade-off axes plus explicit Breaking Point | `0` architecture/RFC docs lacking trade-offs & limits |
| Context deduplication | Restating parent system overview in every subsection | Static context inheritance; direct technical entry | `0` parent-context recap sentences in child sections |
| Perspective & neutrality | 1st/2nd person (`"we"`, `"you"`, `"chúng tôi"`) or praise words | Named 3rd-person systems (`"The service"`); Pass/Fail facts | `0` 1st/2nd pronouns and `0` subjective adjectives |
| Self-containment | Lazy `"See Document X"` deferrals inside spec body | Complete abstraction scope; isolate citations in `## References` | `0` lazy external-doc deferrals in spec body |
| Anti-regression & parity | Patching locally and breaking downstream/existing invariants | End-to-end blast-radius check preserving proven optimizations | `0` logic regressions; `100%` baseline value preserved |

## 4. Two-Tier Adaptive Quality Gates and Deliverable Readiness

Every engineering document created, updated, or refactored must pass all applicable gates below before handover.

### 4.1. Tier 1: Ten Universal Core Gates

- [ ] Gate U1 (Functional Purpose & Diataxis Consistency): Document conforms strictly to 1 Diataxis quadrant; `0` textbook lectures or methodology justifications. (Pass/Fail)
- [ ] Gate U2 (Single-Language Linguistic Integrity): `0` parenthetical English echoes immediately after translated terms in headings or prose. (Pass/Fail)
- [ ] Gate U3 (Anti-AI Stylistic Filtration): `0` unquoted em-dashes or `--` sentence breaks; `0` forced triplets; `0` fake contrasts; `0` Tier 1 AI vocabulary; `0` mechanical bold-prefix bullets in prose. (Pass/Fail)
- [ ] Gate U4 (Table Delimiter & Math Integrity): `0` bare `|` inside table LaTeX math (use `\lvert`, `\rvert`, `\mid`) and `0` numeric HTML pipe entities (use `\|` for literal pipes). (Pass/Fail)
- [ ] Gate U5 (Code Fence, Callout & Heading Hygiene): `0` spaces after opening backticks; `0` raw escape artifacts; `0` HTML entities in headings; compliant GFM callouts. (Pass/Fail)
- [ ] Gate U6 (Thesis, Proportional Rigor & Trade-Off Realism): Explicit thesis upfront; `0` decorative predicate logic on simple rules; `>= 3` realistic trade-offs and explicit load Breaking Point where applicable. (Pass/Fail)
- [ ] Gate U7 (Self-Containment & Isolated References): Complete abstraction coverage; `0` lazy external-doc deferrals in body prose; formal citations isolated in `## References` when required. (Pass/Fail)
- [ ] Gate U8 (Neutral 3rd-Person Perspective): `0` first/second-person pronouns (`"we"`, `"us"`, `"our"`, `"you"`, `"chúng tôi"`, `"chúng ta"`, `"tôi"`, `"bạn"`, `"quý vị"`) and `0` subjective praise adjectives (`"tuyệt vời"`, `"fantastic"`, `"superior"`). (Pass/Fail)
- [ ] Gate U9 (Context Deduplication & Direct Entry): Child subsections inherit parent context (`0` macro-context recaps) and open directly with technical entities, parameters, or tables. (Pass/Fail)
- [ ] Gate U10 (End-to-End Impact & Anti-Regression): Full dependency blast-radius checked; `100%` existing optimal baselines preserved; `0` broken references or logic regressions. (Pass/Fail)

### 4.2. Tier 2: Four Context-Adaptive Extension Gates

- [ ] Gate E1 (Abstraction Layer & Scope Purity): Requirements (`WHAT`) contain `0` code/DDL keywords; Logical models (`LOGIC`) stay vendor-neutral; Design (`HOW`) traces back to UIDs without repeating requirements; Reports back every claim with data; Postmortems contain `0` personal blame. (Pass/Fail)
- [ ] Gate E2 (Namespaced UID Syntax & POLA): `100%` traceable headers match `### X.Y [UID]: [Title]` with domain-scoped prefixes (`REQ-`, `CMP-`, `FIND-`, `REC-`, `INC-`, `ADR-`); `0` flat IDs (`ID01`, `REQ01`, `UC01`). (Pass/Fail)
- [ ] Gate E3 (Tiered Visuals, Semantics & Cross-Modal Parity): Two-tier diagram split; `<= 9` nodes per diagram; `100%` `<Action Verb> + <Direct Object>` naming (`0` `"Manage..."` / `"Quản lý..."` CRUD bundles); `0` invalid extension edges; `0` phantom diagram elements; `0` menu-clone diagrams. (Pass/Fail)
- [ ] Gate E4 (Quantitative Evidence & Traceability Closure): `100%` NFRs, SLOs, and test conclusions carry numeric thresholds with tolerances; `100%` closed bidirectional traceability (`0` orphan requirements, findings, or actions). (Pass/Fail)

### 4.3. Deliverable Readiness and Pre-Export Hygiene

Before finalizing any formal report or external deliverable for Word, PDF, or HTML export, verify these 3 release checks:

1. **Zero Leftover Placeholders:** Scan the full document for unfilled markers (`TODO`, `TBD`, media placeholders, internal export reminders); match count must equal `0`.
2. **Zero Personal Workstation Paths in Final Submitted Reports:** Confirm `0` developer machine paths (such as `C:\Users\...` or local home-drive paths) and `0` internal chat-channel pointers remain inside formal submitted report prose. This restriction applies strictly to final submitted deliverables and never restricts agents from accessing, navigating, linking, or citing valid workspace files, Runbook/SOP runtime filesystem paths, or chat pointers during active engineering work.
3. **Media Existence and Visual Uniqueness:** Verify `100%` of referenced figures and evidence screenshots exist at their target paths and confirm no image asset is accidentally duplicated across distinct test cases, rules, or sections.
