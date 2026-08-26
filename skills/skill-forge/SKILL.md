---
name: skill-forge
description: Creates, critiques, converts, and explains prompts, system prompts, skills, function/tool schemas, and rules files for any AI platform. Content is written in English; user-facing output adapts to English, Vietnamese, or any detected language.
version: 3.0.0
tags: [prompt, system-prompt, user-prompt, function-calling, tool-schema, skill, rules, critique, convert, explain, multilingual]
---

# Skill Forge

A skill for **creating, critiquing, converting, and explaining** prompt artifacts for AI agents and LLM applications: system prompts, user prompts, function/tool schemas, skills (SKILL.md), and rules files.

> **Language policy** (see [Multilingual](#multilingual)): The skill's own instructions are always in English. User-facing output adapts to one of three buckets — English, Vietnamese, or any other detected language.

---

## When to Activate

Activate when the user:
- Asks to **create** a prompt, system prompt, skill, function/tool definition, or rules file
- Wants to **improve, review, or critique** an existing prompt or schema
- Needs to **convert** a prompt or schema from one platform to another
- Asks how to write a rules file (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.cursorrules`, `.mdc`)
- Wants an **explanation** of a prompt pattern or technique

**Trigger keywords**: `prompt`, `system prompt`, `user prompt`, `skill`, `function calling`, `tool schema`, `tool definition`, `rules file`, `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `critique`, `improve prompt`, `tạo prompt`, `système prompt`, `プロンプト`, `提示词`

---

## Workflow Overview

Run this decision flow first, then follow the matching MODE section.

```
User Input
  │
  ├── Detect MODE
  │     CREATE   → build from scratch
  │     CRITIQUE → review + auto-improve existing input
  │     CONVERT  → translate to a different platform format
  │     EXPLAIN  → clarify a pattern, technique, or concept
  │
  ├── Detect OUTPUT TYPE
  │     System Prompt | User Prompt | Function/Tool Schema | AGY Skill | Rules File
  │
  ├── Detect PLATFORM
  │     Claude/Anthropic | OpenAI/GPT | Gemini/Google | MCP | Platform-agnostic (default)
  │
  ├── Detect LANGUAGE BUCKET  → English | Vietnamese | Other (fallback English)
  │
  └── Execute the MODE → output in the user's language bucket
```

---

## Multilingual

The skill responds in the language the user writes in, bucketed into three groups. Only **user-facing output** (prompts, explanations, follow-up questions) follows the bucket; internal processing and the skill's own instructions stay in English.

| User language | Skill responds in |
|---|---|
| English | English |
| Vietnamese | Vietnamese |
| Any other detected language (Japanese, French, ...) | That language |
| Undetected / ambiguous | English (default) |

**For generated artifacts**: the artifact's language follows the user's request, defaulting to English if unspecified. If unclear, ask: *"Should the artifact be in English, or in your language?"*

---

## MODE: CREATE — Build from Scratch

### Step 1: Gather Requirements

Infer from context first; ask in the user's language only if genuinely missing:
1. **Output type** — system prompt / user prompt / function schema / skill / rules file
2. **Use case / domain** — what it does, and in what context
3. **Target platform** — Claude / OpenAI / Gemini / MCP / platform-agnostic
4. **Tone** — professional / friendly / technical / casual
5. **Language** — what language the artifact should be written in
6. **Constraints** — topic scope, forbidden actions, output length

> **Default platform**: platform-agnostic (standard JSON Schema, Markdown + optional XML tags) — portable to any platform.

### Step 2: Build by Output Type

Templates below are platform-agnostic. For platform-specific variants, see the linked reference files.

#### System Prompt
```
# Role & Identity
[Who the assistant is — specific, not generic]

# Core Capabilities
[What it can do — bullet list]

# Communication Style
[Tone, language, format, and length]

# Constraints
[What it must NOT do — stated as concrete actions]

# Context
[App/environment info if relevant]
```
Platform variants → `references/system-prompt-guide.md`

#### User Prompt
```
[Context / Background if needed]

[Task instruction — clear and specific]

[Format requirements if applicable]

[Examples if helpful — inside <examples> tags for Claude]

[Constraints or edge cases]
```
Steering patterns → `references/prompt-patterns.md`

#### Function / Tool Schema
```json
{
  "name": "verb_noun_snake_case",
  "description": "What it does. When to call: [trigger]. Returns: [what].",
  "parameters": {
    "type": "object",
    "properties": {
      "param_name": {
        "type": "string|number|integer|boolean|array|object",
        "description": "What value to provide. Format: [if non-obvious]."
      }
    },
    "required": ["required_params"],
    "additionalProperties": false
  }
}
```
Platform schemas → `references/function-schema-guide.md`

#### AGY Skill (SKILL.md)
```markdown
---
name: skill-name
description: One-sentence description for discovery
version: 1.0.0
---

# Skill Name

## When to Activate
[Keywords and trigger conditions]

## Workflow
[Step-by-step instructions]

## Examples
[Concrete examples with inputs and outputs]

## References
[Links to related files]
```
Creation guide → `references/skill-guide.md`

#### Rules File (CLAUDE.md / AGENTS.md / GEMINI.md / .mdc / .cursorrules)
```markdown
# Project / Domain Name

## Overview / Identity
[Brief description]

## Code Style / Conventions
[Specific rules]

## Architecture / Structure
[Where things live, patterns to follow]

## Common Commands
[Build, test, deploy commands]

## Constraints
[NEVER do X. ALWAYS do Y.]
```
Rules guide → `references/rules-guide.md`

### Quality Gates (all output types)

- [ ] Role/identity is specific (not just "be helpful")
- [ ] Capabilities clearly enumerated
- [ ] Tone explicitly defined
- [ ] Constraints are concrete actions, not vague negations
- [ ] No contradictory instructions
- [ ] Output format guidance present (length, structure, style)
- [ ] Artifact language matches user's request

---

## MODE: CRITIQUE & IMPROVE — Review and Auto-Improve

### Process

1. **Analyze** the input against: *Clarity* (unambiguous to a new reader?), *Completeness*, *Consistency* (no contradictions), *Specificity* (concrete vs generic), *Format fit* (platform-appropriate), *Language consistency*.
2. **Auto-fix** issues that can be improved unambiguously.
3. **Always output three sections** (in the user's language):

```
## 🔧 Changes Made
- Changed "[old text]" → "[new text]" because [reason]
- Added [element] because [reason]
- Removed [element] because [reason]

## ✅ Improved Version
[The improved prompt / schema]

## 💡 Suggested Additions
- Consider adding: [specific missing info]
- Optional improvement: [enhancement idea]
- Needs clarification: [ambiguity that remains]
```

### Evaluation Criteria

| Criterion | Check Question |
|---|---|
| Clarity | Would a new reader understand it without extra context? |
| Role specificity | Is the role more specific than "be helpful"? |
| Tone definition | Is the tone explicitly described? |
| Concrete constraints | Are forbidden actions stated as specific behaviors? |
| Format guidance | Is output format (length, structure, style) specified? |
| No contradictions | Do any instructions conflict? |
| Platform fit | Does it use platform features correctly? |
| Language consistency | Is the language consistent and appropriate? |

### Prefer Positive Instructions

State what to do, not what to avoid:

| ❌ Avoid | ✅ Prefer |
|---|---|
| "Don't use bullet points" | "Write in flowing prose paragraphs." |
| "Do not use markdown" | "Write in plain text, no markdown syntax." |
| "Be helpful" | "Give concrete, actionable answers in the user's language." |

---

## MODE: CONVERT — Cross-Platform Translation

### System Prompt Mapping

| From → To | Key Changes |
|---|---|
| OpenAI → Claude | Add XML tags; allow more nuanced tone |
| Claude → OpenAI | Remove XML wrapper tags if needed; keep plain Markdown |
| Any → Gemini | Reformat for the `systemInstruction` field |
| Any → Platform-agnostic | Remove all platform-specific syntax |

### Function / Tool Schema Mapping

| From → To | Key Changes |
|---|---|
| OpenAI → Anthropic | `parameters` → `input_schema`; remove `type:"function"` wrapper; remove `strict` |
| OpenAI → MCP | `parameters` → `inputSchema`; add optional `title`; optional `outputSchema` |
| OpenAI → Gemini | Same structure; make type names UPPERCASE (`STRING`, `OBJECT`, `ARRAY`, `INTEGER`, `BOOLEAN`, `NUMBER`) |
| Anthropic → OpenAI | `input_schema` → `parameters`; add `type:"function"` + `name` at root |
| MCP → OpenAI | `inputSchema` → `parameters`; add `type:"function"` wrapper |
| Gemini → OpenAI | UPPERCASE type names → lowercase; wrap with `type:"function"` + `name` |

### MCP Specifics

- Tools are exposed over JSON-RPC 2.0 (not a REST wrapper).
- Schema field is `inputSchema`; optional `title` (human-readable label) and `outputSchema`.
- Root is the direct tool object (no `type:"function"` wrapper).

### Output Format

```
## Converted [Type] — [Source] → [Target]

**Changes made:**
- [specific change 1]
- [specific change 2]

**Result:**
[converted output]

**Notes:**
[Platform-specific caveats or features gained/lost in conversion]
```

---

## MODE: EXPLAIN — Clarify Concepts

When the user asks "Why use...", "How does... work", "What's the difference between...":

1. **Explain** the concept in plain language at the user's level
2. **Give a concrete example** (before/after or good/bad comparison)
3. **Link to related patterns** in the reference files
4. **Note when to use / when not to use**

---

## Quick-Reference Comparison Tables

### System Prompts by Platform

| Platform | Format | Tone Default | Special Features |
|---|---|---|---|
| Claude | XML tags supported | Thoughtful, nuanced | `<thinking>` blocks, adaptive reasoning |
| OpenAI | Plain Markdown | Direct, helpful | JSON mode, strict function calling |
| Gemini | `systemInstruction` | Helpful, versatile | Multi-modal, grounding |
| Platform-agnostic | Markdown + optional XML | Configurable | Portable to any platform |

### Function / Tool Schemas by Platform

| Platform | Root wrapper | Schema field | Strict mode | Type case |
|---|---|---|---|---|
| OpenAI | `type:"function"` required | `parameters` | `strict: true` | lowercase |
| Anthropic | None (direct object) | `input_schema` | No (use `required` + schema) | lowercase |
| MCP | None (direct object) | `inputSchema` | No | lowercase |
| Gemini | None (direct object) | `parameters` | No | **UPPERCASE** |

### JSON Schema Type Reference

| Type | Description | Example |
|---|---|---|
| `string` | Text value | `"Paris, France"` |
| `number` | Decimal number | `3.14` |
| `integer` | Whole number | `42` |
| `boolean` | True / false | `true` |
| `array` | Ordered list | `["a","b"]` |
| `object` | Key-value map | `{"key":"value"}` |
| `null` | Null value | `null` |

### Rules Files by Platform

| File | Platform | Auto-loaded | Scope | Glob support |
|---|---|---|---|---|
| `CLAUDE.md` | Claude / AGY | Yes | Project-wide | No |
| `GEMINI.md` | AGY (Antigravity IDE) | Yes | Project-wide | No |
| `AGENTS.md` | Generic agents | Yes | Project-wide | No |
| `.cursor/rules/*.mdc` | Cursor IDE | On file match | File-specific | Yes |
| `.cursorrules` | Cursor (legacy) | Yes | Global | No |

---

## Best-Practice Rules

- **Be clear and direct.** Think of the model as a smart new hire lacking your norms — if a colleague would be confused, the model will be too.
- **Explain *why* a behavior matters**, not just *what* to do.
- **Use few-shot examples** (2–5) to steer format, tone, and structure; wrap them in `<examples>` / `<example>` tags.
- **Structure complex prompts with XML tags**: `<instructions>`, `<context>`, `<input>`, `<examples>`, `<thinking>`, `<answer>`.
- **Give a role** — even one sentence improves performance.
- **Long context (20k+ tokens):** put longform data at the top, wrap each doc in `<document>` tags, and ground answers in quoted source material.
- **Name parameters with snake_case**, make `description` explain *what* and *when*, use `enum` for constrained values, keep `additionalProperties: false` for strict schemas.

---

## Reference Files Index

| File | Contents |
|---|---|
| `references/prompt-engineering-official.md` | Anthropic official best practices (fetched 2026-08) |
| `references/openai-function-calling.md` | OpenAI function calling schema reference |
| `references/mcp-tool-spec.md` | MCP tool specification (v2026-07-28) |
| `references/prompt-patterns.md` | Common prompt patterns (CoT, few-shot, etc.) |
| `references/system-prompt-guide.md` | System prompt templates for all platforms |
| `references/function-schema-guide.md` | Cross-platform function schema comparison |
| `references/skill-guide.md` | AGY Skill (SKILL.md) creation guide |
| `references/rules-guide.md` | Rules file guide (CLAUDE.md, .mdc, etc.) |

---

## Examples

### Example 1: CREATE — System Prompt (English input)

**Input**: "Create a system prompt for an English tutoring chatbot for Vietnamese learners"

**Process**: Mode=CREATE · Type=System Prompt · Platform=platform-agnostic · Domain=English tutoring for Vietnamese speakers

**Output**:
```
# Role & Identity
You are EnglishPal, a friendly and patient English language tutor specializing in
helping Vietnamese learners build conversational fluency and grammar confidence.

# Core Capabilities
- Hold natural English conversations calibrated to the learner's level
- Provide gentle, specific corrections with clear explanations
- Explain grammar rules using simple language and relatable examples
- Suggest vocabulary alternatives, collocations, and idioms
- Give pronunciation tips when relevant

# Communication Style
Warm and encouraging — mistakes are learning opportunities, not failures.
Keep explanations concise; offer to expand when the learner wants more depth.
Use Vietnamese only when the learner is completely stuck.

# Constraints
- Do not do homework for learners; guide them toward the answer
- Do not correct every single error — focus on recurring patterns
- Do not default to Vietnamese; only use it as a last resort

# Context
Embedded in an English learning mobile app used primarily by Vietnamese university
students. Users range from beginner (A1) to upper-intermediate (B2).
```

### Example 2: CRITIQUE — Input in French (demonstrating multilingual support)

**Input** (French): `Tu es un assistant utile. Aide les utilisateurs. Ne dis pas de mauvaises choses.`

**Output** (French):

## 🔧 Modifications Apportées
- Remplacé "assistant utile" → rôle plus spécifique, car "assistant utile" est trop générique
- Ajouté la section **Capacités** car les actions possibles n'étaient pas claires
- Remplacé "Ne dis pas de mauvaises choses" → contraintes spécifiques basées sur l'action, car les négations vagues sont inefficaces
- Ajouté des instructions sur le **Style de communication** car elles étaient totalement absentes

## ✅ Version Améliorée
```
# Rôle
Vous êtes un assistant généraliste aidant les utilisateurs dans la recherche, la rédaction,
l'analyse et les questions quotidiennes.

# Capacités
- Répondre aux questions factuelles avec des informations précises
- Aider à rédiger, éditer et améliorer le contenu écrit
- Expliquer des sujets complexes de manière claire
- Aider à l'analyse et à la résolution de problèmes

# Style de Communication
Chaleureux et professionnel. Adaptez la profondeur technique au niveau d'expertise apparent
de l'utilisateur. Réponses concises par défaut ; proposez de développer pour les sujets complexes.

# Contraintes
- Ne donnez pas de conseils médicaux, juridiques ou financiers à la place de professionnels
- Ne générez pas de contenu susceptible de causer des dommages ou de propager des informations erronées
- En cas de doute, reconnaissez clairement vos limites
```

## 💡 Ajouts Suggérés
- À ajouter : Informations sur l'application ou les utilisateurs cibles
- Optionnel : Préférences de formatage (longueur, utilisation de markdown)
- À clarifier : Y a-t-il des restrictions de sujets spécifiques ?

### Example 3: CONVERT — Function Schema

**Input** (OpenAI):
```json
{
  "type": "function",
  "name": "send_email",
  "description": "Sends an email",
  "parameters": {
    "type": "object",
    "properties": {
      "to": {"type": "string"},
      "subject": {"type": "string"},
      "body": {"type": "string"}
    },
    "required": ["to", "subject", "body"],
    "additionalProperties": false
  },
  "strict": true
}
```

**Request**: Convert to Anthropic format

**Output**:

## Converted Function Schema — OpenAI → Anthropic

**Changes made:**
- Removed `type: "function"` wrapper (Anthropic uses top-level `name` directly)
- Renamed `parameters` → `input_schema`
- Removed `strict` (not supported; schema handles this via `required`)
- Enhanced parameter descriptions (recommended for Anthropic for better comprehension)

**Result:**
```json
{
  "name": "send_email",
  "description": "Sends an email to a specified recipient. Use when the user explicitly requests sending an email.",
  "input_schema": {
    "type": "object",
    "properties": {
      "to": {"type": "string", "description": "Recipient email address (e.g. user@example.com)"},
      "subject": {"type": "string", "description": "Email subject line"},
      "body": {"type": "string", "description": "Full email body content, plain text or HTML"}
    },
    "required": ["to", "subject", "body"]
  }
}
```

**Notes:** Improved descriptions for all parameters — Anthropic models perform better with richer parameter descriptions.
