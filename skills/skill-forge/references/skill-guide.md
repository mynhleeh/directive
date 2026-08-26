# Skill Guide — Creating AGY Skills

A guide for creating skills for the Antigravity (AGY) agent system.

---

## What Is a Skill?

A skill is a **cheatsheet / instruction set** stored as a directory, loaded on-demand by an AGY agent when relevant. Skills enable agents to perform complex workflows in a structured, repeatable way.

---

## Directory Structure

```
skills/
└── skill-name/
    ├── SKILL.md          ← REQUIRED: Main instruction file
    ├── scripts/          ← Optional: Helper scripts
    ├── examples/         ← Optional: Reference implementations
    ├── resources/        ← Optional: Additional files and templates
    └── references/       ← Optional: External documentation
```

---

## SKILL.md Format

```markdown
---
name: skill-name
description: One-sentence description of what this skill does
version: 1.0.0
---

# Skill Name

## Overview
[What this skill does and when to use it]

## When to Activate
[Specific triggers or conditions for using this skill]

## Prerequisites
[What needs to be set up or known before using]

## Instructions
[Step-by-step workflow instructions]

## Examples
[Usage examples with inputs and outputs]

## Common Issues
[Known problems and solutions]

## References
[Links to related resources]
```

---

## YAML Frontmatter Fields

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Kebab-case skill name (matches folder name) |
| `description` | Yes | One-sentence description for skill discovery |
| `version` | No | Semantic version (e.g., `1.0.0`) |
| `author` | No | Creator name |
| `tags` | No | Array of keywords for categorization |
| `dependencies` | No | Other skills this depends on |

---

## Writing Effective Instructions

### 1. Clear Activation Criteria
```markdown
## When to Activate
- User asks to "create a prompt" or "write a system prompt"
- User wants to improve an existing prompt
- User needs to define a function or tool schema
- Keywords: "prompt", "system prompt", "tool definition", "function calling"
```

### 2. Step-by-Step Workflow
```markdown
## Instructions

### Step 1: Identify Output Type
Determine what the user needs:
- System prompt → go to System Prompt workflow
- User prompt → go to User Prompt workflow
- Function schema → go to Function Schema workflow

### Step 2: Gather Requirements
Ask for (or infer from context):
- Target platform (Claude / OpenAI / Gemini / platform-agnostic)
- Use case and domain
- Tone and style preferences
- Any constraints
```

### 3. Concrete Examples
```markdown
## Examples

### Example 1: Customer Support Bot System Prompt
**Input**: "Create a system prompt for a customer support bot for an e-commerce site"
**Process**: 
- Output type: system prompt
- Platform: not specified → use platform-agnostic
- Domain: e-commerce customer support
**Output**: [full system prompt here]
```

---

## Skill Sizing Guidelines

| Size | Description | Approx. SKILL.md length |
|---|---|---|
| **Micro** | Single, focused task | 50–100 lines |
| **Standard** | 2–5 related workflows | 100–300 lines |
| **Complex** | Multi-domain with heavy references | 300+ lines + sub-files |

---

## The Skill Execution Loop

From the `skill-creator` reference pattern:

```
1. Read SKILL.md instructions in full
2. Identify which workflow to follow
3. Gather required inputs (ask if missing)
4. Execute workflow steps
5. Output result in the user's language
6. Offer to iterate or improve
```

---

## Naming Conventions

- **Folder name**: `kebab-case` (e.g., `skill-forge`, `code-reviewer`)
- **Main file**: Always `SKILL.md` — uppercase, always `.md`
- **Script files**: `kebab-case.py`, `kebab-case.sh`
- **Example files**: Descriptive names inside `examples/`

---

## Skill vs Rules vs Hooks

| Type | Location | Purpose | When Loaded |
|---|---|---|---|
| **Skill** | `skills/skill-name/SKILL.md` | Workflow instructions | On-demand when relevant |
| **Rules** | `rules/*.md` or `GEMINI.md` | Always-on guidelines | Every session |
| **Hook** | `hooks.json` | Automated triggers | On specified events |

---

## Multilingual Skills

To support multiple languages, add a language policy to the skill instructions:

```markdown
## Language Policy
Respond in the same language the user writes in.
All internal processing follows these English instructions,
but all user-facing output should match the user's language.
```

---

## Checklist Before Publishing

- [ ] YAML frontmatter is complete (`name`, `description`)
- [ ] `description` is specific enough for discovery
- [ ] Clear "When to Activate" section with keywords
- [ ] Step-by-step instructions (not vague goals)
- [ ] At least 2 concrete examples with inputs and outputs
- [ ] Tested with 5+ diverse inputs
- [ ] Referenced external files exist (no broken paths)
- [ ] Consistent naming conventions throughout
- [ ] Language policy defined if multilingual support needed
