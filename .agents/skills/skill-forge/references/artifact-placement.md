# Workspace Artifact Placement & Source Authority

A **workspace-agnostic classification and citation routing guide** for AI engineering artifacts. It lets a meta-skill discover a target project's conventions dynamically, place artifacts in the right location, and evaluate external vs. operational sources consistently.

> **Why this file exists**: Target projects vary in directory layout. Rather than hardcoding one repository's folders, this reference defines intent-based placement rules and an external source authority ladder for **NAVIGATE** and **EXPLAIN / DISTILL** workflows.

## The 3 Intent Axes

Every engineering artifact serves one of three primary intents. Inspect the active workspace first and map the axis onto the project's existing layout:

| Axis | Decision Question | Typical Target Locations |
| --- | --- | --- |
| **AGENT INSTRUCTIONS** | Will an AI agent load or execute this directly? | `.agents/`, `.claude/`, `.codex/`, `.cursor/rules/`, root `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`, `skills/`, `prompts/`, `rules/` |
| **DOCUMENTATION & REFERENCE** | Will a reader or agent consult this to learn or cite facts? | `docs/`, `references/`, `standards/`, `policies/`, `guides/` |
| **ARCHITECTURE & DESIGN** | Is this a system design, spec, ADR, or mental model? | `docs/architecture/`, `docs/specs/`, `design/`, `adr/`, `rfc/` |

### Decision Tree

```text
Q1: Will an AI agent load or execute this directly?
  -> Yes -> AGENT INSTRUCTIONS (e.g., .agents/skills/, .claude/skills/, .agents/rules/, root AGENTS.md / CLAUDE.md)
  -> No  -> Q2

Q2: Will a reader consult this to learn, look up standards, or verify claims?
  -> Yes -> DOCUMENTATION & REFERENCE (e.g., docs/guides/, references/, standards/)
  -> No  -> Q3

Q3: Is this a system design, architectural spec, or conceptual model?
  -> Yes -> ARCHITECTURE & DESIGN (e.g., docs/architecture/, design/, specs/)
  -> No  -> Clarify with user and follow host repository conventions
```

## Resource Placement Mapping

Discover existing directories in the active project before creating new folders. Use the fallback conventions below only when the host workspace has none:

| Resource type | Axis | Common Workspace Locations |
| --- | --- | --- |
| Skill packages (`SKILL.md`) | AGENT INSTRUCTIONS | `.agents/skills/`, `.claude/skills/`, `.codex/skills/`, or project `skills/` |
| System / user prompts | AGENT INSTRUCTIONS | `.agents/prompts/`, `prompts/`, or dedicated prompt config files |
| Always-on rules files | AGENT INSTRUCTIONS | Project root (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`), `.agents/rules/`, `.cursor/rules/` |
| Automation / helper scripts | AGENT INSTRUCTIONS | Skill-local `scripts/` or workspace `scripts/` |
| Guides, standards, tutorials | DOCUMENTATION & REFERENCE | `docs/`, `references/`, `standards/`, `policies/` |
| Papers & formal specs | DOCUMENTATION & REFERENCE | `docs/papers/`, `references/standards/` |
| Architecture diagrams & specs | ARCHITECTURE & DESIGN | `docs/architecture/`, `docs/specs/`, `design/` |
| Decision records (ADR / RFC) | ARCHITECTURE & DESIGN | `docs/adr/`, `docs/rfc/`, `docs/decisions/` |

## Lifecycle States (MECE)

Separate maintained owned artifacts, retired history, and third-party dependencies cleanly when a project tracks lifecycle state:

| State | Purpose | Contains |
| --- | --- | --- |
| `active` | Currently used, maintained | Self-authored resources actively in production |
| `archived` | Retired — historical only | Deprecated or superseded self-authored resources kept for audit history |
| `third-party` | Vendored or submodule packages | External repositories, upstream skill suites, or vendor bundles |

### Lifecycle Rules

- Keep owned (`active` / `archived`) artifacts separate from `third-party` vendored packages.
- When a `third-party` dependency is retired, remove or untrack it cleanly rather than moving it into an owned `archived` folder.

## External Source Authority Ladder (`Tier 1-4`)

When grounding factual, technical, or methodological claims in external sources, prefer the highest available tier:

| Tier | Authority Class | Examples | Usage Rule |
| --- | --- | --- | --- |
| **Tier 1** | Standards and regulatory bodies | `ISO`, `IEEE`, `W3C`, `IETF RFC`, `NIST`, `COSO`, `IFRS/GAAP`, statutory agencies, peer-reviewed literature | Primary ground truth |
| **Tier 2** | Canonical publishers and domain texts | `O'Reilly`, `Manning`, `Addison-Wesley`, `MIT Press`, `Pearson`, `Wiley`, domain handbooks | Primary ground truth |
| **Tier 3** | Vetted industry and maintainer specs | `Martin Fowler`, `ThoughtWorks Radar`, `OWASP`, `NN/g`, official framework/protocol docs, vetted OSS | Valid when corroborated |
| **Tier 4** | Unranked blogs, Q&A, AI summaries | Personal blogs, unlinked Stack Overflow, community heuristics, LLM explainers | Supporting only; never standalone premise |

## Operational Context (Separate from External Source Tiers)

User conversations, local source code, active project rules, and retired workspace drafts are **Operational Context**, not external empirical authorities:

- **Active Operational Context** (user workflows, project rules, codebase files, requirements): Valid **subject input** for `CRITIQUE`, `CONVERT`, `DISTILL`, and `NAVIGATE`. Treat as local project scope rather than universal technical proof.
- **Archived / Historical Context** (deprecated drafts or legacy prompts): Historical comparison only; never treat as active guidance unless explicitly requested.

```text
ALWAYS separate Operational Context (what the user/project provides) from External Authority (Tiers 1-4).
PREFER Tier 1-3 external sources for factual, security, protocol, and methodological claims.
NEVER promote an unverified Tier 4 blog, community snippet, or LLM summary into a normative premise.
DO NOT invent folder hierarchies that contradict the active workspace's existing layout.
```

## Agent Execution Protocol (Navigation)

When placing or auditing an artifact in any workspace:

```text
Step 1: Inspect the active workspace root and existing config/catalog files dynamically.
Step 2: Classify intent across the 3 axes (AGENT INSTRUCTIONS / DOCUMENTATION & REFERENCE / ARCHITECTURE & DESIGN).
Step 3: Check lifecycle ownership (active vs archived vs third-party) before choosing destination paths.
Step 4: Separate Operational Context inputs from Tier 1-4 external claims; prefer Tiers 1-3 for evidence.
Step 5: Check whether the host project maintains a skill/doc catalog index and remind the user if an entry update is needed.
```

## How the Meta-Skill Uses This

- **Classify** a requested artifact -> determine its intent axis and target workspace path dynamically.
- **Route citations** -> in `EXPLAIN`, `CREATE`, and `CONVERT`, verify external technical rules against `Tier 1-3` and avoid unverified `Tier 4` premises.
- **Organize** -> in `NAVIGATE`, map files cleanly onto the host project's layout without hardcoding external repository conventions.
