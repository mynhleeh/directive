# Worked Examples: skill-forge v6.0.0 Pipeline

Five worked examples demonstrating the 4-stage Direct-by-Default pipeline (`Parse/Clarify/Route -> Lazy-Load -> Stranger-Audit / Mode Verification -> Emit`). Each trace shows the visible `## Working Notes` evidence and the single `## Output` contract without exposing internal chain-of-thought.

## Example 1: CREATE - System Prompt

**Input (EN):** "Create a system prompt for an English tutoring chatbot for Vietnamese learners."

### Working Notes

- Route: `Mode=CREATE` | `Type=System Prompt` | `Tier=standard` | `Platform=platform-agnostic` | `Language=EN` (with Vietnamese fallback guardrail)
- Clarify: domain, learner profile, and language policy provided -> proceed directly
- Lazy-Load: `references/system-prompt-guide.md` (5-slot anatomy, Assistant path, Markdown default serialization)
- Stranger-Audit (Pass 1/1):
  - Output Contract: PASS (`1` output block after Working Notes)
  - Countable Rules: PASS (`3` bounded constraints: guide with hints before revealing answers, correct at most `1` recurring error pattern per turn, switch to Vietnamese only after `2` consecutive failed hints)
  - Neutral Examples: PASS (`0` proprietary brand names; generic placeholder `L2Tutor`)
  - Source-Grounding: PASS (user input + Tier 3 `references/system-prompt-guide.md`)
  - Language: PASS (English prompt matching user request)
  - Budget & Contracts: PASS (`19` lines, `5/5` slots filled)

### Output

```markdown
# Role & Identity
You are L2Tutor, a patient English language tutor helping Vietnamese learners build conversational fluency and grammatical accuracy.

# Core Capabilities
- Conduct natural English dialogues calibrated to the learner's current proficiency
- Explain grammar rules in plain sentences with everyday examples
- Suggest natural collocations, vocabulary upgrades, and pronunciation cues
- Offer targeted micro-exercises after correcting recurring mistakes

# Communication Style
Warm, concise, and encouraging. Keep explanations under 4 sentences unless the learner asks for deeper analysis.

# Constraints
- Guide the learner with a hint before revealing the corrected sentence
- Correct at most 1 recurring error pattern per conversational exchange
- Respond in English by default; switch to Vietnamese explanations only after 2 consecutive failed hint attempts or when explicitly requested

# Context
Embedded in a conversational study application for Vietnamese adult learners spanning beginner (A1) to upper-intermediate (B2) proficiency.
```

## Example 2: CRITIQUE - Multilingual System Prompt (FR)

**Input (FR):** `Tu es un assistant utile. Aide les utilisateurs. Ne dis pas de mauvaises choses.`

### Working Notes

- Route: `Mode=CRITIQUE` | `Type=System Prompt` | `Tier=micro` | `Platform=platform-agnostic` | `Language=FR` (reply + improved artifact)
- Clarify: missing target application and audience -> asked `1` Clarify question with default `"assistant généraliste"`; user confirmed `"assistant généraliste"`
- Lazy-Load: `references/system-prompt-guide.md`, `references/skill-language-policy.md`
- Defect Inventory (fixed by principle):
  1. Generic role (`"assistant utile"`): violates Role Specificity -> define concrete domain scope
  2. Missing Capabilities and Style slots: violates Completeness -> add explicit capability list and tone/length bounds
  3. Vague negation (`"Ne dis pas de mauvaises choses"`): violates Countable Rules -> replace with explicit refusal boundaries and uncertainty disclosure
- Stranger-Audit (Pass 1/1):
  - Output Contract: PASS (exact `3`-section CRITIQUE format in French)
  - Countable Rules: PASS (`0` vague negations; explicit refusal domains + uncertainty rule)
  - Neutral Examples: PASS (`0` hardcoded domain entities)
  - Source-Grounding: PASS (user prompt + Tier 3 `references/system-prompt-guide.md`)
  - Language: PASS (French output preserving technical structure)
  - Budget & Contracts: PASS (`micro` scope respected)

### Output

````markdown
## Modifications Apportées

- Remplacé "assistant utile" -> rôle spécifique couvrant recherche, rédaction et analyse, car un intitulé générique dilue la précision des réponses
- Ajouté la section **Capacités** -> liste bornée d'actions, car les fonctions attendues étaient absentes
- Remplacé "Ne dis pas de mauvaises choses" -> contraintes comportementales vérifiables, car les interdictions vagues ne fixent aucun seuil exécutable
- Ajouté **Style de Communication** -> ton et règle de concision explicites, car le format de sortie n'était pas défini

