---
description: "Portable C4/diagram mapping across DOC-1 to DOC-8, 9-node cognitive load limits, goal-oriented modeling parity, safe table math pipes, and the 8-gate verification contract."
version: "4.0.0"
---

# Portable Visual Modeling & Quality Gate Contract

Self-contained modeling boundaries and verification gates for `technical-doc-author` across any host workspace. When active workspace rules define stricter physical Markdown or modeling standards, workspace rules take precedence on local formatting. For advanced Mermaid diagram syntax, PlantUML/D2/BPMN rendering, or SVG export, delegate to `markdown-mermaid-writing` or specialized diagram skills (`diagram-skills`, `mermaid-diagram`, `mermaid-architect-guide`, `plantuml-guide`, `excalidraw-diagram-guide`) while keeping all constraints below intact.

## 1. C4 Abstraction & Diagram Mapping by Archetype

| Archetype | Allowed C4 Level | Recommended Diagram Types | Strict Abstraction Prohibition |
| :--- | :---: | :--- | :--- |
| `DOC-1` (SRS / PRD) | Level 1 only | System Context, Goal Workflow | Level 4 class diagrams, method signatures, and DB table ERDs are prohibited. |
| `DOC-2` (SDD / Arch Spec) | Level 1 to 3 | Container Topology, Sequence, Statechart, ERD, Data Pipeline | Never copy SRS requirement prose; link nodes to `FR-`/`BR-` UIDs. |
| `DOC-3` (ADR) | Level 1 to 2 | Focused Option Comparison or Container Delta | Do not exceed 9 nodes when contrasting current vs target topology. |
| `DOC-4` (RFC) | Level 1 to 2 | Proposed Topology, Migration Sequence, Rollout Flow | Include migration/deprecation paths; no decorative UI wireframes. |
| `DOC-5` (Tech Report) | Level 2 (Testbed) | Benchmark Harness Topology, Data Pipeline (`flowchart LR`) | Hardware/network topology must match reported test parameters 1:1. |
| `DOC-6` (Postmortem / RCA) | N/A | Incident Fault Propagation Tree, Chronology Flow | Map strictly to observed UTC timestamps and systemic safeguards. |
| `DOC-7` (API Spec) | Level 2 to 3 | Protocol Handshake (`sequenceDiagram`), Resource Statechart | Show HTTP verbs, status codes, and contract boundaries explicitly. |
| `DOC-8` (Runbook / SOP) | N/A | Failover / Rollback Decision Flow (optional) | Keep diagrams strictly operational; never embed tutorial theory. |

## 2. Two-Tier Decomposition & Cognitive Load Rules

1. **Hard 9-Node Ceiling**: A single diagram MUST contain **<= 9 nodes**. Subgraphs, swimlanes, or nested containers do NOT exempt a diagram from the 9-node limit.
2. **Two-Tier Split**: When a system or flow exceeds 9 components, decompose into:
   - **Tier 1 (Context / Macro View, <= 9 nodes)**: External actors, ingress gateway, primary service containers, and primary datastores.
   - **Tier 2 (Subsystem / Micro View, <= 9 nodes)**: Internal pipeline stages, protocol sequence, or entity state transitions for one focused subsystem.
3. **Viewport Fit**: Diagrams must render cleanly without horizontal scroll clutter.

## 3. Modeling Semantics & Cross-Modal Parity

1. **Goal-Oriented Entity Naming**: Format behavioral nodes and use cases as `<Active Verb> + <Direct Object>` (e.g., `Settle Account Ledger`, `Validate Security Token`).
2. **Zero CRUD / God Bundles**: Decompose catch-all `"Manage [Entity]"` or `"Quản lý [Thực thể]"` operations into distinct atomic goals. Count of `"Manage..."` entities MUST equal 0.
3. **Zero UI Micro-Steps**: Never model button clicks or field typing (`Click Submit`, `Open Settings Modal`) as architectural workflow nodes.
4. **Relationship Semantics**:
   - `<<include>>`: Unconditional mandatory sub-goal required for the base goal to complete (never sequential steps).
   - `<<extend>>`: Optional conditional extension at a defined extension point (never mutually exclusive branches; model exclusive branches as separate paths).
5. **Static vs Dynamic Decoupling**: Do not force mechanical 1:1 symmetry between N static containers and N dynamic workflows. For single-actor or batch tools, skip decorative actor-to-bubble use-case diagrams in favor of `flowchart TD` or `stateDiagram-v2`.
6. **Cross-Modal Parity (Zero Phantom Entities)**: 100% of diagram nodes and UIDs MUST have matching specification sections in the document body, and every specified component/goal must match diagram terminology.
7. **Mandatory Component Contract Table**: Place a structured table immediately after every architecture or pipeline diagram:

