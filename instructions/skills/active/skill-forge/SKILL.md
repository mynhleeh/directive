---
name: skill-forge
description: "AI artifact architecture engine for System/User Prompts (COSTAR-X), cross-platform Function/Tool JSON Schemas with Round-Trip checks, Rules file multi-format sync, directive house contracts, DISTILL provenance, and NAVIGATE taxonomy. Trigger whenever prompt, schema, rules, skill house-contract, distillation, or placement work is requested. Do NOT trigger for full MCP server SDKs (use mcp-builder), standalone skill TDD/benchmarking/trigger optimization (use writing-skills or skill-creator), or ordinary coding/debugging (use tech-mentor)."
version: 6.0.0
tags:
  - meta-skill
  - system-prompt
  - user-prompt
  - function-calling
  - tool-schema
  - rules
  - convert
  - distill
  - navigate
  - costar-x
  - house-contracts
  - taxonomy
  - multilingual
  - round-trip
  - sdo
compatibility: "Platform-agnostic (Claude, OpenAI, Gemini, MCP, Cursor, Codex, AGY). Direct-by-Default execution with mechanical rules; delegates companion skills dynamically via active workspace skill registries."
---

# Skill Forge

AI artifact engineering engine for System Prompts, User Prompts (`COSTAR-X`), cross-platform Function/Tool JSON Schemas, Rules files, `directive` house-contract `SKILL.md` overlays, pattern distillation (`DISTILL`), and 3-axis resource placement (`NAVIGATE`).

## Overview

`skill-forge` authors, critiques, converts, explains, distills, and organizes prompt, schema, rules, and house-contract skill artifacts using a Direct-by-Default 4-stage pipeline, lazy-loaded `references/`, and countable stranger-audit gates.

## When to Activate

Activate when the user requests work on prompts, schemas, rules files, house-contract skills, content distillation, or repository taxonomy placement.

- **Keywords:** `prompt`, `system prompt`, `user prompt`, `COSTAR-X`, `skill`, `SKILL.md`, `function calling`, `tool schema`, `Prompt.txt`, `Tools.json`, `rules file`, `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.cursorrules`, `.mdc`, `critique`, `convert`, `round-trip`, `distill`, `provenance`, `navigate`, `taxonomy`.
- **Do NOT activate for:** full Python/TypeScript MCP server SDK builds (`mcp-builder`), standalone skill TDD/pressure testing (`writing-skills`), standalone skill benchmarking/trigger evals (`skill-creator`), Claude SDK migration alone (`claude-api`), or ordinary coding/debugging (`tech-mentor`).

## External Delegation & Runtime Resolution

`skill-forge` avoids duplicating capabilities owned by installed companion skills. Delegate specialized domains using the matrix below:

| Capability Domain | Handled by `skill-forge` | Delegated Companion Skill |
| --- | --- | --- |
| Skill TDD, pressure tests, persuasion | None (omitted) | `writing-skills` |
| Skill evals, benchmarks, trigger optimization | Thin House Overlay checks only | `skill-creator` |
| Full MCP server SDK and transport wiring | Standalone JSON schema mapping and `Prompt.txt` + `Tools.json` | `mcp-builder` |
| Claude SDK migration and Claude prompt cruft audit | Cross-platform portability (`OpenAI <-> Claude <-> Gemini`) | `claude-api` |
| Coding agent 4 core behavioral principles | Rules format matrix and Single-Source -> Multi-Format Sync | `karpathy-guidelines` |

**Runtime resolution rule:** Resolve companion skills dynamically by canonical skill name inside the active workspace's skill directories (`.agents/`, `.claude/`, `.codex/`, or harness skill registries), matching exact names or collision-prefixed variants (e.g., `ant-skill-creator`, `aers-skill-creator`). Never hardcode repository-source external paths. If a needed companion skill is absent from the active workspace, name the missing canonical skill so the user can install or attach it, and execute only the in-scope `skill-forge` portion.

## Core Principles

Every instruction and generated artifact obeys these 5 rules; `SKILL.md` overrides `references/` if any rule conflicts, and conflicts must be flagged immediately:

