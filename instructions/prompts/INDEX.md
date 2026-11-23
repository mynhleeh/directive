---
name: prompts-index
description: "Index, capabilities catalog, and trust classification for prompt collections and captures under instructions/prompts/ (active, archive, external). Read to discover available system prompts and external references."
version: 1.2.0
tags: [prompts, index, tiers, system-prompts, personas, instructions]
metadata:
  author: "directive"
  scope: "All prompt collections under instructions/prompts/"
---

# Prompts Index

Catalog and source-trust classification for prompt collections under `instructions/prompts/`. Canonical definitions of the 6-tier trust scale live in [README.md](../../README.md).

## Lifecycle State & Source Trust Overview

| Lifecycle State | Focus & Provenance | Tier | Count | Notes |
| --- | --- | --- | --- | --- |
| [`active/`](active/) | In-house specialized persona prompts and multi-file packages | `Tier 5` | 3 packages | Active domain-specific prompt packages |
| [`archive/`](archive/) | Retired in-house prompts kept for historical reference | `Tier 6` | 2 files | Standalone historical prompts |
| [`external/`](external/) | Third-party prompt captures and leak repositories | `Tier 6` | 2 submodules | Unverified captures; structural syntax examples only |

## Prompt Catalog by State

### Active Prompts

| Prompt Package | Focus / Domain | Tier | Description |
| --- | --- | --- | --- |
| [`autonomous-software-engineer`](active/autonomous-software-engineer/instruction.md) | Software Engineering | `Tier 5` | Autonomous software engineer prompt with strict execution lifecycle and testing discipline |
| [`deep-reasoning-researcher`](active/deep-reasoning-researcher/instruction.md) | Deep Research | `Tier 5` | Deep reasoning researcher prompt for structured hypothesis formulation and literature synthesis |
| [`psychological-counselor`](active/psychological-counselor/instruction.md) | Psychological Counseling | `Tier 5` | Multi-file clinical counseling prompt bundle with CBT, interview pacing, and crisis protocols |

### Archived Prompts

| Prompt | Domain | Tier | Description |
| --- | --- | --- | --- |
| [`dsa`](archive/dsa.md) | Data Structures & Algorithms | `Tier 6` | Retired problem-solving prompt for competitive programming and data structure practice |
| [`n8n`](archive/n8n.md) | Workflow Automation | `Tier 6` | Retired workflow automation prompt for node-based orchestration and API triggers |

### External Prompt Registries

| Repository | Origin | Tier | Purpose |
| --- | --- | --- | --- |
| [`system-prompts-and-models-of-ai-tools`](external/system-prompts-and-models-of-ai-tools/) | Git Submodule | `Tier 6` | Community collection of AI tool system prompts and model configuration guides |
| [`system_prompts_leaks`](external/system_prompts_leaks/) | Git Submodule | `Tier 6` | Large-scale repository of extracted commercial system prompts across major AI providers |

## Maintenance Rules

1. Register each new prompt package in `Prompt Catalog by State` under its corresponding lifecycle state table.
2. Manage source tiers exclusively within this `INDEX.md` document. Never record tier metadata inside individual prompt files or frontmatter.
3. Treat `external/` prompt captures strictly as structural syntax examples; prohibited as active factual authority or official vendor documentation.
