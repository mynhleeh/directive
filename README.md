# Directive

A structured **Second Brain & Knowledge Base** for AI commanding — storing everything related to prompting, instructing, and directing AI agents: skills, prompts, rules, guides, papers, architectures, and more.

Optimized for both human navigation and AI Agent reference.

---

## 🎯 Mission

This repository serves a **dual purpose**:

- **For humans**: a navigable knowledge base for everything related to AI commanding — organized by intent, not by format.
- **For AI agents**: a system-level directive and entry point. When this README is in context, an AI agent should use it to autonomously navigate, prioritize, and retrieve resources from this repository to fulfill user requests.

---

## 🗂️ Directory Structure

```
directive/
├── instructions/               # Resources to DIRECTLY COMMAND AI (execute immediately)
│   ├── skills/                 # Skill files (SKILL.md format)
│   ├── prompts/                # System prompts & prompt collections
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

### Dynamic Lifecycle Split

Sub-folders are created **only when a folder contains 2 or more different tiers**.
If a folder has only one type of resource, files sit directly in that folder (implicitly treated as `active`).

#### The 3 Tiers

| Tier | Purpose | Contains |
|---|---|---|
| `active/` | Currently used, actively maintained | Self-created resources in use |
| `archive/` | Retired — historical reference only | Self-created resources no longer in use |
| `external/` | Third-party content, submodules | External repos, cloned resources |

#### Trigger Rule

| Types present in folder | Action |
|---|---|
| Only 1 type | **No sub-folders** — files sit directly in folder |
| 2 or more types | **Create sub-folders** for each type present |

#### MECE Boundary

- `active/` and `archive/` contain **only self-created resources**.
- `external/` contains **only third-party resources**.
- When an `external/` resource is no longer needed → **remove/untrack the submodule** (do not move to `archive/`).

Currently split folders: `instructions/skills/` (`active/` + `external/`), `instructions/prompts/` (`active/` + `archive/` + `external/`).

---

## 📚 Knowledge Source Hierarchy

When citing or referencing content from this repository, apply the following priority order. Higher tiers carry greater epistemic weight — always prefer the highest available tier for any given claim.

| Priority | Type | Location | Signal |
|---|---|---|---|
| Tier 1 | Academic papers, technical reports, benchmark studies | `knowledge/papers/` | Peer-reviewed, cited, reproducible |
| Tier 2 | Official documentation, architecture specs | `blueprints/architectures/`, `knowledge/guides/` | Authoritative source |
| Tier 3 | Curated guides, tutorials | `knowledge/guides/` | Practitioner-verified |
| Tier 4 | Articles, blog posts | `knowledge/articles/` | Community knowledge |
| Tier 5 | External submodules | `instructions/*/external/` | Third-party curated resources |
| Tier 6 | Active working files | `instructions/*/active/` | Operational, not necessarily evidence-based |
| Tier 7 | Archive | `instructions/*/archive/` | Historical, may be outdated |

> **Note on Tier 5 vs Tier 6**: External submodules rank above active files because they typically represent curated third-party collections with broader scope, even though their quality is unverified. Neither should be used to support factual claims when Tier 1–4 sources exist.

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

## 🤖 AI Agent Directive

This section is a **system-level directive** for any AI agent operating with this repository in context — applies universally to all tools and ecosystems (Cursor, Claude, Gemini, GPT, Copilot, and others).

### Execution Protocol

When receiving a user request in the context of this repository:

```
Step 1: Read this README — establish repo scope and available resources.
Step 2: Classify the request type:
          INSTRUCT  → navigate to instructions/
          LEARN     → navigate to knowledge/
          DESIGN    → navigate to blueprints/
Step 3: Consult the Knowledge Source Hierarchy before citing any resource.
Step 4: Prioritize Tier 1–3 sources for factual or methodological claims.
Step 5: Cross-reference YAML frontmatter for semantic matching where available.
Step 6: Execute the request using the highest-tier applicable source found.
```

### Resource Discovery Rules

- **Skills** → `instructions/skills/active/` — each skill is a directory containing a `SKILL.md` file
- **Curated prompts** → `instructions/prompts/active/`
- **Scientific backing** → `knowledge/papers/` [HIGHEST PRIORITY — Tier 1]
- **Methodology and guides** → `knowledge/guides/` [Tier 2–3]
- **System design reference** → `blueprints/`
- **External raw prompts** → `instructions/prompts/external/` [Tier 5 — use as data source, not authority]

### Trust & Citation Rules

```
ALWAYS cite source tier when referencing content.
PREFER knowledge/papers/ over any other source for factual claims.
PREFER knowledge/guides/ over instructions/prompts/ for methodology.
TREAT instructions/*/external/ as higher priority than active/archive context.
TREAT instructions/*/active/ as operational context, not as evidence.
DO NOT reference archive/ unless explicitly asked for historical context.
DO NOT treat submodule content as peer-reviewed or verified, despite being external.
```

### Current Resource Index

<!-- INDEX:START -->
```
directive/
├── blueprints/                 # Resources to DESIGN AI systems
│   ├── architectures/          # System designs, agent architectures
│   └── concepts/               # Mental models, taxonomy, frameworks
├── instructions/               # Resources to DIRECTLY COMMAND AI (execute immediately)
│   ├── prompts/                # System prompts & prompt collections
│   │   ├── active/
│   │   │   ├── function-anatomist.md       # Prompt structure breakdown
│   │   │   ├── git-github.md               # Git commands and workflow
│   │   │   └── system-architecture.md      # Architecture design prompt
│   │   ├── archive/
│   │   │   ├── dsa.md                      # Data structures & algorithms
│   │   │   └── n8n.md                      # n8n automation workflows
│   │   └── external/
│   │       ├── system-prompts-and-models-of-ai-tools/ [submodule]
│   │       └── system_prompts_leaks/ [submodule]
│   ├── rules/                  # Rules files (AGENTS.md, .cursorrules, GEMINI.md…)
│   ├── scripts/                # Automation scripts for AI workflows
│   └── skills/                 # Skill files (SKILL.md format)
│       ├── active/
│       │   ├── deep-flashcard-generator/   # Flashcard generation skill
│       │   ├── doc-drill/                  # Document drilling & Q&A skill
│       │   ├── document-vocab-extractor/   # Vocabulary extraction skill
│       │   ├── skill-forge/                # Meta-orchestrator: generates/critiques/converts/explains/distills/navigates artifacts
│       │   └── vocab-lookup/               # Vocabulary lookup skill
│       └── external/
│           ├── andrej-karpathy/ [submodule]
│           └── anthropics/ [submodule]
└── knowledge/                  # Resources to READ & LEARN about AI/prompting
    ├── articles/               # Blog posts, case studies, saved pages
    ├── guides/                 # How-to guides, tutorials, manuals
    │   └── the-complete-guide-to-building-skill-for-claude.pdf
    └── papers/                 # Academic & technical papers [PRIORITY SLOT — Tier 1]
```
<!-- INDEX:END -->

> External submodules (e.g., `system_prompts_leaks`, `andrej-karpathy`, `anthropics`) may have their own README files with internal navigation.