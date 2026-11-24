---
trigger: always_on
description: "Role-based 4-tier knowledge grounding hierarchy, dynamic multi-branch scope resolution, external source ingestion protocol, and strict 3-channel source attribution and citation parity."
---

# Knowledge Grounding & Source Attribution

Establishes how agents discover, rank, verify, ingest, and cite authoritative knowledge without relying on hardcoded paths or leaking internal notes into formal deliverables.

## 1. Role-Defined 4-Tier Grounding Hierarchy

Workspace directory structures evolve continuously. Discover paths dynamically by listing the workspace root and active working directory at task start, then map existing documents to these 4 functional tiers before relying on any source:

| Tier | Functional Role | Authority & Obligations |
| --- | --- | --- |
| **Tier 1: Primary Mandate** | Assignment specs, project charters, rubrics, regulatory mandates, grading or acceptance criteria | Highest structural and compliance authority; strictly **read-only**; never omit a mandatory Tier 1 deliverable or criterion |
| **Tier 2: Requirements Authority** | Project requirements specification (SRS/PRD, use cases, business rules) | Highest authority for domain rules, formulas, scope, and terminology; writable under approved decisions (no separate decision ledger); if missing, draft from seed material + Tier 3, then supersede seed material |
| **Tier 3: Technical Standards** | Shared workspace reference library, engineering standards, textbooks, exemplary templates | Benchmarks architecture, formatting, and methodology; strictly **read-only**; never overrides Tier 2 business rules |
| **Tier 4: Project Deliverables** | Analysis, design models, schemas, source code, scripts, reports, and automated test suites | Writable under approved changes; must maintain bidirectional traceability back to Tiers 1 and 2 |

When Tier 2 is ambiguous or silent on a business rule, formula, or threshold, stop and ask per `core-collaboration-charter.rule.md` [R2], then record the user's decision into Tier 2.

**Implementation vs. Documentation Drift Protocol:** Whenever executable artifacts (source code, SQL schemas, scripts, or runtime configs) diverge from upstream requirements, models, diagrams, or report tables, inspect both, report the exact element delta, and ask the user which artifact is authoritative before synchronizing.

## 2. Dynamic Multi-Scope Resolution & Decoupled Traceability

1. **Unrestricted Workspace Discovery (`ACTIVE_SCOPE`):** Discover and connect freely across all relevant workspace directories, sibling docs, and user-provided external paths without artificial path restrictions. Infer the active working directory, branch, or service module from the target file path; when no path is given and multiple scopes exist, list candidates and ask once.
2. **Local-Over-Global Cascade:** Search in strict priority order:
   - *Level 1 (Local):* Active scope's documentation subtree (`docs/` or equivalent).
   - *Level 2 (Shared):* Workspace-level shared reference directory (`reference/` or equivalent), consulting other sibling scopes only as a last resort and explicitly tagging any sibling reference with its scope in chat.
3. **Dynamic Path Verification:** Treat remembered paths from earlier turns as unverified hints. Re-list or search the directory tree at session start and whenever a path fails to resolve.
4. **Draft vs. Finalized Binary Hygiene:** Inspect timestamps and file contents rather than inferring finality from folder names alone; flag unresolved placeholders or stale drafts explicitly, and never assume an editable source draft matches a compiled binary deliverable (`.pdf`, `.docx`).
5. **Decoupled Traceability:** Never hardcode identifier prefixes (`REQ-`, `UC-`, `BR-`). Discover and enforce whatever identifier convention Tier 2 defines.

## 3. External Knowledge Grounding & Ingestion Gate

1. **Resolution Sequence:** When Tiers 1 and 3 lack required domain standards or methodology, consult authoritative primary literature (official standards like IEEE/ISO/RFC, peer-reviewed texts, canonical specifications) rather than unverified blog snippets, and cross-check critical claims across at least **2** credible sources.
2. **Persistent Ingestion Proposal:** When an external standard will serve as a recurring baseline across multiple deliverables, propose local ingestion in chat (providing title, author/body, year, DOI/ISBN/URL, and target shared folder such as `reference/` or `standards/`) so subsequent tasks ground locally.

## 4. Three-Channel Source Attribution Discipline

Every source reference belongs strictly to **1 of 3 separate channels**. Never mix formats across channels.

| Channel | Allowed Location | Required Format & Rules |
| --- | --- | --- |
| **Chat Pointer** | Chat responses only | Informal `file path (section or page)` or URL accompanying every factual or numeric claim; NEVER copy internal repo paths or scope paths into formal deliverables |
| **Inference & Notes** | Chat responses only | Agent derivations, assumptions, and trade-offs explicitly labeled `Inference` or `Note`; NEVER combine source facts and agent inferences in the same sentence without explicit markers |
| **Deliverable Citation** | Target deliverable's bibliography section only | Formal citation style (APA current edition unless the deliverable establishes another style); body text uses only the document's in-text citation marker |

### Deliverable Citation Hygiene & Verification

1. Locate the deliverable's bibliography section by reading the document; if absent, ask where it belongs before adding entries.
2. Cite the original primary source; if only a secondary summary was verified, state so in chat and cite the summary as read.
3. Reuse existing bibliography entries instead of duplicating sources. Never fabricate missing bibliographic fields (edition, chapter, page, year, publisher, DOI/URL); flag missing fields to the user first.
4. **Zero-Orphan Parity Check:** Verify before handover that the count of in-text markers lacking bibliography entries equals **0** and the count of unused bibliography entries equals **0** (retain search commands and counts per R3).

## 5. Rationalization Blockers & Red Flags

| Rationalization Under Pressure | Mandatory Counter-Rule |
| --- | --- |
| "Sibling scope `sibling-scope/notes.md` has a concrete number, so use it and link the file path in the spec." | Sibling scope notes are non-authoritative when primary Tier 2 is silent, and repo paths MUST NOT appear inside deliverables. Flag the conflict in chat and ask the user. |
| "Put a `[TBD: e.g., 15-60 min]` conjecture inside the spec text so stakeholders see an estimate." | Unconfirmed numbers are conjectures (R6) and must stay out of deliverables until confirmed. Present options in chat instead. |

**Red Flags:** relative repo paths (`sibling-scope/notes.md`, `../reference/`) appearing inside SRS/SDD prose; blending source facts and agent guesses into one unmarked sentence; bibliography entries not cited in body text.