1. **Countable & Mechanical:** Express every rule as a number, threshold, or deterministic pass/fail recipe (`0` vague adjectives or judgment calls) so average models execute reliably.
2. **Principles over Instances:** Author generalizable rules and neutral examples with `0` real brands or user-supplied proper nouns; abstract specific cases into rules for the whole class.
3. **Clarify Gate (`max 3` questions, 1 batch with defaults):** Never invent missing routing signals or ambiguous intent. Ask up to **3** questions in **1** batch, each paired with an explicit default option; if signals are confident, proceed and log chosen defaults with 1-line reasons in `## Working Notes`.
4. **Surgical Scope:** Emit only the requested artifact and its declared contract. Put optional enhancements in `## Suggested Additions` (under `CRITIQUE`) or omit them.
5. **Source-Grounded & Tier-Aware:** Trace every factual or methodological claim to user input or `Tier 1-7` (`references/taxonomy-navigation.md`). Prefer `Tier 1-3`; never copy external content verbatim and never promote unverified `Tier 5` material into a premise.

## Language Policy

Internal skill instructions and all `references/` files remain in English; user-facing replies adapt to the user's language per `references/house-language-policy.md`.

| Input Language | Reply Language | Technical Terms | Artifact Language |
| --- | --- | --- | --- |
| English | English | Preserve original | English (unless specified) |
| Vietnamese / French / Japanese / Other | User's language | Preserve English terms | Follow user request (default: English) |
| Ambiguous | Ask 1 Clarify question (default: English) | Preserve original | Ask at Clarify Gate |

## Instructions: Direct-by-Default Pipeline

Run all 4 stages directly in the primary turn without dispatching subagents unless the user explicitly asks for them:

```text
User Request
  -> Stage 1: Parse, Clarify & Route (Mode, Artifact Type, Tier, Platform, Language)
  -> Stage 2: Lazy-Load (1-2 references max) & Execute directly or Delegate by canonical name
  -> Stage 3: Stranger-Audit (6 countable criteria, separate pass, max 2 iterations) + Mode Gates
  -> Stage 4: Emit (compact ## Working Notes + single ## Output block)
```

### Stage 1: Parse, Clarify & Route

1. Classify `Mode` (`CREATE`, `CRITIQUE`, `CONVERT`, `EXPLAIN`, `DISTILL`, `NAVIGATE`), `Artifact Type` (`skill`, `system prompt`, `user prompt`, `function schema`, `rules file`), `Intensity Tier` (`micro`, `standard`, `deep engine`), `Platform` (`Claude`, `OpenAI`, `Gemini`, `MCP`, `platform-agnostic`), and `Language`.
2. Split `KNOWN` vs `MISSING` signals. Stop at the Clarify Gate (`max 3` questions, 1 batch with defaults) only when a missing signal changes artifact structure.

### Stage 2: Lazy-Load & Execute / Delegate

1. Open only the `1-2` reference files mapped to the active `Mode` and `Artifact Type` in the Reference Files Index; never bulk-load all references.
2. Execute the active mode's recipe directly, or delegate to the matching companion skill via dynamic runtime resolution when the task enters an external domain.

### Stage 3: Stranger-Audit & Mode Gates

Re-read the generated artifact from top to bottom in a separate pass (never in the writing pass) and score all **6** countable criteria PASS/FAIL with quoted evidence or count; fix failed items only and re-check failed items (`max 2` iterations):

| # | Criterion | Countable Pass Condition | Fix Recipe |
| --- | --- | --- | --- |
| 1 | Output Contract | Exactly `1` `## Output` block after `## Working Notes` (or `3` fixed sections for `CRITIQUE`) | Trim extras or move ideas to `## Suggested Additions` |
| 2 | Countable Rules | `0` judgment-call instructions; every rule uses a number, threshold, or recipe | Replace vague phrasing with explicit threshold or condition |
| 3 | Neutral Examples | `0` real brand names or single-case hardcodes from user input | Swap to neutral placeholder domain and abstract intent |
| 4 | Source-Grounding | `100%` of factual claims trace to user input or cited `Tier 1-7`; `0` unverified `Tier 5` premises | Drop unsupported claims or cite verified tier |
| 5 | Language | Reply matches user language; artifact matches request/default; English terms preserved | Re-serialize mismatched sections |
| 6 | Budget & Contracts | Skill `< 500` lines (`references/` split if deep); frontmatter has `0` XML brackets and `0` workflow-summary verbs in `description` | Move depth to `references/` and strip summary verbs |