| Node / Component | Technology / Protocol | Operational Responsibility | Primary Failure Mode |
| :--- | :--- | :--- | :--- |
| Ingress Gateway | Envoy / TLS 1.3 | Rate limiting (`REQ-NET-01`), token offload | `HTTP 503` on upstream pool exhaustion |
| Ledger Service | gRPC / HTTP/2 | Idempotent transaction settlement (`FR-WAL-02`) | Backpressure rejection at queue saturation |

## 4. Portable Markdown, Prose & Table Safety

1. **Pipe Protection in Table Math & Code Spans**: Never place bare unescaped pipe characters inside inline LaTeX math or inline code spans inside Markdown table cells (e.g., union types or absolute values). Use TeX macros `\lvert x \rvert`, `\lVert v \rVert`, `\mid`, or escaped `\|` (never HTML entity `&#124;`).
2. **Fence, Heading & Callout Hygiene**:
   - Open code and Mermaid fences cleanly with zero space after backticks (` ```mermaid `), use 4+ outer backticks when enclosing documents that themselves contain 3-backtick blocks, and strip trailing raw escape literals (`\n\n`, `\t`).
   - Write raw `&`, `<`, `>` in headings (never `&amp;`, `&lt;`, `&gt;` which break TOC anchor slugs).
   - Use standard GFM callouts (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`) with zero nesting and zero consecutive callout blocks.
   - Use compact 3-hyphen table delimiters (`| --- |`, `| :--- |`, `| :---: |`, or `| ---: |`), omit thematic-break `---` lines from body prose, omit em-dash (`—`) punctuation outside code spans, and omit decorative emojis from technical headings and lists.

## 5. Portable 8-Gate Verification Contract (`G1`–`G8`)

Verify every finished document against all 8 gates before delivery:

| Gate | Requirement | Mechanical Pass Criterion |
| :---: | :--- | :--- |
| **G1** | Diataxis Isolation & Zero Textbook | 100% of sections align to 1 declared Diataxis intent (no theory lectures in SOPs or API schemas); count of methodological textbook preambles = 0. |
| **G2** | Abstraction Layer Purity | SRS contains 0 code methods, exception classes, GoF patterns, or SQL schemas; SDD cites `REQ-`/`BR-` UIDs instead of copying SRS prose; Postmortem has 0 personal blame. |
| **G3** | POLA UID & Context Inheritance | 100% traceable headings match `### X.Y [PREFIX]-[DOMAIN]-[NN]: [Title]`; count of flat IDs (`UC01`, `FR01`, `ID01`) and trailing `(UID)` headings = 0; 0 parent-context rehashes in sub-sections. |
| **G4** | Thesis, Trade-Offs & Breaking Point | `DOC-2`/`3`/`4`/`5` include an explicit thesis statement, >= 3 concrete trade-off axes, >= 2 disqualified alternatives (`DOC-3`/`4`), and a quantitative Breaking Point. |
| **G5** | Visual Cap, Goal Naming & Parity | Every diagram has <= 9 nodes (even with subgraphs); 0 `"Manage..."` CRUD bundles; 0 phantom nodes lacking body text; Component Contract Table follows every architecture/pipeline diagram. |
| **G6** | Quantitative Closure & Traceability | 100% of NFRs, SLOs, and benchmarks carry verified numeric thresholds with tolerances (0 fabricated baselines); 0 orphaned requirements, findings, or actions; every `DOC-8` step carries a stdout/stderr check and every destructive step carries an explicit rollback. |
| **G7** | Monolingual, 3rd-Person & Self-Contained | 0 redundant bilingual glosses (`Term (Dịch)`); 0 first/second-person pronouns (`we`, `our`, `you`); 0 deflecting body links (`refer to Doc X`); external refs isolated in `## References` only if requested. |
| **G8** | Markdown & Table Hygiene | 0 bare `\|` (unescaped pipe) in table LaTeX math or code spans; 0 HTML entities (`&#124;`, `&amp;`); 0 spaced code fences; 0 thematic-break `---` lines in body text; 0 em-dash punctuation outside code spans; 0 nested/consecutive callouts or decorative heading emojis. |

For final prose AI-tell scrubbing (faux contrasts, forced triads, stock AI words) or n-gram/watermark checks, hand off the gate-verified draft to `humanizer` or `de-aigc-skills`.
