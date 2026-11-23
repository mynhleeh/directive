---
name: directive
description: "High-level repository overview, intent-based directory taxonomy, lifecycle rules, canonical 6-tier source trust model, and CLI quickstart for the directive knowledge base. Read to orient across top-level modules before drilling into per-directory indexes."
version: 2.3.0
tags: [directive, overview, taxonomy, architecture, tiers, navigation]
metadata:
  author: "directive"
  scope: "Repository-wide high-level entry point"
---

# Directive

Structured Second Brain and Knowledge Base for AI commanding, built as a high-level entry map shared by human contributors and AI agents.

## Repository Architecture

Directories follow an intent-based taxonomy separating execution directives, learning material, architectural designs, and management tooling.

### Intent-Based Taxonomy

| Intent Axis | Core Question | Resource Types |
| --- | --- | --- |
| [Instructions](instructions/) | Will an AI execute this directly? | Agents, prompts, rules (`*.rule.md`), scripts, skills (`SKILL.md`) |
| [Knowledge](knowledge/) | Will a reader consult this to learn or cite evidence? | Guides, tutorials, academic papers, articles |
| [Blueprints](blueprints/) | Is this a system design, blueprint, or mental model? | Architectures, agent designs, concepts, frameworks |
| [CLI & Tooling](directive-cli/) | How are directives scanned, bundled, or exported? | Interactive CLI, scanner, exporter, `pytest` suite |

### Dynamic Lifecycle States

Folders containing multiple lifecycle states or provenances split into strict mutually exclusive subdirectories:

| State Folder | Provenance | Lifecycle Scope |
| --- | --- | --- |
| `active/` | Owned | Maintained resources in active use (default when no state subfolder exists) |
| `archive/` | Owned | Retired historical resources kept for reference only |
| `external/` | Third-party | Git submodules and vendored external packages |

Owned artifacts stay inside `active/` or `archive/`. Third-party artifacts stay inside `external/` and are deinitialized or removed rather than archived when retired.

### Workspace Layout

```text
directive/
├── README.md                         # High-level repository overview, taxonomy, and tier model
├── blueprints/                       # System designs and mental models
│   ├── architectures/                # System and agent architecture specs
│   └── concepts/                     # Mental models, taxonomies, and frameworks
├── directive-cli/                    # Interactive CLI, scanner, exporter, and pytest suite
├── instructions/                     # Direct AI execution artifacts
│   ├── agents/                       # Custom agent personas and tool definitions
│   ├── prompts/                      # Standalone prompts (active, archive, external)
│   ├── rules/                        # Workspace governance rules (*.rule.md)
│   ├── scripts/                      # Skill extraction and maintenance utilities
│   └── skills/                       # Reusable skills (active, external)
└── knowledge/                        # Learning and evidence documents
    ├── articles/                     # Technical articles and case studies
    ├── guides/                       # Vendor docs, books, and practitioner guides
    └── papers/                       # Peer-reviewed papers and technical reports
```

## Source Trust Tiers

Sources across the repository and external research share a single 6-tier epistemic trust scale based on verification rigor and provenance rather than folder status alone.

| Tier | Classification | Epistemic Criteria | Usage & Citation Policy |
| --- | --- | --- | --- |
| Tier 1 | Normative Standards & Peer-Reviewed Literature | Statutory mandates, formal standards (`ISO`, `IEEE`, `W3C`, `IETF RFC`, `NIST`), peer-reviewed academic papers, formal technical reports | Primary ground truth for empirical claims, formulas, and normative compliance |
| Tier 2 | Official Vendor Specs & Canonical Textbooks | Official primary vendor or protocol documentation, first-party vendor skill suites backed by official specs, canonical technical books from established publishers | Primary ground truth for platform behavior, APIs, and enduring methodology |
| Tier 3 | Vetted OSS & Curated Practitioner Guides | Community-vetted open-source repositories with test suites or broad adoption, vetted practitioner handbooks (`OWASP`, `Martin Fowler`), corroborated architectural designs | Valid engineering workflow and architectural baseline; verify license before reuse |
| Tier 4 | Articles & Niche Community Bundles | Technical articles, case studies, referenced Q&A, and smaller or single-author third-party packages lacking broad verification | Supporting context or candidate reference; corroborate against Tiers 1-3 before normative adoption |
| Tier 5 | AI-Authored & Working Workspace Assets | Self-authored or AI-synthesized instructions, drafts, conceptual models, automation scripts, and active project deliverables | Never standalone scientific or external proof; ground factual claims in Tiers 1-3 |
| Tier 6 | Historical Archives & Unverified Captures | Retired historical artifacts no longer maintained, leaked verbatim prompt captures without official verification, unranked personal blogs, LLM summaries | Historical trace or structural syntax example only; prohibited as factual premise or active guidance |

Exact tier assignments and catalog inventories are managed exclusively in each parent module's `INDEX.md` document (never inside individual file contents or frontmatter).

### Operational Role vs Source Tier

1. Epistemic reliability (`Source Trust Tier`) is independent from workspace obligation (`Operational Role`): vetted third-party sources (`Tier 2-4`) outrank AI-authored internal assets (`Tier 5`) in technical evidence, whereas owned rules and agent specifications remain binding as `Workspace Governance` during repository tasks.
2. Within software or academic project deliveries, project-specific mandates and approved requirements take precedence on domain rules over external standards, while standards draw from `Source Trust Tiers 1-3`.

### Source Governance

1. License verification: inspect each external source's local `LICENSE` file and `.gitmodules` entry before copying or redistributing content.
2. External retirement: remove vendored directories or run `git submodule deinit` for retired external dependencies instead of moving them into `archive/`.
3. Catalog placement: document individual items, tiers, and caveats inside each module's dedicated index file rather than expanding this root file.

## CLI & Metadata Convention

### Directive CLI

The Python toolsuite in [directive-cli](directive-cli/README.md) inventories agents, rules, and skills, updates submodules, resolves skill name collisions deterministically, and scaffolds target `.agents/` workspaces.

```bash
pip install -r directive-cli/requirements.txt
python -m directive_cli.main
python -m pytest directive-cli/tests/ -v
```

Standalone skill export and index generation are available via `python instructions/scripts/extract_skills.py` and `python instructions/scripts/generate_skill_index.py`.

### Frontmatter Convention

Owned markdown directives and skills include a YAML frontmatter header for both human readability and automated indexing:

```yaml
---
name: "Resource name"
description: "Capability scope and trigger conditions"
tags: [tag1, tag2, tag3]
---
```
