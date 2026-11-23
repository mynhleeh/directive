---
name: blueprints-index
description: "Index and tier registry for system architectures and conceptual models under blueprints/ (architectures, concepts). Read to resolve design document tiers, evaluation rules, and current catalog entries."
version: 1.1.0
tags: [blueprints, index, tiers, architectures, concepts, design]
metadata:
  author: "directive"
  scope: "All system designs and conceptual models under blueprints/"
---

# Blueprints Index

Catalog and source-trust classification for architectural designs and mental models under `blueprints/`. Canonical definitions of the 6-tier trust scale live in [README.md](../README.md).

## Subfolder Tier Defaults

| Category | Scope | Default Tier | Provenance & Catalog Policy |
| --- | --- | --- | --- |
| [`architectures/`](architectures/) | System topologies, agent architectures, and multi-component design specifications | Tier 3 | Unreviewed AI-authored drafts are classified under Tier 5 in Blueprint Catalog until corroborated |
| [`concepts/`](concepts/) | Mental models, conceptual taxonomies, and working design frameworks | Tier 5 | Validated conceptual frameworks are promoted to Tier 3 in Blueprint Catalog after empirical proof |

## Blueprint Catalog

`architectures/` and `concepts/` currently contain no documents beyond `.gitkeep` placeholders.

When adding the first blueprint document, create a compact catalog table with columns `Blueprint`, `Category`, `Tier`, `Lifecycle State`, and `Summary` embedding the relative path in `Blueprint`.

## Maintenance Rules

1. Add a row to `Blueprint Catalog` whenever introducing a design document under `architectures/` or `concepts/`.
2. Manage source tiers exclusively within `Blueprint Catalog` in this file. Never record tier metadata inside individual blueprint files or frontmatter.
3. Move retired blueprints to an explicit `archive/` subdirectory only when historical provenance is needed.
