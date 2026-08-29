---
name: skill-forge
description: "Authoring engine for the directive knowledge base: create, critique, port, distill, or understand any AI artifact — skills (SKILL.md), system/user prompts, function/tool schemas, rules files (CLAUDE.md, AGENTS.md, GEMINI.md, .cursorrules, .mdc), MCP tools — for any domain, platform (Claude, OpenAI, Gemini, Cursor, MCP), or language. Trigger whenever the user asks to write, improve, convert, explain, or extract a prompt/skill/schema/rules artifact, or to turn a conversation or repo into reusable artifacts — e.g. 'viết prompt', 'tạo skill', 'critique this prompt', 'convert this schema', 'distill this conversation'. Do NOT trigger for ordinary coding questions, runtime debugging, or a generic concept question with no artifact to create or convert."
version: 4.0.0
tags: [meta-skill, orchestrator, prompt, system-prompt, user-prompt, function-calling, tool-schema, skill, rules, critique, convert, explain, distill, navigate, multilingual, reasoning, chain-of-thought, audit, weak-model-first, behavioral-testing, red-green-refactor, iron-law, sdo]
compatibility: "Any agent (Claude, OpenAI, Gemini, MCP, Cursor, AGY). Weak-model-first: every rule is mechanical and countable so average models comply; stronger models can only exceed the floor."
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

> **Do NOT trigger** for:
> - Ordinary coding questions / feature requests (use a normal coding agent).
> - Runtime debugging, error diagnosis, concept explanation, or project onboarding (use `tech-mentor`).

---

## Workflow Pipeline

Every request runs the same pipeline. **Do not skip a stage; do not merge two stages into one pass.** The pipeline is a reasoning + verification loop, not a linear emit. Each stage has a countable outcome so a weak model cannot skip it silently:

```
User Input
  │
  ├─ STAGE 1: PARSE
  │     Restate the request in ≤2 lines. Classify: mode · artifact type · intensity tier ·
  │     platform · language. Split inputs into KNOWN (present) vs AMBIGUOUS/MISSING.
  │
  ├─ GATE: CLARIFY
  │     Ambiguous or missing? → STOP and ask (max 3 questions, one batch, each with a
  │     default option). Clear? → proceed. NEVER invent data (Principle 3).
  │
  ├─ STAGE 2: THINK (long chain-of-thought)
  │     Reason through the mode's fixed sub-questions (see references/execution-protocol.md),
  │     including the test-plan design (scenario + pressures + compliance criteria,
  │     see references/behavioral-testing.md). Do not skip or merge sub-questions.
  │     End with a compact ## Working Notes block: routing decision + test plan +
  │     one-line rationale each. The block is the ONLY visible trace of thinking.
  │
  ├─ STAGE 3: BASELINE TEST (RED — Iron Law)
  │     Run the failing test BEFORE writing: pressure scenario (skills/rules) or
  │     fresh-context run (prompts/schemas) WITHOUT the artifact. Record rationalizations
  │     verbatim in Working Notes. NO ARTIFACT WITHOUT A FAILING TEST FIRST.
  │
  ├─ STAGE 4: GENERATE
  │     Produce the artifact addressing the documented baseline failures. Mechanical,
  │     countable rules only — no "make it better" language.
  │
  ├─ STAGE 5: EVALUATE (stranger-review)
  │     Re-read the artifact as a stranger reviewing someone else's work — never in the
  │     same pass that wrote it. Run every countable criterion: PASS/FAIL + fix recipe.
  │
  ├─ STAGE 6: TEST — GREEN ⇄ REFACTOR
  │     Re-run the STAGE 3 scenario WITH the artifact → agent must comply (GREEN).
  │     New rationalization? → REFACTOR: explicit negation, rationalization table,
  │     red flags, description violation symptoms (references/behavioral-testing.md).
  │     Acceptance criteria from STAGE 1 · neutrality · trigger test · consistency.
  │
  ├─ LOOP: STAGE 5 ⇄ STAGE 6 (max 2 iterations)
  │     Apply fixes → re-audit → re-test. Over the cap → emit with residual defects flagged.
  │
  └─ STAGE 7: EMIT
        Output block only (per output contract). State assumptions/defaults used.
        Offer exactly one follow-up.
```

---

## Language Policy

The skill responds in the user's language, bucketed into three groups. Only **user-facing output** follows the bucket; internal processing and the skill's own instructions stay in English.

| User language | Skill responds in |
|---|---|
| English | English |
| Vietnamese | Vietnamese |
| Any other detected language (Japanese, French, ...) | That language |
| Undetected / ambiguous | Ask one question at the CLARIFY gate (default option: English) |

**For generated artifacts**: the artifact's language follows the user's request, defaulting to English if unspecified. Internal `references/` files remain English per `references/house-language-policy.md`. If unclear, ask at the CLARIFY gate: *"Should the artifact be in English, or in your language?"*

