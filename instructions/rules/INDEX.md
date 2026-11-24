---
name: rules-index
description: "Index, authority hierarchy, lifecycle state, and trust classification for workspace rules under instructions/rules/ (active, archive). Read to discover active governance invariants and archived rule history."
version: 1.4.0
tags: [rules, index, tiers, lifecycle, governance, constraints, standards]
metadata:
  author: "directive"
  scope: "All active and archived rule specifications under instructions/rules/"
---

# Rules Index

Catalog, lifecycle state, authority hierarchy, and source-trust classification for workspace rules under `instructions/rules/`. Canonical definitions of the 6-tier trust scale live in [README.md](../../README.md).

## Lifecycle State & Source Trust Overview

| Lifecycle State | Focus & Provenance | Tier | Count | Notes |
| --- | --- | --- | --- | --- |
| [`active/`](active/) | Maintained in-house engineering, formatting, and collaboration governance rules | `Tier 5` | 7 rules | Operational Role: Workspace Governance; eligible for `.agents/rules/` mirroring |
| [`archive/`](archive/) | Retired domain-specific rules kept for historical reference | `Tier 6` | 2 rules | Historical reference only; excluded from active precedence and scaffolding |

## Rule Catalog by State

### Active Rules

| Rule | Scope & Purpose | Precedence | Summary |
| --- | --- | --- | --- |
| [`clean-engineering-and-testing`](active/clean-engineering-and-testing.rule.md) | Code Quality & Testing | Priority 5 | Micro-unit inside-out delivery, zero-guesswork halting, precision arithmetic, edge-case test matrix |
| [`core-collaboration-charter`](active/core-collaboration-charter.rule.md) | Core Collaboration | Priority 2 & 3 | Single-unit incremental delivery, clarify gate, evidence-backed claims, four-link reasoning |
| [`file-folder-organization`](active/file-folder-organization.rule.md) | File & Folder Hygiene | Priority 4 | Mechanical naming delimiters, 4-level hierarchy, plural pools, root hygiene, and 6 verification gates |
| [`knowledge-grounding-and-citation`](active/knowledge-grounding-and-citation.rule.md) | Knowledge Grounding | Priority 5 | Multi-tier grounding hierarchy, read-only standard tiers, drift/draft hygiene, and 3-channel citations |
| [`markdown-formatting-and-layout`](active/markdown-formatting-and-layout.rule.md) | Markdown Layout | Priority 4 | Content density, compact tables, zero thematic breaks, zero HTML entities, deterministic awk checks |
| [`task-workflow-and-construction`](active/task-workflow-and-construction.rule.md) | Task Orchestration | Priority 6 | Six-phase pipeline, scaffold-first construction, binary deliverable safety, cross-platform whole-scope sweeps |
| [`technical-writing-principles`](active/technical-writing-principles.rule.md) | Technical Writing | Priority 5 | Ten universal authoring principles, anti-AI filters, 2-tier quality gates, and pre-export deliverable hygiene |

### Archived Rules

| Rule | Scope & Purpose | Summary |
| --- | --- | --- |
| [`database-design-and-sql`](archive/database-design-and-sql.rule.md) | Database Design & SQL | Retired ER/EER modeling, 1NF-BCNF normalization proofs, exact DECIMAL math, symmetric triggers, 5-category SQL verification |
| [`software-architecture-and-modeling`](archive/software-architecture-and-modeling.rule.md) | Software Architecture | Retired separation of Requirements/OOA/OOD, Inside-Out dependencies, SOLID principles, and UML modeling |

## Maintenance Rules

1. Register each new rule in `Rule Catalog by State` under its corresponding lifecycle state table (`active/` or `archive/`), including active `Precedence` where applicable.
2. Manage source tiers exclusively within this `INDEX.md` document (`Tier 5` for `active/`, `Tier 6` for `archive/`). Never record tier metadata inside individual `*.rule.md` files or frontmatter.
3. Mirror active rule definitions from `active/` to `.agents/rules/` and `.claude/rules/` when target workspace scaffolding is required; keep `archive/` rules out of active scaffolding.
