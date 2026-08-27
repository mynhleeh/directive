# House Structure Conventions

The **unified structural template** for every generated skill. It codifies how a `SKILL.md` and its supporting directories should be organized, so the meta-skill emits consistent, well-structured artifacts every time.

> **Why this file exists**: The repo's active skills varied — `deep-flashcard-generator` was self-contained, `doc-drill` used a lazy-loaded `references/` folder, `vocab-lookup` shipped a companion `prompt.md`. This file reconciles them into one canonical structure.

---

## Directory Structure

```
skill-name/
├── SKILL.md          ← REQUIRED: the main instruction file
├── references/       ← OPTIONAL: docs loaded into context on demand (progressive disclosure)
├── scripts/          ← OPTIONAL: executable helper scripts
├── examples/         ← OPTIONAL: reference implementations / input-output pairs
└── assets/           ← OPTIONAL: templates, icons, fonts used in output
```

---

## Canonical SKILL.md Skeleton

```markdown
---
name: skill-name
description: "What it does AND when to trigger."
version: 1.0.0
tags: [tag1, tag2]
---

# {Display Name}

> {One-line mission statement — the single purpose of this skill}

## When to Activate
[Explicit trigger logic + keyword list + near-miss negatives]

## Overview
[What this skill does, its scope, and when to use it]

## Instructions
[Step-by-step workflow — imperative voice, numbered phases where order matters]

## Output Contract
[EXACT output format — a single block, no other prose. Critical for reliability.]

## Examples
[Concrete input → output pairs, showing the contract in action]

## Common Issues
[Known pitfalls and their fixes]

## References
[Relative paths to reference files, with "when to read this"]
```

---

## Progressive Disclosure (Critical)

The `references/` folder is the key to keeping `SKILL.md` lean. Follow the three-layer model:

| Layer | What | Where | Loaded |
|---|---|---|---|
| **Metadata** | `name`, `description`, `tags` | Frontmatter | Always, at startup |
| **Instructions** | Core workflow, output contract | `SKILL.md` body | On activation |
| **Resources** | Detailed guides, tables, edge cases | `references/` | Only when needed |

### Rules
- **Keep `SKILL.md` under 500 lines / 5000 tokens.** If a workflow needs more depth, split it into `references/`.
- **Split by variant**, not by concern, when a domain has multiple flavors — e.g., `references/aws.md`, `references/gcp.md` so the agent reads only the relevant one.
- **Reference files should be one directory deep** with relative paths, and include *"when to read this"* guidance so the agent knows if/when to open them.

```markdown
## References
- `references/adaptive-difficulty.md` — Read when the learner's accuracy drifts out of the target band.
- `references/format-ladder.md` — Read when escalating card format complexity.
```

---

## Output Contract (Essential for Reliability)

Every generated skill that produces structured output **must** declare an explicit output contract. This is the single biggest driver of reliability.

```markdown
## Output Contract

## [What to emit, and ONLY what to emit]

Output a single `{format}` block. No preamble, no postamble, no conversation.
```

### Example (from `deep-flashcard-generator`-style skills)
```
## Output Contract

## Cards
Emit a single TSV block. Each line is one card: field1, field2, field3.
No other prose before or after the block.
```

### Why it matters
- Eliminates the model "explaining" instead of emitting.
- Makes output machine-parseable (TSV, JSON, Markdown table).
- Mirrors the real-world skill pattern: *"output only this exact format."*

---

## Anti-Examples (❌ / ✅)

Every skill that bounds behavior should use explicit contrast pairs instead of abstract prose.

```
❌ "Be accurate."              → too vague to enforce
✅ "If you are not 100% certain about a fact, omit the card entirely."
```

```markdown
## Anti-Examples

| ❌ Avoid | ✅ Prefer | Why |
|---|---|---|
| "Be helpful" | "Guide the user to the answer without doing the work" | Concrete action |
| "Never speculate" | "If uncertain, omit; use only universal known facts as support" | Enforceable |
```

---

## Naming & File Conventions

| Item | Convention |
|---|---|
| Folder + `name` | `kebab-case`, matches exactly |
| Main file | `SKILL.md` (uppercase, `.md`) |
| Scripts | `kebab-case.py` / `kebab-case.sh` |
| Reference files | lowercase, hyphenated, descriptive |
| Output blocks | A single fenced block, clearly labeled |

---

## Generated-Skill Checklist

- [ ] Frontmatter follows the House Frontmatter Contract (name matches dir, trigger description)
- [ ] `## When to Activate` present (for standard/deep tiers)
- [ ] `## Overview` states scope
- [ ] `## Instructions` is imperative and step-by-step
- [ ] `## Output Contract` declares exactly what to emit
- [ ] `## Anti-Examples` uses ❌/✅ contrast pairs
- [ ] `## References` uses relative paths with "when to read this"
- [ ] `SKILL.md` under 500 lines; depth moved to `references/`
- [ ] Language Policy section present (if multilingual)