---

## Reasoning Principles

Every artifact passes through these six principles. **They outrank any instruction below** — if a rule in a MODE section conflicts with a principle here, the principle wins and the conflict must be fixed or flagged, never silently ignored.

1. **Weak-model-first.** Assume the user runs an average-to-weak model. Every rule must therefore be **mechanical and countable** — a number, a pass/fail boundary, a fixed recipe — never "use good judgment." A stronger model can only do better; the rules are a floor, not a ceiling.
2. **Reasoning scales, rules do not.** Author *principles*, not hardcoded lists. When the user supplies one specific situation or example, transmute it into a general rule that applies to all similar cases — never tailor the artifact to a single instance (see DISTILL).
3. **Ask, don't invent.** Never fabricate missing data. If any input is ambiguous, missing, or doubtful, stop at the CLARIFY gate and ask (max 3 questions, one batch, each with a default option). If nothing is ambiguous, proceed without asking (Principle 4).
4. **Do exactly what's asked.** Deliver precisely the requested artifact — no scope creep, no extra sections, no unsolicited rewrites. Anything beyond the request belongs in Suggested Additions, not in the output.
5. **Source-grounded.** Every factual claim in a generated artifact must trace to the user's input or a cited source tier (see `references/taxonomy-navigation.md`). Never promote unverified external material (Tier 5) into a premise.
6. **Single source of truth.** This `SKILL.md` wins over its `references/`. When two instructions conflict, the one higher in this file wins — and the conflict must be fixed or flagged, never silently ignored.

---

## MODE: CREATE — Build from Scratch

### Routing

