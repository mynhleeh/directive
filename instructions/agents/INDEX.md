---
name: agents-index
description: "Index, capabilities catalog, lifecycle state, and trust classification for agent specifications under instructions/agents/ (active, archive). Read to discover available specialized agents."
version: 1.4.0
tags: [agents, index, tiers, lifecycle, orchestration, capabilities]
metadata:
  author: "directive"
  scope: "All active and archived agent definitions under instructions/agents/"
---

# Agents Index

Catalog, lifecycle state, and source-trust classification for agent specifications under `instructions/agents/`. Canonical definitions of the 6-tier trust scale live in [README.md](../../README.md).

## Lifecycle State & Source Trust Overview

| Lifecycle State | Focus & Provenance | Tier | Count | Notes |
| --- | --- | --- | --- | --- |
| [`active/`](active/) | Maintained in-house agent personas and tool definitions | `Tier 5` | 4 agents | Operational Role: Workspace Governance; eligible for `.agents/agents/` mirroring |
| [`archive/`](archive/) | Retired in-house agent specifications kept for historical reference | `Tier 6` | 2 agents | Historical reference only; excluded from active workspace scaffolding |

## Agent Catalog by State

### Active Agents

| Agent | Archetype / Focus | Description |
| --- | --- | --- |
| [`academic-mentor`](active/academic-mentor/agent.md) | Academic Examiner & Coach | Read-only Socratic tutor and defense examiner for software, database, and CS capstone projects |
| [`cv-architect`](active/cv-architect/agent.md) | Career & Resume Strategist | High-impact CV, resume, and technical portfolio architect using STAR/XYZ methods |
| [`directive-encyclopedia`](active/directive-encyclopedia/agent.md) | Living Repository Librarian | Master librarian and living encyclopedia for the directive knowledge base and external grounding |
| [`omni`](active/omni/agent.md) | Meta-Orchestrator | Domain-agnostic meta-orchestrator for multi-faceted tasks, dynamic skill discovery, and subagents |

### Archived Agents

| Agent | Archetype / Focus | Description |
| --- | --- | --- |
| [`database-architect`](archive/database-architect/agent.md) | Data & SQL Architect | Retired relational data modeler and SQL engineer for ER/EER design, 1NF-BCNF normalization, DDL/triggers, and parity audits |
| [`software-lifecycle-architect`](archive/software-lifecycle-architect/agent.md) | Systems Architect | Retired systems architect governing requirements, OOA/OOD architecture, inside-out coding, and reviews |

## Maintenance Rules

1. Register each new agent specification in `Agent Catalog by State` under its corresponding lifecycle state table (`active/` or `archive/`).
2. Manage source tiers exclusively within this `INDEX.md` document (`Tier 5` for `active/`, `Tier 6` for `archive/`). Never record tier metadata inside individual `agent.md` files or frontmatter.
3. Mirror active agent definitions from `active/` to `.agents/agents/` when target workspace scaffolding is required; keep `archive/` definitions out of active scaffolding.
