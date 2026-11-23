---
name: knowledge-index
description: "Index and tier registry for curated learning and evidence documents under knowledge/ (papers, guides, articles). Read to resolve document tiers, evaluation rules, and current catalog entries."
version: 1.2.0
tags: [knowledge, index, tiers, papers, guides, articles, citations]
metadata:
  author: "directive"
  scope: "All learning and evidence documents under knowledge/"
---

# Knowledge Index

Catalog and source-trust classification for reference documents under `knowledge/`. Canonical definitions of the 6-tier trust scale live in [README.md](../README.md).

## Subfolder Tier Defaults

| Category | Scope | Default Tier | Provenance & Catalog Policy |
| --- | --- | --- | --- |
| [`papers/`](papers/) | Peer-reviewed academic papers and formal technical reports | Tier 1 | Preprints and non-peer-reviewed whitepapers are classified under Tier 3 or Tier 4 in Document Catalog |
| [`guides/`](guides/) | Vendor documentation, canonical books, and practitioner guides | Tier 3 | Official vendor documentation and canonical textbooks are classified under Tier 2 in Document Catalog |
| [`articles/`](articles/) | Technical articles, engineering blog posts, and case studies | Tier 4 | Unverified opinion pieces and summary notes are classified under Tier 6 in Document Catalog |

## Document Catalog

| Document | Category | Tier | Notes |
| --- | --- | --- | --- |
| [The Complete Guide to Building Skills for Claude](guides/the-complete-guide-to-building-skill-for-claude.pdf) | `guides/` | Tier 2 | Official Anthropic skill-authoring methodology guide (vendor PDF) |

`papers/` and `articles/` currently contain no documents beyond `.gitkeep` placeholders.

## Maintenance Rules

1. Register each new document in `Document Catalog` with its subfolder, verified Tier, and concise scope note.
2. Manage source tiers exclusively within `Document Catalog` in this file. Never record tier metadata inside individual document files or frontmatter.
3. Keep retired or superseded knowledge files only if historically needed; otherwise remove obsolete drafts cleanly.
