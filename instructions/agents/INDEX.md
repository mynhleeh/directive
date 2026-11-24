---
name: agents-index
description: "Index, capabilities catalog, and trust classification for agent specifications under instructions/agents/. Read to discover available specialized agents."
version: 1.3.0
tags: [agents, index, tiers, orchestration, capabilities]
metadata:
  author: "directive"
  scope: "All agent definitions under instructions/agents/"
---

# Agents Index

Catalog and source-trust classification for agent specifications under `instructions/agents/`. Canonical definitions of the 6-tier trust scale live in [README.md](../../README.md).

## Module Tier

All owned agent specifications in this directory are in-house AI-authored working assets classified under **Tier 5**.

## Agent Catalog

| Agent | Archetype / Focus | Description |
| --- | --- | --- |
| [`academic-mentor`](academic-mentor/agent.md) | Academic Examiner & Coach | Read-only Socratic tutor and defense examiner for software, database, and CS capstone projects |
| [`cv-architect`](cv-architect/agent.md) | Career & Resume Strategist | High-impact CV, resume, and technical portfolio architect using STAR/XYZ methods |
| [`database-architect`](database-architect/agent.md) | Data & SQL Architect | Relational data modeler and SQL engineer for ER/EER design, 1NF-BCNF normalization, DDL/triggers, and parity audits |
| [`directive-encyclopedia`](directive-encyclopedia/agent.md) | Living Repository Librarian | Master librarian and living encyclopedia for the directive knowledge base and external grounding |
| [`omni`](omni/agent.md) | Meta-Orchestrator | Domain-agnostic meta-orchestrator for multi-faceted tasks, dynamic skill discovery, and subagents |
| [`software-lifecycle-architect`](software-lifecycle-architect/agent.md) | Systems Architect | Systems architect governing requirements, OOA/OOD architecture, inside-out coding, and reviews |

## Maintenance Rules

1. Register each new agent specification in `Agent Catalog` with its archetype and concise summary.
2. All agent specifications in this directory are governed as Tier 5 assets. Never record tier metadata inside individual `agent.md` files or frontmatter.
3. Mirror active agent definitions to `.agents/agents/` when target workspace scaffolding is required.
