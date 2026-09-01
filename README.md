# Directive

A structured **Second Brain & Knowledge Base** for AI commanding — storing everything related to prompting, instructing, and directing AI agents: skills, prompts, rules, guides, papers, architectures, and more.

Optimized for both human navigation and AI Agent reference.

---

## 🎯 Mission

This repository serves as a structured **Second Brain & Knowledge Base** for AI commanding.

- **For humans**: This `README.md` is your navigable entry point — organized by intent, not by format.
- **For AI agents**: DO NOT READ THIS FILE. Your system-level directives, rules, and entry points live in `.agents/agents/directive/agent.md` and `REFERENCE_INDEX.md`.

---

## 🗂️ Repository Architecture

Our directories are organized by an **Intent-Based Taxonomy** along 3 axes.

### Decision Tree & Locations

| Intent Axis | Question | Location | Resource Types |
|---|---|---|---|
| **INSTRUCTIONS** | Will I feed this directly to AI for it to execute? | `instructions/` | Skills (`SKILL.md`), System Prompts, Rules (`.cursorrules`), Automation Scripts |
| **KNOWLEDGE** | Will I read this to learn about AI/prompting? | `knowledge/` | How-to Guides, Tutorials, Academic Papers, Articles |
| **BLUEPRINTS** | Is this a system design, blueprint, or mental model? | `blueprints/` | Architectures, Agent Designs, Mental Models, Frameworks |

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
| [**andrej-karpathy**](instructions/skills/external/andrej-karpathy/) | Behavioral principles and skills derived from Karpathy's notes. | Git Submodule |
| [**anthropics**](instructions/skills/external/anthropics/) | Official Claude skills and tool-use patterns. | Git Submodule |
| [**superpowers**](instructions/skills/external/superpowers/) | Advanced agentic skills for enhanced development workflows. | Git Submodule |
| [**system_prompts_leaks**](instructions/prompts/external/system_prompts_leaks/) | Structural references of leaked system prompts (Claude Code, Cursor, etc.). | Git Submodule |
| [**system-prompts-and-models-of-ai-tools**](instructions/prompts/external/system-prompts-and-models-of-ai-tools/) | Older collection of AI tool system prompts for cross-vendor comparison. | Git Submodule |
| [**ui-ux-pro-max-skill**](instructions/skills/external/ui-ux-pro-max-skill/) | AI-powered design intelligence and UI/UX engineering workflows. | Git Submodule |
| [**orca**](instructions/skills/external/orca/) | The AI Orchestrator for 100x builders (Codex, ClaudeCode, OpenCode, Pi). | Git Submodule |
| [**deeptutor-eduhub**](instructions/skills/external/deeptutor-eduhub/) | Education and tutoring skill patterns via EduHub registry. | Vendored Dir |
| [**Skillboard**](https://www.skillboard.lol/) | Global open-source catalog of custom skills for AI IDEs. | Website |

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
