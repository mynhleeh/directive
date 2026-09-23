# Directive

A structured **Second Brain & Knowledge Base** for AI commanding — storing everything related to prompting, instructing, and directing AI agents: skills, prompts, rules, guides, papers, architectures, and more.

Optimized for both human navigation and AI Agent reference.

---

## 🎯 Mission

This repository serves as a structured **Second Brain & Knowledge Base** for AI commanding.

- **For humans**: This `README.md` is your navigable entry point — organized by intent, not by format.
- **For AI agents**: DO NOT READ THIS FILE. Your system-level directives, rules, and entry points live in `.agents/agents/directive-encyclopedia/agent.md` and `REFERENCE_INDEX.md`.

---

## 🗂️ Repository Architecture

Our directories are organized by an **Intent-Based Taxonomy** along 4 axes.

### Decision Tree & Locations

| Intent Axis | Question | Location | Resource Types |
|---|---|---|---|
| **INSTRUCTIONS** | Will I feed this directly to AI for it to execute? | `instructions/` | Skills (`SKILL.md`), System Prompts, Rules (`*.rule.md`), Automation Scripts |
| **KNOWLEDGE** | Will I read this to learn about AI/prompting? | `knowledge/` | How-to Guides, Tutorials, Academic Papers, Articles |
| **BLUEPRINTS** | Is this a system design, blueprint, or mental model? | `blueprints/` | Architectures, Agent Designs, Mental Models, Frameworks |
| **CLI & TOOLING** | How do I scan, manage, or export these directives? | `directive-cli/` | Interactive CLI, scanner, exporter, test suites |

### Dynamic Lifecycle Splits (Tiers)

When a folder contains multiple sources or states, it is split into sub-folders:
- **`active/`**: Currently used, self-created resources.
- **`archive/`**: Retired, historical reference only.
- **`external/`**: Third-party content, git submodules, vendored directories.

*Note: If only one tier exists, files sit directly in the root folder (implicitly `active`).*

---

## 📚 External Reference Sources

The repository incorporates several external repositories and registries for research and skill building. Below is a complete catalog of all external references (see `REFERENCE_INDEX.md` for full citation policies, caveats, and licenses):

| Reference Source | Description | Type |
|---|---|---|
| [**AI-Research-SKILLs**](instructions/skills/external/AI-Research-SKILLs/) | Domain-specific ML engineering and AI research orchestration. | Git Submodule |
| [**Auto-Empirical-Research-Skills**](instructions/skills/external/Auto-Empirical-Research-Skills/) | Empirical research, econometric pipelines, and academic paper replication suites. | Git Submodule |
| [**andrej-karpathy**](instructions/skills/external/andrej-karpathy/) | Behavioral principles and skills derived from Karpathy's notes. | Git Submodule |
| [**anthropics**](instructions/skills/external/anthropics/) | Official Claude skills and tool-use patterns. | Git Submodule |
| [**scientific-agent-skills**](instructions/skills/external/scientific-agent-skills/) | 160+ scientific computing, computational biology, and materials science agent skills. | Git Submodule |
| [**superpowers**](instructions/skills/external/superpowers/) | Advanced agentic skills for enhanced development workflows. | Git Submodule |
| [**system_prompts_leaks**](instructions/prompts/external/system_prompts_leaks/) | Structural references of leaked system prompts (Claude Code, Cursor, etc.). | Git Submodule |
| [**system-prompts-and-models-of-ai-tools**](instructions/prompts/external/system-prompts-and-models-of-ai-tools/) | Older collection of AI tool system prompts for cross-vendor comparison. | Git Submodule |
| [**ui-ux-pro-max-skill**](instructions/skills/external/ui-ux-pro-max-skill/) | AI-powered design intelligence and UI/UX engineering workflows. | Git Submodule |
| [**orca**](instructions/skills/external/orca/) | The AI Orchestrator for 100x builders (Codex, ClaudeCode, OpenCode, Pi). | Git Submodule |
| [**humanizer**](instructions/skills/external/humanizer/) | Rewrite AI-sounding text so it reads like the writer without changing what it says. | Git Submodule |
| [**deeptutor-eduhub**](instructions/skills/external/deeptutor-eduhub/) | Education and tutoring skill patterns via EduHub registry. | Vendored Dir |
| [**Skillboard**](https://www.skillboard.lol/) | Global open-source catalog of custom skills for AI IDEs. | Website |

---

## 🤖 Core Agents, Governance Rules & Active Skills

### Core Agents (`instructions/agents/`)
Specialized system-level agent definitions synced into IDE workspaces (`.agents/agents/` and `.claude/agents/`):
- [**`directive-encyclopedia`**](instructions/agents/directive-encyclopedia/agent.md): Master librarian agent. Defines repository citation policies, manages tier hierarchies (Tier 1–5), and oversees index consistency.
- [**`omni`**](instructions/agents/omni/agent.md): Universal execution agent with multi-domain capabilities for codebase analysis, feature authoring, and orchestration.
- [**`cv-architect`**](instructions/agents/cv-architect/agent.md): Specialized persona for curriculum vitae, resume, and technical portfolio engineering.

### Governance Rules (`instructions/rules/`)
Repository-wide architectural and stylistic guardrails (synced to `.agents/rules/` and `.claude/rules/`):
- [**`file-folder-organization.rule.md`**](instructions/rules/file-folder-organization.rule.md): Strict MECE structure, directory taxonomy along 4 axes, and dynamic lifecycle tiering (`active/`, `archive/`, `external/`).
- [**`technical-writing-principles.rule.md`**](instructions/rules/technical-writing-principles.rule.md): Anti-AI writing guidelines, elimination of empty rhetoric, precise technical vocabulary, and factual calibration.

### Active Skills (`instructions/skills/active/`)
Curated, high-priority skills authored and maintained in-house:
- [**`academic-research-synthesizer`**](instructions/skills/active/academic-research-synthesizer/): Comprehensive academic literature synthesis, method-setting matrices, and research frontier mapping.
- [**`code-architect-auditor`**](instructions/skills/active/code-architect-auditor/): Full-spectrum codebase audits, structural hygiene checks, and architectural refactoring guidance.
- [**`skill-forge`**](instructions/skills/active/skill-forge/): End-to-end framework for authoring, evaluating, refining, and testing new agent skills.
- [**`tech-mentor`**](instructions/skills/active/tech-mentor/): Interactive software engineering tutoring, Socratic debugging, and technical coaching.
- [**`technical-doc-author`**](instructions/skills/active/technical-doc-author/): Production technical documentation authoring featuring an automated multi-subagent anti-AI decontamination audit loop (v3.4.0).

---

## 🛠️ CLI & Management Tooling (`directive-cli`)

The repository includes a standalone Python CLI toolsuite (`directive-cli/`) designed to inspect, validate, and scaffold directives:

- **Interactive TUI**: Powered by `questionary` for guided workspace management.
- **Directive Scanner**: Scans and inventories installed agents, rules, and skills across `.agents/`, `.claude/`, and `instructions/`.
- **Packaging & Export**: Validates YAML frontmatter, resolves references, and bundles skills for deployment.
- **Automated Test Suite**: Integrated with `pytest` for regression testing.

### Quickstart

```bash
# Install dependencies
pip install -r directive-cli/requirements.txt

# Launch interactive CLI
python directive-cli/main.py

# Run test suite
pytest directive-cli/tests/ -v
```

---

## 📋 Metadata Convention

All owned files in the repository should include a YAML frontmatter header to assist with indexing:

```yaml
---
name: "Resource name"
description: "Brief description"
tags: [tag1, tag2, tag3]
---
```