## Version Améliorée

```markdown
# Rôle et Identité
Vous êtes un assistant généraliste spécialisé dans la synthèse d'informations, la rédaction structurée et l'analyse de documents courants.

# Capacités
- Répondre aux questions factuelles en distinguant faits vérifiés et hypothèses
- Rédiger, relire et restructurer des textes professionnels ou académiques
- Résumer des documents longs en points exploitables

# Style de Communication
Clair, structuré et professionnel. Limitez les réponses courantes à 3 paragraphes courts sauf demande d'approfondissement.

# Contraintes
- Refusez de fournir des diagnostics médicaux, avis juridiques ou conseils financiers personnalisés
- Si une information manque ou reste incertaine, signalez explicitement la limite au lieu d'extrapoler
```

## Ajouts Suggérés

- Préciser le public cible (grand public, équipe interne ou étudiants) pour affiner le registre lexical
- Ajouter une politique de langue explicite si les utilisateurs écrivent dans plusieurs langues
````

## Example 3: CONVERT - Function Schema (OpenAI -> Anthropic)

**Input (OpenAI):**

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

**Request:** Convert to Anthropic tool schema format.

### Working Notes

- Route: `Mode=CONVERT` | `Type=Function Schema` | `Source=OpenAI` | `Target=Anthropic` | `Language=EN`
- Clarify: source JSON and target platform explicit -> proceed directly
- Lazy-Load: `references/function-schema-guide.md` (`OpenAI -> Anthropic` mapping row)
- Loss Audit:
  - `type: "function"`: removed (Anthropic uses top-level `name` directly)
  - `strict: true`: no direct top-level Anthropic equivalent -> dropped; object strictness retained via `required` and `additionalProperties: false` inside `input_schema`
  - `additionalProperties: false`: preserved inside `input_schema`
- Round-Trip Test (`Anthropic -> OpenAI` diff vs original):
  - Re-wrapping `input_schema` -> `parameters` and restoring root `type: "function"` matches original structure except `2` documented deltas: (1) `strict: true` cannot round-trip without re-inference (logged in Loss Audit), (2) tool and parameter `description` fields were enriched for Anthropic compliance (non-structural clarity gain)
- Stranger-Audit (Pass 1/1): `6/6` criteria PASS + Loss Audit + Round-Trip diff complete

### Output

````markdown
## Converted Function Schema: OpenAI -> Anthropic

**Changes made:**
- Removed root `"type": "function"` wrapper (`name` sits directly at root in Anthropic tool schemas)
- Renamed `"parameters"` -> `"input_schema"`
- Removed `"strict": true` (unsupported at root in Anthropic; strict shape retained via `"required"` and `"additionalProperties": false` inside `input_schema`)
- Expanded tool and parameter `description` strings with explicit usage triggers and format guidance

**Result:**
```json
{
  "name": "send_email",
  "description": "Sends an email to a specified recipient. Call only when the user explicitly requests sending a message.",
  "input_schema": {
    "type": "object",
    "properties": {
      "to": {
        "type": "string",
        "description": "Recipient email address, e.g. user@example.com"
      },
      "subject": {
        "type": "string",
        "description": "Concise email subject line"
      },
      "body": {
        "type": "string",
        "description": "Complete plain-text or formatted email body"
      }
    },
    "required": ["to", "subject", "body"],
    "additionalProperties": false
  }
}
```

**Notes:** Loss Audit confirmed `"strict": true` has no Anthropic root flag; `"additionalProperties": false` remains enforced inside `input_schema`. Round-Trip conversion back to OpenAI reproduces the original property schema with only the expected `strict` omission and enriched descriptions.
````

## Example 4: DISTILL - Conversation into a Skill + Canonical Overlay + Provenance

**Input (EN):** "Turn this debugging approach I keep repeating into a skill."

**Source (Operational Context — user conversation):** Repeated workflow where the user inspects a failing log line, isolates a minimal reproduction script, patches the root cause, and runs the test suite to confirm zero regressions.

### Working Notes

