# Directive

A structured **Second Brain & Knowledge Base** for AI commanding — storing everything related to prompting, instructing, and directing AI agents: skills, prompts, rules, guides, papers, architectures, and more.

Optimized for both human navigation and AI Agent reference.

---

## 🗂️ Directory Structure

```
directive/
├── instructions/               # Resources to DIRECTLY COMMAND AI (execute immediately)
│   ├── skills/
│   │   ├── owned/              # Self-created skill files
│   │   │   └── skill-forge/   # Skill for creating/critiquing prompts & skills
│   │   └── external/          # Skills from external sources (git submodules)
│   │       ├── andrej-karpathy/
│   │       └── anthropics/
│   ├── prompts/                # System prompts & prompt collections
│   │   ├── system_prompts_leaks/
│   │   └── system-prompts-and-models-of-ai-tools/
│   ├── rules/                  # Rules files (AGENTS.md, .cursorrules, GEMINI.md…)
│   └── scripts/                # Automation scripts for AI workflows
│
├── knowledge/                  # Resources to READ & LEARN about AI/prompting
│   ├── guides/                 # How-to guides, tutorials, manuals
│   ├── papers/                 # Academic & technical papers
│   └── articles/               # Blog posts, case studies, saved pages
│
└── blueprints/                 # Resources to DESIGN AI systems
    ├── architectures/          # System designs, agent architectures
    └── concepts/               # Mental models, taxonomy, frameworks
```

---

## 🧭 Classification Standard

### 3 Axes — Intent-Based Taxonomy

| Axis | Decision Question | Folder |
|---|---|---|
| **INSTRUCTIONS** | Will I feed this directly to AI for it to execute? | `instructions/` |
| **KNOWLEDGE** | Will I read this to learn about AI/prompting? | `knowledge/` |
| **BLUEPRINTS** | Is this a design, blueprint, or mental model? | `blueprints/` |

### Decision Tree

```
Q1: Will I feed this directly to an AI agent to execute?
  → Yes → instructions/
  → No  → Q2

Q2: Will I read this to learn about AI or prompting?
  → Yes → knowledge/
  → No  → Q3

Q3: Is this a system design, architecture, or mental model?
  → Yes → blueprints/
```

### Resource Classification Table

| Resource type | Axis | Location |
|---|---|---|
| Skill files (`SKILL.md`) | INSTRUCTIONS | `instructions/skills/` |
| System prompts | INSTRUCTIONS | `instructions/prompts/` |
| System prompt leaks (raw) | INSTRUCTIONS | `instructions/prompts/` |
| Rules files (`AGENTS.md`, `.cursorrules`) | INSTRUCTIONS | `instructions/rules/` |
| Automation scripts | INSTRUCTIONS | `instructions/scripts/` |
| How-to guides, tutorials | KNOWLEDGE | `knowledge/guides/` |
| Academic / technical papers | KNOWLEDGE | `knowledge/papers/` |
| Blog posts, saved articles | KNOWLEDGE | `knowledge/articles/` |
| System architecture diagrams | BLUEPRINTS | `blueprints/architectures/` |
| Mental models, frameworks | BLUEPRINTS | `blueprints/concepts/` |

### Dynamic `owned/` vs `external/` Split

Sub-folders are created only **when a folder contains BOTH owned and external resources**.

| Folder state | Structure |
|---|---|
| Only owned | Files/dirs directly in folder |
| Only external | Files/dirs directly in folder |
| **Both owned & external** | Create `owned/` and `external/` sub-folders |

Currently `instructions/skills/` is the only folder with both types.

---

## 📋 Metadata Convention (YAML Frontmatter)

All owned files should include a YAML frontmatter header:

```yaml
---
name: "Resource name"
description: "Brief description"
tags: [tag1, tag2, tag3]
---
```

---

## 🤖 Note for AI Agents

When searching for context or references, use this index to navigate:

- **To instruct / prompt an AI** → start in `instructions/`
- **To learn about prompting techniques** → start in `knowledge/`
- **To understand AI system design** → start in `blueprints/`
- **Skill files** are always named `SKILL.md` and located in `instructions/skills/`
- **Most owned files** contain YAML frontmatter for semantic search and categorization

> External submodules (e.g., `system_prompts_leaks`, `andrej-karpathy`, `anthropics`) may have their own README files with internal navigation.