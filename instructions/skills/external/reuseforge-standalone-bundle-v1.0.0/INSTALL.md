# Installation and first-use checklist

## Install

1. Extract `reuseforge-standalone-bundle-v1.0.0.zip`.
2. Open ChatGPT `/skills`.
3. Upload each file from `skills/` **one at a time**.
4. Confirm that all nine ReuseForge Skills appear in the Skill library.
5. Start with the Orchestrator for new or ambiguous ReuseForge work.

## First smoke test

Use a small disposable idea, for example:

> Use ReuseForge Orchestrator. I want to build a local document-search app and I want to reuse existing open-source components where practical. Start at the correct ReuseForge stage and do not skip approvals.

Expected behavior:

1. Orchestrator routes to project framing.
2. Project Framer creates capability-level framing and stops for explicit Gate A approval.
3. It must **not** jump directly to repository search, architecture, planning, or implementation before the required state/Gate.

After Gate A, a second smoke test can ask for discovery of one approved capability. Asset Scout should discover candidates but must not claim that a candidate is suitable until Candidate Auditor has audited it.

## If something appears wrong

- A member ZIP failing to upload: verify its SHA-256 against `CHECKSUMS.sha256`.
- A workflow skipping a Gate: explicitly invoke `@ReuseForge Orchestrator` and ask it to validate canonical lifecycle state.
- A candidate being selected from README/stars alone: route it through `reuseforge-candidate-auditor`.
- A new chat losing state: use `reuseforge-memory-recovery` with the canonical repository state files.
- A repository/API/version failure during execution: use `reuseforge-repair-router`; it should diagnose before repair.

## Do not do this

- Do not upload the outer bundle as a single Skill.
- Do not install only the Orchestrator if you expect the complete end-to-end workflow.
- Do not treat RF Gate approvals as Solo Builder DEV Gate approvals, or vice versa.
- Do not treat structural validation as proof that the recipient has GitHub/web/executor access.