Enforce mandatory mode gates during Stage 3 before advancing to Stage 4:

- **CONVERT Gate:** Run **Loss Audit** (list every platform-specific field dropped or transformed) and **Round-Trip Test** (convert output back to source format in `## Working Notes` and account for every diff).
- **DISTILL Gate:** Verify case-to-principle transmutation and append `## Provenance` (source + tier, generalization moves, excluded Tier-5 content).
- **NAVIGATE Gate:** Verify 3-axis tree (`Q1`/`Q2`/`Q3`), `Tier 1-7` citation priority, MECE boundary (`active/` vs `archive/` vs `external/`), and workspace index update check.

### Stage 4: Emit

Emit `## Working Notes` followed by a single `## Output` block. When creating, porting, or classifying a skill inside a workspace with a catalog index (e.g., `SKILL_INDEX.md`), add a 1-line registration reminder in `## Working Notes`.

## Modes

### MODE: CREATE

Route `Artifact Type` -> `Intensity Tier` (`references/domain-engine-tiers.md`) -> `Platform` -> `Language`, then apply the matching recipe:

- **Skill (`SKILL.md` thin House Overlay):** Apply `references/house-frontmatter-contract.md` (note `metadata:` nesting when exporting to strict `agentskills.io` `quick_validate.py`), `references/house-structure-conventions.md`, `references/house-language-policy.md`, and `references/domain-engine-tiers.md`. Emit the canonical skeleton (`## When to Activate` for standard/deep, `## Overview`, `## Instructions`, `## Output Contract`, `## Anti-Examples`, `## References`). Delegate pressure testing to `writing-skills` and evals/trigger tuning to `skill-creator`.
- **System Prompt:** Follow `references/system-prompt-guide.md`. Fill all 5 slots (`Role & Identity`, `Capabilities`, `Constraints`, `Communication Style`, `Context`), route Agent vs Assistant, pick serialization (`XML` for Claude, Markdown default, `YAML`/`JSON` for Gemini), and apply `<examples>`, `20k+` `<documents>` top-load, and adaptive-thinking guidance as needed.
- **User Prompt:** Follow `references/user-prompt-guide.md` (4 input signals) and `references/prompt-framework-costar-x.md` (`COSTAR-X` scaffold, `<variable>` isolation, mandatory `<thinking>`). Include `XÁC NHẬN KHỞI ĐỘNG` **only** for interactive session-boot prompts; omit it for API calls, headless batch pipelines, or `Prompt.txt` agent configs.
- **Function / Tool Schema:** Follow `references/function-schema-guide.md`. Use verb-first `snake_case` names, WHAT + WHEN descriptions, `required`, `additionalProperties: false` for strict schemas, `outputSchema` for MCP, and `Prompt.txt` + `Tools.json` parity for packaged agent resources. Delegate full MCP server SDKs to `mcp-builder`.
- **Rules File:** Follow `references/rules-guide.md` for `CLAUDE.md`, `AGENTS.md`/`GEMINI.md`, `.cursor/rules/*.mdc`, and `.cursorrules`. Keep one canonical source synchronized across formats (`CLAUDE.md <-> .cursor/rules/*.mdc <-> GEMINI.md / AGENTS.md`) and delegate Karpathy's 4 coding principles to `karpathy-guidelines` (`Tier 5` candidate guidance).

### MODE: CRITIQUE