Determine **artifact type**, then **intensity tier**, then **platform** (Principle 4: do exactly what's asked — only infer the minimum needed to route). Infer from context first; ask at the CLARIFY gate only when a routing signal is genuinely missing (Principle 3). State your routing back in the Working Notes block.

| Signal | Options | Reference |
|---|---|---|
| **Artifact type** | skill / system prompt / user prompt / function schema / rules file | See per-type recipe below |
| **Intensity tier** | micro / standard / deep engine | `references/domain-engine-tiers.md` |
| **Platform** | Claude / OpenAI / Gemini / MCP / platform-agnostic (default) | `references/system-prompt-guide.md`, `references/function-schema-guide.md` |
| **Language** | English / Vietnamese / other (follow user) | `references/house-language-policy.md` |

> The **intensity tier** is the biggest structural lever. A micro skill is a single self-contained file; a deep engine is adaptive and stateful with lazy-loaded `references/`. Pick it before writing.

> **Test-first (Iron Law)**: before writing any artifact, design and run the failing test (STAGE 3 BASELINE TEST) — pressure scenario for skills/rules, fresh-context run for prompts/schemas. Record rationalizations verbatim; they are the spec the artifact must defeat. Full procedure in `references/behavioral-testing.md`.

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

## Common Issues
[Known failure modes + fixes]

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
Cross-check `references/house-structure-conventions.md` in the EVALUATE stage (stranger-review, never the writing pass):
- [ ] Frontmatter follows House Frontmatter Contract (name matches dir, trigger description)
- [ ] Role/identity is specific (not just "be helpful")
- [ ] Constraints are concrete actions, not vague negations — each has a countable pass/fail boundary
- [ ] Output format explicitly declared (single block)
- [ ] Intensity tier actually matches the depth of the artifact
- [ ] No contradictions; language consistent
- [ ] Under 500 lines; depth moved to `references/` (progressive disclosure)
- [ ] Examples are neutral and generalized — no domain-specific names or single-case hardcodes (Principle 2)
- [ ] Every rule is mechanical and countable — a weak model can execute it without judgment calls (Principle 1)
- [ ] Every claim traces to user input or a cited source tier (Principle 5)
- [ ] Baseline test ran BEFORE writing (Iron Law) — rationalizations recorded verbatim (see `references/behavioral-testing.md`)
- [ ] Guidance form matches the baseline failure type — recipe vs prohibition vs REQUIRED slot (Match the Form table)
- [ ] Discipline artifact has a rationalization table + red flags; description includes violation symptoms
- [ ] Description follows SDO — trigger conditions only, NO workflow summary (a summary lets agents follow the description and skip the body)
- [ ] Token budget respected — SKILL.md ≤ 500 lines / ~5000 tokens; descriptions < 500 chars where possible

Apply every FAIL item's fix recipe, then re-check the failed items only (LOOP, max 2 iterations).

---

## MODE: CRITIQUE & IMPROVE — Review and Auto-Improve

### Process

1. **Analyze** the input against: *Clarity* (unambiguous to a new reader?), *Completeness*, *Consistency* (no contradictions), *Specificity* (concrete vs generic), *Format fit* (platform-appropriate), *Language consistency*.
2. **Run the EVALUATE ⇄ TEST loop** (max 2 iterations): fix issues by *principle*, not by instance — each fix must state the general rule it enforces so the same class of defect is covered, not just the one occurrence (Principle 2).
3. **Auto-fix** issues that can be improved unambiguously. If a defect's cause is ambiguous, ask at the CLARIFY gate instead of guessing (Principle 3).
4. **Always output three sections** (in the user's language):

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

### Round-Trip Test (mandatory)
After converting, **convert the result back** to the source format in the Working Notes block and diff it against the original. Every meaningful difference is a conversion error or a deliberate, justified change — list each one in the output's **Changes made** section. This catches lost fields (`strict`, `title`, `outputSchema`, type-name casing) that a single-pass conversion misses.

---

## MODE: EXPLAIN — Clarify Concepts

When the user asks "Why use...", "How does... work", "What's the difference between...":

1. **Explain** the concept in plain language at the user's level (STAGE 2 THINK: identify the concept's essential shape before writing).
2. **Give a concrete example** (before/after or good/bad comparison) — but use a *neutral, generalizable* example; never anchor the explanation to a single user-supplied case (Principle 2). If the user gave a specific situation, first abstract it into the general pattern, then explain the pattern.
3. **Link to related patterns** in the reference files.
4. **Note when to use / when not to use** — including which models or platforms the pattern suits.
5. If the question itself is ambiguous (e.g., which platform or which pattern), ask one clarifying question at the CLARIFY gate rather than answering a guessed version (Principle 3).

---

## MODE: DISTILL — Turn Content Into Artifacts

Distill existing content (a conversation, a corpus, a repo, a doc) into a reusable artifact or a **skill family**. This is the meta-skill acting on itself — the same process that created this knowledge base.

### Skill Distillation Flow
1. **Capture intent** — extract the workflow from the source: tools/actions used, step sequence, corrections, input/output formats.
2. **Classify** — what artifact type(s) emerge from the source?
3. **Select tier** — single task (micro) / 2–5 workflows (standard) / adaptive multi-phase (deep engine).
4. **Transmute user cases into principles** — if the user supplied one specific situation or example, generalize it into a rule that covers the whole class of cases; if the source is domain-specific, abstract the reusable shape and note the generalization in the Provenance block (Principle 2).
5. **Emit per House Contract** — follow frontmatter / language / structure conventions.
6. **Validate** — run the EVALUATE ⇄ TEST loop (neutrality of examples, trigger test, countable rules).

### Provenance Ledger (mandatory for distilled artifacts)
Every distilled artifact ends with a `Provenance` block: source (conversation / corpus / repo / doc + tier), the generalization moves applied (e.g., "generalized from Git/GitHub to any CLI tool"), and the unverified external content deliberately excluded. The ledger makes "no hardcoding" auditable — a later reader can verify the artifact is a pattern, not a copy.

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
If a resource fits more than one axis, or its tier is ambiguous (e.g., Tier 2 vs Tier 3), ask one question at the CLARIFY gate instead of guessing (Principle 3); otherwise classify and state the decision in the Working Notes block.

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

- **Think of the model as a smart new hire lacking your norms** — and assume it is an *average* model: if a colleague would be confused, the model will be too. Write every rule to be executed correctly by a weak model; a strong model only exceeds the floor (Principle 1).
- **Behavior is verified, not assumed.** The self-audit proves the artifact's *shape*; the baseline test proves *compliance*. Run RED before writing (Iron Law), GREEN after — see `references/behavioral-testing.md`.
- **Match the form to the failure.** Recipes fix wrong-shaped output; prohibitions + rationalization tables fix rule-skipping under pressure; REQUIRED slots fix omitted elements. Never default to prohibition (it backfires on shaping problems).
- **Explain *why* a behavior matters**, not just *what* to do — but keep the *why* in one line; the *what* must stay mechanical and countable.
- **Use few-shot examples** (2–5) to steer format, tone, and structure; wrap them in `<examples>` / `<example>` tags. Keep examples neutral and generalizable — never contaminate output with example content (Principle 2).
- **Structure complex prompts with XML tags**: `<instructions>`, `<context>`, `<input>`, `<examples>`, `<thinking>`, `<answer>`.
- **Give a role** — even one sentence improves performance.
- **Apply progressive disclosure**: keep `SKILL.md` under 500 lines; push depth into `references/`.
- **Respect the token budget.** Every token competes with conversation history. Keep frequently-loaded skills lean; reference `--help` or external files instead of listing details; cross-reference instead of repeating.
- **Use persuasion deliberately for discipline rules** (authority, commitment, scarcity, social proof, unity) — see `references/behavioral-testing.md` § Persuasion Principles. Never for manipulation.
- **Never copy submodule/external content verbatim** — extract patterns only (Tier 5 is unverified; Principle 5).
- **State the chosen default** (platform/tier/language) back to the user in the Working Notes block so they can correct them.
- **Audit as a stranger, never in the writing pass.** Models — weak or strong — fail when they "check" their own output in the same pass that produced it. Separate writing and reviewing; make every review item countable (PASS/FAIL boundary + fix recipe).
- **Parameter naming** (`snake_case`), **enum for constrained values**, and **`additionalProperties: false` for strict schemas** — see `references/function-schema-guide.md`. For EXPERT-level artifacts also apply long-context handling (top-load data, `document` tags, grounded answers).

---

## Reference Files Index

| File | Contents | Read when |
|---|---|---|
| `references/execution-protocol.md` | Long chain-of-thought sub-questions per mode; stranger-audit mechanics; test checklist; weak-model-first rules | Every request, STAGE 2 THINK + STAGE 5 EVALUATE |
| `references/behavioral-testing.md` | RED-GREEN-REFACTOR procedure; pressure scenarios; rationalization capture; micro-test wording; persuasion principles | Every request, STAGE 3 BASELINE TEST + STAGE 6 GREEN ⇄ REFACTOR |
| `references/examples.md` | 5 worked examples rewritten through the v4.0.0 pipeline (Working Notes → baseline → audit → test) | Before first use of each MODE |
| `references/house-frontmatter-contract.md` | Unified YAML schema: `name`/`description`/`version`/`tags`/`compatibility`/`metadata`/`allowed-tools`; trigger-optimized description anatomy; validation checklist | Every create/rewrite of a skill |
| `references/house-language-policy.md` | English internal / user-language output; language buckets; artifact vs output distinction | Every multilingual artifact |
| `references/house-structure-conventions.md` | Unified SKILL.md skeleton; progressive disclosure; lazy-loaded `references/`; output contract; anti-example table | Every skill |
| `references/taxonomy-navigation.md` | 3-axis taxonomy; decision tree; Tier 1–7; MECE active/archive/external boundary | NAVIGATE/ORGANIZE, citation routing |
| `references/domain-engine-tiers.md` | micro / standard / deep engine tiers; decision tree; lazy-load rule | Selecting intensity tier |
| `references/prompt-framework-costar-x.md` | COSTAR-X framework; `<variable>` isolation; mandatory `<thinking>`; startup line | Authoring/porting prompts |
| `references/user-prompt-guide.md` | How the user should phrase a request; the 4 routing signals; ask-vs-infer policy | CREATE (user prompt), routing |
| `references/skill-guide.md` | Skill creation guide; frontmatter; sizing; progressive disclosure; skill-creator workflow | CREATE (skill) |
| `references/rules-guide.md` | Rules file guide; platform matrix; candidate-principle skeleton; multi-format sync | CREATE (rules) |
| `references/system-prompt-guide.md` | System prompt templates; 5-slot anatomy; agent-vs-assistant; XML vs Markdown | CREATE / CONVERT (system prompt) |
| `references/function-schema-guide.md` | Cross-platform schema comparison; MCP conventions; `outputSchema`; `Prompt.txt`+`Tools.json` | CREATE / CONVERT (schema) |
| `references/openai-function-calling.md` | OpenAI function calling schema, strict mode | CONVERT (schema) |
| `references/mcp-tool-spec.md` | MCP tool specification | CREATE / CONVERT (MCP) |
| `references/prompt-patterns.md` | 10 prompt patterns + anti-patterns | CREATE / EXPLAIN (prompt) |
| `references/prompt-engineering-official.md` | Anthropic official best practices (Claude-specific — see annotation) | CREATE / EXPLAIN (all) |

---

## Examples

Five worked examples — CREATE (system prompt), CRITIQUE (multilingual), CONVERT (schema + round-trip), DISTILL (skill + provenance), NAVIGATE (classification) — rewritten through the v4.0.0 pipeline with Working Notes, audit, and test stages, live in **`references/examples.md`**. Read it before your first use of each MODE.

### Inline example: Working Notes block shape (CREATE)

```
## Working Notes
- Request: create a system prompt for a tutoring chatbot (EN input)
- Mode=CREATE · Type=System Prompt · Platform=platform-agnostic · Tier=standard
- Known: tutoring domain, target learners. Missing: none — proceed (no CLARIFY needed)
- Baseline (RED): control run without artifact → agent gave the answer outright (rationalization: "helpful = answer")
- Audit (stranger pass): 5-slot anatomy complete ✓ · constraints countable ✓ · neutral examples ✓
- Test: GREEN run → agent guides instead of answering ✓ · acceptance 4/4 · PASS (1 iteration)

## Output
[the artifact, single block]
```
