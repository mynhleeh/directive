---
name: skill-forge
description: "Meta-orchestrator for the directive knowledge base: generates, critiques, converts, explains, distills, and navigates AI artifact types (SKILL.md skills, system/user prompts, function schemas, rules files). Use whenever the user wants to create, improve, port, understand, or distill any prompt-related artifact or skill for any AI platform. Make sure to use this skill whenever the user mentions prompts, system prompts, user prompts, skills, function calling, tool schemas, rules files, CLAUDE.md, AGENTS.md, .cursorrules, .mdc, prompt frameworks, or wants to turn existing content/repos into reusable artifacts — even if they don't explicitly ask for a 'skill'."
version: 2.0.0
tags: [meta-skill, orchestrator, prompt, system-prompt, user-prompt, function-calling, tool-schema, skill, rules, critique, convert, explain, distill, navigate, multilingual]
license: MIT
compatibility: [any-agent, claude, openai, gemini, mcp, cursor, agy]
---

# Skill Forge

A **meta-orchestrator** that distills the entire `directive` knowledge base into one brain capable of **generating**, **critiquing**, **converting**, **explaining**, **distilling**, and **navigating** AI artifacts — skills, prompts, function schemas, and rules files — for any domain, any platform, and any language.

> **Language policy** (see [Language Policy](#language-policy)): The skill's own instructions are always in English. User-facing output adapts to the user's language (English / Vietnamese / any other detected language). Generated artifacts follow `references/house-language-policy.md`.

---

## When to Activate

Activate when the user:
- Wants to **CREATE** an artifact (skill / prompt / function schema / rules file)
- Wants to **CRITIQUE & IMPROVE** an existing prompt or schema
- Wants to **CONVERT** an artifact across platforms (OpenAI ↔ Anthropic ↔ MCP ↔ Gemini ↔ platform-agnostic)
- Wants an **EXPLANATION** of a pattern, technique, or concept
- Wants to **DISTILL** existing content (a conversation, a corpus, a repo) into a new artifact or skill family
- Wants to **NAVIGATE / ORGANIZE** content using the repo's 3-axis taxonomy
- Is working with **AI commanding** — turning instructions into repeatable, machine-usable artifacts

**Trigger keywords**: `prompt`, `system prompt`, `user prompt`, `skill`, `SKILL.md`, `function calling`, `tool schema`, `tool definition`, `rules file`, `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.cursorrules`, `.mdc`, `MCP`, `critique`, `convert`, `distill`, `tạo skill`, `tạo prompt`, `système prompt`, `プロンプト`, `提示词`

---

## Workflow Pipeline

Run this decision flow once, then follow the matching MODE section. Every artifact is produced through the same six-stage pipeline:

```
User Input
  │
  ├── STAGE 1: UNDERSTAND THE NEED
  │     What outcome does the user want? (create / critique / convert / explain / distill / navigate)
  │
  ├── STAGE 2: CLASSIFY ARTIFACT TYPE
  │     skill | system prompt | user prompt | function/tool schema | rules file
  │
  ├── STAGE 3: SELECT INTENSITY TIER
  │     micro | standard | deep engine   → see references/domain-engine-tiers.md
  │
  ├── STAGE 4: SELECT RECIPE
  │     Which reference file holds the exact recipe for this artifact type?
  │
  ├── STAGE 5: GENERATE
  │     Produce the artifact following the House Contract
  │     (frontmatter · language policy · structure conventions)
  │
  └── STAGE 6: VALIDATE
        Run the quality checklist for the artifact type
```

---

## Language Policy

The skill responds in the user's language, bucketed into three groups. Only **user-facing output** follows the bucket; internal processing and the skill's own instructions stay in English.

| User language | Skill responds in |
|---|---|
| English | English |
| Vietnamese | Vietnamese |
| Any other detected language (Japanese, French, ...) | That language |
| Undetected / ambiguous | English (default) |

**For generated artifacts**: the artifact's language follows the user's request, defaulting to English if unspecified. Internal `references/` files remain English per `references/house-language-policy.md`. If unclear, ask: *"Should the artifact be in English, or in your language?"*

---

## MODE: CREATE — Build from Scratch

### Routing

Determine **artifact type**, then **intensity tier**, then **platform**. Infer from context first; ask in the user's language only if genuinely missing.

| Signal | Options | Reference |
|---|---|---|
| **Artifact type** | skill / system prompt / user prompt / function schema / rules file | See per-type recipe below |
| **Intensity tier** | micro / standard / deep engine | `references/domain-engine-tiers.md` |
| **Platform** | Claude / OpenAI / Gemini / MCP / platform-agnostic (default) | `references/system-prompt-guide.md`, `references/function-schema-guide.md` |
| **Language** | English / Vietnamese / other (follow user) | `references/house-language-policy.md` |

> The **intensity tier** is the biggest structural lever. A micro skill is a single self-contained file; a deep engine is adaptive and stateful with lazy-loaded `references/`. Pick it before writing.

### Per-Type Recipe

Each type has a recipe + a canonical reference. Emit the artifact **in a single output block** (see `references/house-structure-conventions.md`).

#### Skill (SKILL.md)
Follow `references/skill-guide.md` + `references/house-structure-conventions.md`.

```markdown
---
name: skill-name
description: "Trigger-optimized: what it does AND when to trigger."
version: 1.0.0
tags: [...]
---

# {Display Name}

## When to Activate
[...]

## Overview
[...]

## Instructions
[Step-by-step, imperative]

## Output Contract
[Single block — what to emit, and only that]

## Anti-Examples
| ❌ Avoid | ✅ Prefer | Why |
[...]

## References
[Relative paths with "when to read this"]
```

#### System Prompt
Follow `references/system-prompt-guide.md`. Include the 5-slot anatomy (Role, Capabilities, Constraints, Style, Context); choose platform serialization.

#### User Prompt
Follow `references/user-prompt-guide.md`. Cover Need, Artifact type, Intensity tier, Domain.

#### Function / Tool Schema
Follow `references/function-schema-guide.md`. Action-prefixed names, WHAT + WHEN, `required`, `additionalProperties: false` for strict; add `outputSchema` for MCP.

#### Rules File
Follow `references/rules-guide.md`. Karpathy 4-principle skeleton; single-source-to-multi-format sync.

### Quality Gates (all types)
Cross-check `references/house-structure-conventions.md`:
- [ ] Frontmatter follows House Frontmatter Contract (name matches dir, trigger description)
- [ ] Role/identity is specific (not just "be helpful")
- [ ] Constraints are concrete actions, not vague negations
- [ ] Output format explicitly declared (single block)
- [ ] Intensity tier actually matches the depth of the artifact
- [ ] No contradictions; language consistent
- [ ] Under 500 lines; depth moved to `references/` (progressive disclosure)

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

## MODE: DISTILL — Turn Content Into Artifacts

Distill existing content (a conversation, a corpus, a repo, a doc) into a reusable artifact or a **skill family**. This is the meta-skill acting on itself — the same process that created this knowledge base.

### Skill Distillation Flow
1. **Capture intent** — extract the workflow from the source: tools/actions used, step sequence, corrections, input/output formats.
2. **Classify** — what artifact type(s) emerge from the source?
3. **Select tier** — single task (micro) / 2–5 workflows (standard) / adaptive multi-phase (deep engine).
4. **Abstract the pattern** — separate the *reusable shape* (structure, contract, anti-examples) from the *domain-specific content*.
5. **Emit per House Contract** — follow frontmatter / language / structure conventions.
6. **Validate** — run the quality checklist.

### Skill Family Distillation
When a source produces multiple related artifacts, emit a **family**: a parent `SKILL.md` that selects across variants, plus `references/<variant>.md` for each. This is the multi-domain organization pattern (see `references/skill-guide.md` → progressive disclosure).

> **Critical rule**: Distill **patterns and templates**, never verbatim copy. External/Tier-5 material (leaked prompts, third-party submodules) is unverified — do not promote it into a premise. Generated content must be newly authored abstracted patterns.

---

## MODE: NAVIGATE / ORGANIZE — Classify and Place Content

Use the repo's 3-axis taxonomy to classify and place content. See `references/taxonomy-navigation.md`.

### Classify a Resource
```
Q1: Feed directly to an AI agent to execute?  → instructions/
Q2: Read to learn about AI / prompting?      → knowledge/
Q3: Design, architecture, or mental model?   → blueprints/
```

### Route Citations by Source Hierarchy
Always cite the **source tier** when referencing content. Prefer `knowledge/papers/` (Tier 1) > docs/specs (Tier 2) > guides (Tier 3) > articles (Tier 4) > external submodules (Tier 5) > active (Tier 6) > archive (Tier 7).

### Organize (active / archive / external)
- `active/` and `archive/` → **self-created only**.
- `external/` — **third-party only**. Remove (un-track) it when no longer needed; do NOT move to `archive/`.

---

## Quick-Reference Comparison Tables

Platform mapping (system prompts, function/tool schemas, JSON types, rules files) lives in the reference guides. Read the relevant one before authoring or converting a cross-platform artifact:

- **System prompt / platform matrix** → `references/system-prompt-guide.md`
- **Function / tool schema matrix** → `references/function-schema-guide.md` + `references/openai-function-calling.md`
- **Rules file platform matrix** → `references/rules-guide.md`
- **MCP specifics** → `references/mcp-tool-spec.md`

---

## Best-Practice Rules

- **Be clear and direct.** Think of the model as a smart new hire lacking your norms — if a colleague would be confused, the model will be too.
- **Explain *why* a behavior matters**, not just *what* to do.
- **Use few-shot examples** (2–5) to steer format, tone, and structure; wrap them in `<examples>` / `<example>` tags.
- **Structure complex prompts with XML tags**: `<instructions>`, `<context>`, `<input>`, `<examples>`, `<thinking>`, `<answer>`.
- **Give a role** — even one sentence improves performance.
- **Apply progressive disclosure**: keep `SKILL.md` under 500 lines; push depth into `references/`.
- **Never copy submodule/external content verbatim** — extract patterns only (Tier 5 is unverified).
- **State the chosen default** (platform/tier/language) back to the user so they can correct them. Note: the original best practices here also recommend long-context handling (top-load data, `document` tags, grounded answers) and schema naming (`snake_case`, WHAT+WHEN descriptions, `enum` for constrained values, `additionalProperties: false` for strict schemas) — keep those in mind for EXPERT-level artifacts.
- **Parameter naming** (`snake_case`), **enum for constrained values**, and **`additionalProperties: false` for strict schemas** — see `references/function-schema-guide.md`.

---

## Reference Files Index

| File | Contents | Read when |
|---|---|---|
| `references/house-frontmatter-contract.md` | Unified YAML schema: `name`/`description`/`version`/`tags`/`license`/`compatibility`; trigger-optimized description anatomy; validation checklist | Every create/rewrite of a skill |
| `references/house-language-policy.md` | English internal / user-language output; language buckets; artifact vs output distinction | Every multilingual artifact |
| `references/house-structure-conventions.md` | Unified SKILL.md skeleton; progressive disclosure; lazy-loaded `references/`; output contract; anti-example table | Every skill |
| `references/taxonomy-navigation.md` | 3-axis taxonomy; decision tree; Tier 1–7; MECE active/archive/external boundary | NAVIGATE/ORGANIZE, citation routing |
| `references/domain-engine-tiers.md` | micro / standard / deep engine tiers; decision tree; lazy-load rule | Selecting intensity tier |
| `references/prompt-framework-costar-x.md` | COSTAR-X framework; `<variable>` isolation; mandatory `<thinking>`; startup line | Authoring/porting prompts |
| `references/user-prompt-guide.md` | How the user should phrase a request; the 4 routing signals | CREATE (user prompt), routing |
| `references/skill-guide.md` | AGY skill creation guide; frontmatter; sizing; progressive disclosure; skill-creator workflow | CREATE (skill) |
| `references/rules-guide.md` | Rules file guide; platform matrix; Karpathy 4-principle skeleton; multi-format sync | CREATE (rules) |
| `references/system-prompt-guide.md` | System prompt templates; 5-slot anatomy; agent-vs-assistant; XML vs Markdown | CREATE / CONVERT (system prompt) |
| `references/function-schema-guide.md` | Cross-platform schema comparison; MCP conventions; `outputSchema`; `Prompt.txt`+`Tools.json` | CREATE / CONVERT (schema) |
| `references/openai-function-calling.md` | OpenAI function calling schema, strict mode | CONVERT (schema) |
| `references/mcp-tool-spec.md` | MCP tool specification | CREATE / CONVERT (MCP) |
| `references/prompt-patterns.md` | 10 prompt patterns + anti-patterns | CREATE / EXPLAIN (prompt) |
| `references/prompt-engineering-official.md` | Anthropic official best practices | CREATE / EXPLAIN (all) |

---

## Examples

### Example 1: CREATE — System Prompt (English input)

**Input**: "Create a system prompt for an English tutoring chatbot for Vietnamese learners"

**Process**: Mode=CREATE · Type=System Prompt · Platform=platform-agnostic · Tier=standard

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
- Remplacé "Ne dis pas de mauvaises choses" → contraintes basées sur l'action, car les négations vagues sont inefficaces
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

# Style de Communication
Chaleureux et professionnel. Adaptez la profondeur technique au niveau d'expertise de l'utilisateur.

# Contraintes
- Ne donnez pas de conseils médicaux, juridiques ou financiers à la place de professionnels
- En cas de doute, reconnaissez clairement vos limites
```

## 💡 Ajouts Suggérés
- À ajouter : Informations sur l'application ou les utilisateurs cibles
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

### Example 4: DISTILL — Turn a Conversation into a Skill

**Input** (English): "Turn this debugging approach I keep repeating into a skill."

**Process**: Mode=DISTILL · Classify=skill · Tier=standard · Abstract the step sequence, output contract, and anti-examples from the repeated workflow.

**Output**: A `SKILL.md` with `## When to Activate`, imperative `## Instructions`, an `## Output Contract` block, and a ❌/✅ `## Anti-Examples` table — emitted per the House Contract.

### Example 5: NAVIGATE — Classify a Resource

**Input**: "Where does this AGENTS.md rule file belong?"

**Process**: Feed to AI to execute? Yes → `instructions/`. Rules file → `instructions/rules/`. Third-party? No → `active/`.

**Output**: `instructions/rules/active/` (self-created, always-on rules file).