1. Audit the input across 6 criteria: **Clarity**, **Completeness**, **Consistency**, **Specificity** (concrete action rules over vague negations), **Format fit**, and **Language consistency**.
2. Fix every unambiguous defect by underlying *principle* (not instance) across `max 2` Stranger-Audit iterations; ask at the Clarify Gate for ambiguous intent.
3. Emit exactly these 3 sections in the user's language inside `## Output`:

```markdown
## Changes Made

- Changed "[old]" -> "[new]" because [violated principle]

## Improved Version

[Single improved artifact block]

## Suggested Additions

- Consider adding: [missing context or optional enhancement]
```

### MODE: CONVERT

Translate system prompts (`OpenAI <-> Claude <-> Gemini <-> Platform-agnostic` via `references/system-prompt-guide.md`), user prompts (`COSTAR-X` structural conversion via `references/prompt-framework-costar-x.md`), rules files (multi-format sync via `references/rules-guide.md`), or Function/Tool JSON Schemas (`references/function-schema-guide.md`) using the mapping table below, then run the mandatory **Loss Audit** and **Round-Trip Test**:

| From -> To | Key Schema Changes |
| --- | --- |
| `OpenAI -> Anthropic` | `parameters` -> `input_schema`; drop `type: "function"` wrapper and `strict` |
| `OpenAI -> MCP` | `parameters` -> `inputSchema`; drop `type: "function"` and `strict`; add optional `title` and `outputSchema` |
| `OpenAI -> Gemini` | Keep `parameters`; UPPERCASE JSON types (`STRING`, `OBJECT`, `ARRAY`, `INTEGER`, `BOOLEAN`, `NUMBER`); drop `type: "function"`, `strict`, `additionalProperties` |
| `Anthropic -> OpenAI` | `input_schema` -> `parameters`; add root `type: "function"` and `name`; evaluate `strict` and `additionalProperties: false` |
| `MCP -> OpenAI` | `inputSchema` -> `parameters`; add root `type: "function"`; log lost `title` and `outputSchema` |
| `Gemini -> OpenAI` | UPPERCASE types -> lowercase; add root `type: "function"` and `name` |
| `Anthropic <-> MCP / Gemini` | Rename `input_schema` <-> `inputSchema` / `parameters`; add/drop `title` + `outputSchema` (MCP) or UPPERCASE types (Gemini) |

Emit `## Converted [Type]: [Source] -> [Target]` containing `**Changes made:**`, `**Result:**`, and `**Notes:**` (all Loss Audit items and Round-Trip diff outcomes).

### MODE: EXPLAIN

1. State the concept's essential mechanism in `1-2` plain sentences matched to the user's technical level.
2. Provide `1` neutral before/after contrast example (abstract user-supplied specifics into a general pattern first).
3. Link the relevant `references/` file with its epistemic tier (`Tier 1-7`) and specify when to use vs skip the pattern across platforms.

### MODE: DISTILL

1. Extract workflow steps, tools, corrections, and I/O contracts from the source (conversation, document, corpus, or repo).
2. Classify artifact type(s) and `Intensity Tier`; emit a **skill family** (parent router `SKILL.md` + `references/<variant>.md`) when multiple variants emerge.
3. Transmute single user instances into general rules (`0` verbatim external copies; `0` `Tier 5` premises) and append a mandatory `## Provenance` block recording **Source (+ Tier)**, **Generalization moves**, and **Excluded external/Tier-5 content**.

### MODE: NAVIGATE

Classify and place resources using `references/taxonomy-navigation.md`:

```text
Q1: Feed directly to an AI agent to execute? -> INSTRUCTIONS (`instructions/`, `skills/`, `.agents/`)
Q2: Read to learn, research, or explain?     -> KNOWLEDGE (`knowledge/`, `docs/`, `reference/`)
Q3: System design, architecture, or model?  -> BLUEPRINTS (`blueprints/`, `architectures/`, `design/`)
```

