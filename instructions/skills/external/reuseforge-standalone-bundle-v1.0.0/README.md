# ReuseForge Standalone Bundle v1.0.0

Protocol: `reuseforge/1.0`

This package contains the complete 9-Skill ReuseForge family as a **standalone distribution**. It does **not** require Solo Builder Dev Orchestrator, Aki, A2, Orca, or any private runtime to install.

## Important installation rule

**Do not upload this outer ZIP as one Skill.** It contains multiple Skills. Extract it first, then upload each ZIP inside `skills/` individually from ChatGPT `/skills`.

Recommended order:

1. `reuseforge-orchestrator.zip`
2. `reuseforge-project-framer.zip`
3. `reuseforge-asset-scout.zip`
4. `reuseforge-candidate-auditor.zip`
5. `reuseforge-solution-architect.zip`
6. `reuseforge-project-planner.zip`
7. `reuseforge-execution-handoff.zip`
8. `reuseforge-repair-router.zip`
9. `reuseforge-memory-recovery.zip`

Install all 9 for the complete workflow. The order is recommended for clarity; the member packages are independently valid Skills.

## Core workflow

`Idea -> Framing -> Gate A -> Discovery -> Candidate Audit -> Architecture -> Gate B -> Planning -> Gate C -> Execution Handoff`

Conditional branches:

- execution/integration failure -> `reuseforge-repair-router`
- new chat/context loss/stale state -> `reuseforge-memory-recovery`

The Orchestrator routes work and enforces lifecycle legality. It does not silently perform specialist work or approve Gates for the Human.

## Solo Builder integration

Solo Builder Dev Orchestrator is **optional**. When installed, ReuseForge may be used as the Reuse Review subworkflow before Solo Builder DEV Gate C. The two Gate systems remain separate:

- Solo Builder: DEV Gates A-E
- ReuseForge: RF Gates A-C

ReuseForge does not replace Solo Builder, Repo Execution Controller, Aki, A2, or Orca.

## Environment-dependent capabilities

Some tasks can use web search, GitHub access, repository files, Codex/OpenCode, or an external executor. Availability depends on the recipient's ChatGPT plan, enabled tools/connectors, and local environment. Missing optional tools should reduce capability, not invalidate the Skill package itself.

## Verification performed before distribution

- Official Skill Creator validator: 9/9 PASS
- Package -> extract -> revalidate: 9/9 PASS
- ZIP integrity: 9/9 PASS
- JSON and YAML parse: PASS
- Internal `references/`, `scripts/`, and `assets/` path resolution: 59/59
- Shared ReuseForge protocol references: identical across all 9 members
- Hard references to Solo Builder / Aki / A2 / Orca: none detected

See `TEST_REPORT.md` and `CHECKSUMS.sha256` for details.