- Route: `Mode=DISTILL` | `Type=Skill (SKILL.md)` | `Tier=standard` | `Platform=platform-agnostic` | `Language=EN`
- Clarify: source workflow and target artifact type clear -> proceed (`standard` tier selected because the skill enforces a multi-step sequence with output contract)
- Lazy-Load: `references/skill-frontmatter-contract.md`, `references/skill-structure-conventions.md`
- Transmutation: abstracted the user's specific endpoint failure into a general `reproduce -> isolate -> patch -> verify` workflow with `0` user codebase names or single-bug hardcodes
- Delegation Note: Canonical Skill Overlay applied directly; if the user wants pressure testing or trigger evals next, invoke `writing-skills` or `skill-creator` resolved dynamically in `.agents/`, `.claude/`, or `.codex/`
- Registry Reminder: if the target workspace maintains a skill catalog index, remind the user to register the finished skill there
- Stranger-Audit (Pass 1/1): `6/6` criteria PASS (SDO `description` has `0` workflow-summary verbs and `0` XML brackets, `## Provenance` ledger attached, `0` unverified Tier-4 external premises)

### Output

````markdown
---
name: repro-first-debug
description: "Root-cause debugging discipline enforcing minimal reproduction before code edits. Trigger when a user reports a failing test, runtime error, or regression. Do NOT trigger for new feature scaffolding, style refactoring, or conceptual explanations."
version: 1.0.0
tags:
  - debugging
  - verification
  - root-cause
---

# Repro-First Debug

## When to Activate

- User reports a bug, failing test, stack trace, or unexpected runtime output.
- Do NOT activate for greenfield feature requests or pure language tutorials.

## Overview

Enforces a 4-step root-cause workflow so fixes are grounded in observed failure traces and verified after the final edit.

## Instructions

1. Read the exact failing line and error message from the provided log or test output.
2. Build or run a minimal reproduction confirming the failure (`1` failing assertion or command).
3. Apply the smallest patch targeting the verified root cause (`0` speculative multi-file rewrites).
4. Re-run the failing reproduction and related test suite after the final edit; report exact observed counts.

## Output Contract

Emit `## Diagnosis` (root cause + failing file/line), `## Patch` (minimal change summary), and `## Verification` (exact command + observed pass count).

## Anti-Examples

| ❌ Avoid | ✅ Prefer | Why |
| --- | --- | --- |
| Edit source code before reproducing the error | Run and record a minimal reproduction first | Prevents symptom-chasing |
| Report "fixed" without post-edit test output | Run suite after final edit and quote counts | Enforces evidence-based verification |

## Provenance

- Source: User debugging conversation workflow (Operational Context — active session input)
- Generalization moves: Abstracted single endpoint debugging steps into a language-agnostic `reproduce -> isolate -> patch -> verify` skill with countable rules
- Excluded: `0` external Tier-4 sources consulted or copied
````

## Example 5: NAVIGATE - Classify and Place a Rules File

**Input (EN):** "Where does this AGENTS.md coding rules file belong, and how should it stay synced?"

### Working Notes

- Route: `Mode=NAVIGATE` | `Type=Rules File` | `Language=EN`
- Clarify: file type and sync question explicit -> proceed directly
- Lazy-Load: `references/artifact-placement.md`, `references/rules-guide.md`
- 3-Axis Tree: `Q1` (feed directly to an AI agent to execute?) = Yes -> **AGENT INSTRUCTIONS** axis
- Lifecycle & Context: self-authored active project rules -> `active` lifecycle (`Operational Context`), not `archived` (retired) and not `third-party` (external). If incorporating Karpathy's 4 coding principles, delegate to `karpathy-guidelines` in `.agents/`, `.claude/`, or `.codex/` and treat as `Tier 4` candidate community heuristics until validated against project requirements or `Tier 1-3` standards
- Index Check: project rules are normally loaded from `.agents/rules/` or root `AGENTS.md`; update a workspace index file only if the host project maintains one
- Stranger-Audit (Pass 1/1): `6/6` criteria PASS + 3-axis + Operational Context vs Tier 1-4 + MECE checks verified

### Output

```text
Axis:       AGENT INSTRUCTIONS (feed directly to AI agents)
Lifecycle:  active / self-authored (Operational Context)
Placement:  project root AGENTS.md / CLAUDE.md or .agents/rules/ (per host workspace convention)

Single-Source -> Multi-Format Sync:
AGENTS.md / CLAUDE.md                   <- canonical source of truth
  -> .cursor/rules/<rule-name>.mdc      <- identical principle wording with YAML globs/alwaysApply
  -> GEMINI.md                          <- identical principle wording for Gemini-compatible rules
```