- **MECE lifecycle:** `active/` and `archive/` hold self-created assets only; `external/` holds third-party content only (untrack/delete when obsolete, never move to `archive/`).
- **Citation priority (`Tier 1-7`):** `Tier 1` (peer-reviewed/formal specs) > `Tier 2` (official vendor docs) > `Tier 3` (curated guides) > `Tier 4` (articles) > `Tier 5` (external submodules) > `Tier 6` (active project files) > `Tier 7` (archives).
- **Registry check:** Remind the user to update `SKILL_INDEX.md` or `REFERENCE_INDEX.md` (when present) after adding or moving artifacts.

## Anti-Examples

| ❌ Avoid | ✅ Prefer | Why |
| --- | --- | --- |
| "Write clear rules and use good judgment" | "Cap each section at 5 rules; state a threshold per rule" | Mechanical rules enforce consistency |
| Copy user repo/brand names into examples | Abstract intent into a neutral placeholder domain | Prevents prompt contamination |
| Bulk-load all 11 reference files upfront | Lazy-load only the 1-2 mapped references per task | Preserves context budget |
| Guess missing tier, language, or target | Ask max 3 Clarify questions in 1 batch with defaults | Prevents structural rework |
| Emit `SKILL.md` with summary verbs in `description` | Put triggers and near-miss negatives only in `description` | Prevents body-skipping (SDO) |

## Output Contract

Every response emits `## Working Notes` followed by a single `## Output` block:

```markdown
## Working Notes

- Route: Mode=[mode] | Type=[type] | Tier=[tier] | Platform=[platform] | Language=[lang]
- Clarify: [none - proceed | defaults stated | 1-batch question]
- Lazy-Load: [1-2 reference filenames]
- Audit (Pass [1|2]): [6/6 criteria PASS + Mode Gate summary]

## Output

[Single artifact block or 3-section CRITIQUE block]
```

## Reference Files Index

| File | Contents | Read when |
| --- | --- | --- |
| `references/house-frontmatter-contract.md` | Unified YAML schema, SDO trigger anatomy, `agentskills.io` `metadata:` portability, validation checklist | Creating or reviewing any `SKILL.md` |
| `references/house-language-policy.md` | English internals, user-language output buckets, artifact vs output language rule | Any multilingual request or skill |
| `references/house-structure-conventions.md` | Canonical `SKILL.md` skeleton, progressive disclosure, Output Contract, anti-example table | Creating or restructuring a `SKILL.md` |
| `references/domain-engine-tiers.md` | `micro` / `standard` / `deep engine` decision tree, lazy-load rule, tier-scaled testing pointers | Selecting or auditing intensity tier |
| `references/taxonomy-navigation.md` | 3-axis taxonomy, Q1/Q2/Q3 tree, `Tier 1-7` hierarchy, MECE `active`/`archive`/`external` rules | `NAVIGATE` or citation tier routing |
| `references/system-prompt-guide.md` | 5-slot anatomy, Agent vs Assistant, XML/Markdown/JSON templates, `<examples>`, `20k+` `<documents>`, adaptive thinking | `CREATE` / `CONVERT` / `CRITIQUE` system prompts |
| `references/user-prompt-guide.md` | 4 routing signals, request anatomy, ask-vs-infer policy, request anti-patterns | `CREATE` user prompts or ambiguous routing |
| `references/prompt-framework-costar-x.md` | `COSTAR-X` scaffold, `<variable>` isolation, `<thinking>` CoV, interactive-only `XÁC NHẬN KHỞI ĐỘNG` | `CREATE` / `CONVERT` / `EXPLAIN` user prompts |
| `references/function-schema-guide.md` | `OpenAI` / `Anthropic` / `MCP` / `Gemini` matrix, Responses wire format, `Prompt.txt` + `Tools.json`, `mcp-builder` pointer | `CREATE` / `CONVERT` / `CRITIQUE` tool schemas |
| `references/rules-guide.md` | `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` / `.cursor/rules/*.mdc` / `.cursorrules` formats, multi-format sync, `karpathy-guidelines` pointer | `CREATE` / `CONVERT` / `NAVIGATE` rules files |
| `references/examples.md` | 5 worked `v6.0.0` Direct-by-Default traces (`CREATE`, `CRITIQUE`, `CONVERT`, `DISTILL`, `NAVIGATE`) | First execution of any mode |
