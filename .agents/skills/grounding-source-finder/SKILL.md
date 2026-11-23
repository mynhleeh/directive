---
name: grounding-source-finder
description: "Use when a design choice, business rule, policy, formula, or methodological decision across any domain lacks coverage in local files and needs external standards, canonical books, or vetted specifications before proceeding. Trigger on 'find a source', 'need a reference', 'cơ sở lý thuyết', 'tìm chuẩn cho quyết định', or ungrounded rule gaps. Do NOT trigger for academic papers, DOIs, PubMed/arXiv preprints, or systematic reviews (use paper-lookup, deep-literature-search, or research-lookup), nor for local file lookups."
version: "2.0.0"
tags:
  - grounding
  - standards
  - business-rules
  - architecture
  - decision-support
  - source-vetting
  - cross-domain
license: MIT
compatibility: "Platform-agnostic. Portable with zero hardcoded workspace paths; requires web search or fetch for live link verification."
---

# Grounding Source Finder

> Find and vet external standards, canonical books, and industry specifications to ground unverified decisions, rules, and designs across any domain before finalizing or saving them.

## Scope Exclusions

- Academic papers, DOIs/PMIDs/arXiv preprints, citation graphs, or PRISMA literature reviews -> delegate to `paper-lookup`, `deep-literature-search`, or `research-lookup`.
- Existing workspace files (`docs/`, `references/`, `policies/`, `knowledge/`) -> read local files directly.

## Language Policy

Follow these English instructions internally. Respond in the user's writing language while preserving established English technical terms.

## Workflow

1. **Check internal tiers dynamically**: Inspect local project folders first, then shared workspace folders (`docs/`, `policies/`, `standards/`, `references/`, `reference/`, `academic/`, `knowledge/`). If covered internally, cite that path and stop.
2. **Generalize to problem class**: Restate the narrow question as a domain-neutral problem class before searching, and print it in `Working Notes` so misframing is caught early.
3. **Search >= 2 Tier 1-3 surfaces**: Query at least two independent surfaces from the ladder below and cross-check critical claims across >= 2 sources.
4. **Verify every URL live**: Open or fetch each candidate link in this session to confirm it resolves the problem class. Never cite from memory or search snippets alone. Mark paywalled items and prefer comparable open-access equivalents.
5. **Stop at Confirmation Gate**: Emit the `Output Contract` block and wait for explicit user approval before writing deliverables or saving references locally.

| Narrow user ask | Generalized problem class |
| --- | --- |
| "Pro-rate mid-cycle upgrades and round VND/USD cents" | Mid-cycle subscription proration and currency minor-unit rounding |
| "Approve refunds over 500 USD and log sensitive edits" | Dual-control authorization (segregation of duties) and tamper-evident audit logging |
| "Set SLA timeouts for urgent vs normal support tickets" | Multi-tier service-level queue prioritization and escalation thresholds |

## Source Authority Ladder

| Tier | Authority Class | Examples | Rule |
| --- | --- | --- | --- |
| **Tier 1** | Standards and regulatory bodies | `ISO`, `IEEE`, `W3C`, `IETF RFC`, `NIST`, `COSO`, `IFRS/GAAP`, statutory agencies | Primary ground truth |
| **Tier 2** | Canonical publishers and domain texts | `O'Reilly`, `Manning`, `Addison-Wesley`, `MIT Press`, `Pearson`, `Wiley`, domain handbooks | Primary ground truth |
| **Tier 3** | Vetted industry and maintainer specs | `Martin Fowler`, `ThoughtWorks Radar`, `OWASP`, `NN/g`, official framework/protocol docs | Valid when corroborated |
| **Tier 4** | Unranked blogs, Q&A, AI summaries | Personal blogs, unlinked Stack Overflow, LLM explainers | Supporting only; never standalone |

Require current editions (`<= 3` years or active standard) for security, compliance, protocols, and APIs; accept enduring texts (`10+` years) for invariant theory, algorithms, and accounting principles.

## Output Contract

Emit one block in the user's language containing only live-verified URLs (if none qualify, state `"No verified Tier 1-3 source found"` and ask whether to broaden the class or record an explicit assumption):

```markdown
## Working Notes
- Concrete question: [restate ask]
- Generalized problem class: [domain-neutral class]
- Internal tiers checked: [discovered paths -> not covered]
- Search surfaces used: [>= 2 Tier 1-3 surfaces]

## Candidate Sources
| # | Title | Author / Body | Year | Tier | Link | Problem-Class Coverage |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ... | ... | ... | Tier 1..3 | [verified URL + access note] | ... |

## Recommendation
[Synthesis across >= 2 sources in 1-2 sentences, noting trade-offs]

## Next Step
Awaiting confirmation before registering [title, author/body, year, URL] into [target path].
```

## Discipline Guardrails

**Violating the letter of these rules is violating the spirit of these rules.**

| Rationalization Under Pressure | Non-Negotiable Reality |
| --- | --- |
| "Demo or sprint is blocked; pick one top blog or vendor doc and save it now." | Urgency never bypasses vetting or confirmation. Emit vetted options and wait. |
| "I know the standard citation from memory; skip opening the URL." | Memory fabricates editions and links. Verify every URL live in this session. |
| "Search literally for the user's exact feature wording." | Narrow terms miss standards and textbooks. Generalize to the problem class first. |
| "Workspace uses `standards/` or `policies/`, not `docs/reference/`, so skip local check." | Discover local and shared documentation folders dynamically before external search. |

Red flags requiring immediate stop: unverified or memory citations; standalone Tier 4 blogs; missing `Working Notes`; writing into workspace files without confirmation.
