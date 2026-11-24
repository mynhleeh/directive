# Rules File Guide

A guide for writing always-on instruction files for AI agents and coding assistants.

## What Is a Rules File?

A rules file is a Markdown file containing **always-on instructions** for an agent — unlike skills (loaded on-demand), rules files are loaded into every session. They define:
- Coding style and conventions
- Behavioral defaults
- Project-specific context
- Forbidden actions

## Platform Comparison Matrix

| Feature | CLAUDE.md | AGENTS.md / GEMINI.md | Cursor .mdc | .cursorrules |
| --- | --- | --- | --- | --- |
| **Platform** | Claude Code / CLI | Generic agent harnesses | Cursor IDE | Cursor IDE (legacy) |
| **Scope** | Project or global | Project or global | Per-file or global | Global |
| **Format** | Markdown | Markdown | MDC (Markdown + YAML meta) | Plain text |
| **Auto-loaded** | Yes | Yes | On file match | Yes (legacy) |
| **File location** | Root or `.agents/` | Root or `.agents/rules/` | `.cursor/rules/` | `.cursorrules` |
| **Frontmatter** | No | No | Yes (YAML) | No |
| **Glob patterns** | No | No | Yes | No |
| **Priority** | High | High | Context-dependent | Lower than .mdc |

## CLAUDE.md Structure (Andrej Karpathy Style)

Recommended for: Claude agents, coding agents, generic agent workspaces

```markdown
# Project Name

## Overview
[Brief description of what this project does]

## Tech Stack
- Language: Python 3.11
- Framework: FastAPI
- Database: PostgreSQL

## Code Style
- Use type hints for all functions
- Write docstrings for all public methods
- Max line length: 100 characters
- Prefer f-strings over .format()

## Common Commands
- Run tests: `pytest tests/`
- Format code: `ruff format .`
- Type check: `mypy .`

## Architecture Notes
- All API routes in `app/routes/`
- Database models in `app/models/`
- Business logic in `app/services/`

## Constraints
- NEVER commit secrets or API keys
- ALWAYS write tests for new features
- DO NOT modify migration files directly
```

## Behavioral Coding Principles (External Companion)

When authoring always-on rules that need behavioral guardrails (think before coding, simplicity first,
surgical changes, goal-driven execution), invoke `karpathy-guidelines` resolved dynamically in the
active runtime workspace (`.agents/`, `.claude/`, `.codex/`). Treat `karpathy-guidelines` as
**Tier 4 candidate community heuristics** per `artifact-placement.md` — validate each principle against project
requirements or `Tier 1-3` engineering standards before promoting it into a mandatory rule, and keep one canonical source synchronized
across formats (`CLAUDE.md` <-> `.cursor/rules/*.mdc` <-> `GEMINI.md` / `AGENTS.md`).

## Single-Source -> Multi-Format Sync

When a rules file is published across platforms (`CLAUDE.md` <-> `.cursor/rules/*.mdc` <-> `GEMINI.md` / `AGENTS.md`), keep shared principles in sync across all formats. If you edit them in one file, update all targets — the source of truth is one file, and formats multiply from it.

```text
CLAUDE.md                                 <- source of truth
└── .cursor/rules/karpathy-guidelines.mdc <- same principles, .mdc format
└── GEMINI.md / AGENTS.md                 <- same principles, agent format
```

> **Rule**: Use a section marker like `## Behavioral Coding Principles` or `## Four Principles` and keep identical wording across formats so `diff`-based sync is trivial.

## GEMINI.md / AGENTS.md Structure (Generic Agent Workspace)

Recommended for: Generic agent harnesses and multi-tool workspaces

```markdown
# Project Rules

## Behavior
- Always confirm before deleting files
- Prefer small, focused changes over large refactors
- Ask for clarification when requirements are ambiguous

## Code Conventions
[Project-specific conventions]

## Forbidden Actions
- Do not run database migrations automatically
- Do not commit to the main branch directly
- Do not expose API keys in code or logs

## Context
[Important project context the agent should always know]
```

## Cursor .mdc Format

```markdown
---
description: Rules for Python backend code
globs: ["**/*.py", "!**/tests/**"]
alwaysApply: false
---

# Python Backend Rules

## Style
- Use type annotations on all function signatures
- Write docstrings for all public methods
- Follow PEP 8 strictly

## Patterns
- Use dependency injection for services
- Prefer composition over inheritance
```

### .mdc Frontmatter Fields

| Field | Description |
| --- | --- |
| `description` | What these rules are for (displayed in the Cursor UI) |
| `globs` | File patterns these rules apply to |
| `alwaysApply` | If `true`, always included regardless of file context |

## Legacy .cursorrules Format

Simple plain text, no frontmatter:

```text
You are an expert in TypeScript, React, and Next.js.

Code Style:
- Use functional components with hooks
- Prefer named exports over default exports
- Use TypeScript strict mode
- Always handle loading and error states

Architecture:
- Keep components small and focused
- Extract custom hooks for reusable logic
- Use server components where possible in Next.js 14+

Testing:
- Write unit tests for utility functions
- Use React Testing Library for component tests
```

## Content Categories

### 1. Identity & Expertise

```markdown
You are an expert in [domain] with deep knowledge of [technologies].
```

### 2. Code Style Preferences

```markdown
## Code Style
- Prefer [pattern] over [anti-pattern]
- Use [naming convention] for [things]
- Maximum [constraint] for [element]
```

### 3. Architecture Decisions

```markdown
## Architecture
- [Component type] lives in [location]
- [Pattern] is used for [use case]
- Never use [anti-pattern]
```

### 4. Common Commands

```markdown
## Commands
- Build: `npm run build`
- Test: `npm test`
- Deploy: `./scripts/deploy.sh`
```

### 5. Behavioral Instructions

```markdown
## Behavior
- Always [action] before [other action]
- Ask for confirmation when [condition]
- Default to [approach] unless explicitly specified
```

### 6. Constraints & Safety

```markdown
## Constraints
- NEVER [forbidden action]
- ALWAYS [required action]
- DO NOT [risky action] without [safeguard]
```

## Writing Guidelines

### DO:

- Use imperative voice ("Use", "Write", "Prefer")
- Be specific and concrete
- Include examples for rules that might be misinterpreted
- Organize with clear section headings
- Keep individual rules short (1–2 lines each)

### DON'T:

- Write contradictory rules
- Include confidential information (keys, passwords)
- Write rules so vague they don't change behavior ("be good")
- Include implementation details that are likely to change

## File Placement Strategy

```text
Project Root/
├── CLAUDE.md            ← Global project rules (for coding agents)
├── GEMINI.md            ← Gemini-compatible agent rules
├── .agents/
│   └── rules/
│       ├── coding-style.md
│       └── project-context.md
└── .cursor/
    └── rules/
        ├── typescript.mdc
        └── python.mdc
```

## Checklist

- [ ] Rules are specific and actionable
- [ ] No contradictory instructions
- [ ] Tech stack is documented
- [ ] Common commands are listed
- [ ] Forbidden actions are explicit and concrete
- [ ] Rules organized with clear headings
- [ ] File length is appropriate (not so long that key rules are diluted)
