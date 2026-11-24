---
trigger: glob
globs: "**/*"
description: "Mechanical, context-neutral standards for naming, delimiter hierarchy, depth capping, and directory hygiene across workspace storage."
---

# File and Folder Organization Rules

Defines mechanical, context-neutral conventions for organizing, naming, moving, and standardizing files and folders across any digital workspace for both human contributors and automated agents.

## 1. Core Axioms

1. **Delimiter Hierarchy:** Hyphens (`-`) separate major semantic parts; underscores (`_`) join constituent words within a single semantic part.
2. **Context-Aware Language:** Default to standard technical English for international portability; allow ASCII-transliterated native names only when translation causes recognition loss against official records.
3. **Strict Encapsulation:** Never leave raw asset files floating at a scope unit's root directory alongside functional subfolders when they belong to a specific category pool.
4. **Deterministic Predictability:** Express every character, delimiter, depth, and date rule as a binary Pass/Fail check with zero subjective judgment.

## 2. Mechanical Naming Standards and Delimiter Hierarchy

### 2.1. Two-Tier Delimiter Hierarchy

To maximize human readability and automated string parsing, filenames and directories follow two delimiter levels:

- **Macro Delimiter (`-`):** Separates **independent semantic parts** (for example, `[Prefix/Date]-[Entity]-[Category]-[Suffix]`).
- **Micro Delimiter (`_`):** Joins **words inside a single part** whenever a name contains 2 or more semantic parts.

```text
General multi-part structure (>= 2 parts):
[part_one]-[part_two]-[part_three]
  ^          ^          ^
  |          |          +-- Internal words joined with snake_case (_)
  +----------+------------- Parts separated with kebab-case (-)
```

#### Branching Rules by Part Count

| Semantic Parts | Syntax | Delimiter Rule | Neutral Examples |
| --- | --- | --- | --- |
| **Single-part (1 part)** (subject, topic, or category name) | Pure `kebab-case` | Use `-` only to join words | `discrete-math`, `presentation-skills`, `digital-electronics`, `phap-luat-dai-cuong` |
| **Multi-part (>= 2 parts)** (ordered prefix, date, type, or suffix) | Hybrid (`kebab-case` outer, `snake_case` inner) | Use `-` between parts and `_` inside each part | `01-system_architecture`, `2026_03_31-quarterly_review`, `component_a-test_suite`, `module_alpha-lecture_notes` |

### 2.2. Sequence Numbering

- Zero-pad all sequence numbers to preserve natural lexicographical sorting across filesystems:
  - Sequences under 100 items: minimum 2 digits (`01`, `02`, `03`, ..., `99`).
  - Sequences of 100 or more items: minimum 3 digits (`001`, `002`, ..., `999`).
- Apply the delimiter hierarchy when pairing numbers with descriptive content: `nn-<part_two_content>` (for example, `01-introduction_overview.md`, `02-core_analysis.pdf`).

### 2.3. Temporal Tokens

- Treat any date or month token as an **independent semantic part**:
  - Standalone date directory or file: ISO 8601 (`YYYY-MM-DD`).
  - Multi-part filename containing a date: join date components with `_` and separate from the content part with `-`: `YYYY_MM_DD-<content_name>` (for example, `2026_03_31-annual_summary_report.pdf`) or month-level `YYYY_MM-<content_name>` (for example, `2026_03-quarterly_review`).

### 2.4. Allowed Character Set

- **Allowed:** Lowercase ASCII letters `a-z`, digits `0-9`, hyphen `-`, underscore `_`, and period `.` (for file extensions only).
- **Strictly Forbidden:**
  - Spaces.
  - Uppercase letters (`A-Z`).
  - Special characters (`@`, `#`, `$`, `%`, `&`, `*`, `(`, `)`, `+`, `=`, `[`, `]`, `{`, `}`).
  - Unicode accented characters (transliterate all non-ASCII letters to plain unaccented ASCII).

## 3. Context-Aware Language Policy

Apply a two-tier priority rule to balance technical standardization with accurate official record lookup:

```text
[Tier 1: Default]     Standard technical English (English-first)
        |
        v (Recognition-loss exception)
[Tier 2: Exception]   ASCII-transliterated native name when English translation
                      degrades official record identification
```

### 3.1. Tier 1: English-First Default

Apply English names mandatorily to:

- 100% of Level 3 functional pool directories (`docs/`, `references/`, `slides/`, `assessments/`, `templates/`, `reports/`, `images/`).
- Universal academic, scientific, or engineering subjects and technologies (`computer-architecture`, `discrete-math`, `probability-statistics`, `digital-electronics`).
- Technical status markers and data categories.

### 3.2. Tier 2: Identity Preservation Exception

Apply ASCII-transliterated native naming only when:

- A course, statutory text, or institutional record carries a localized legal, civic, or curriculum title whose English translation causes recognition loss against official transcripts or records.
- Convert 100% to **lowercase unaccented ASCII** obeying Section 2 delimiter rules (for example, preserve `phap-luat-dai-cuong`, `triet-hoc-mac-lenin`, `ky-nang-lam-viec-nhom`; standardize universal subjects in English such as `algebra`, `calculus-01`, `physics`).

## 4. Four-Level Directory Hierarchy

Keep organized workspace storage within a maximum depth of **4 levels** from the workspace root:

```text
Level 0: [Workspace Root]
  +-- Level 1: [Domain Namespace]          (e.g., engineering/ or archives/)
        +-- Level 2: [Scope / Entity]      (e.g., discrete-math/ or project_alpha-phase_01/)
              +-- Level 3: [Category Pool] (e.g., docs/ or references/ - plural nouns)
                    +-- Level 4: [Target]  (e.g., 01-system_overview.md)
```

- **Level 1 (Domain Namespace):** Top-level functional domain (such as `academics`, `operations`, `certifications`).
- **Level 2 (Scope Unit):** Independent course, project, module, or event container.
- **Level 3 (Functional Category):** Resource purpose pool, named using **plural English nouns** (Section 5).
- **Level 4 (Target Artifact):** Actual content file.

## 5. Pluralization and Functional Category Matrix

Standardize all Level 3 functional directories as plural English nouns (with `archive/` as the sole lifecycle singular exception):

| Standard Directory | Number Form | Scope Inside Directory |
| --- | --- | --- |
| `docs/` | Plural | Specifications, guides, meeting minutes, synthesized notes |
| `references/` | Plural | Textbooks, third-party reference manuals, external standards |
| `slides/` or `presentations/` | Plural | Slide decks and lecture or defense presentations |
| `assessments/` or `exams/` | Plural | Exams, quizzes, grading rubrics, answer keys |
| `exercises/` or `assignments/` | Plural | Practice sets, lab exercises, coursework assignments |
| `images/` or `media/` | Plural | Diagrams, screenshots, figures, audio, and video assets |
| `templates/` | Plural | Reusable document scaffolds and boilerplate forms |
| `reports/` | Plural | Periodic reports, acceptance deliverables, progress summaries |
| `data/` or `datasets/` | Collective | Raw spreadsheets, experimental logs, empirical measurement files |
| `archive/` | Singular | Historical records whose active lifecycle has completely ended |

## 6. Root Hygiene Principles

1. **Max-1 Index Rule:** Allow at most **1** overview/index file (such as `overview.md` or `index.md`) at the root of each Level 2 Scope Unit.
2. **No Floating Assets:** Place all image files (`.png`, `.jpg`), office/document files (`.docx`, `.xlsx`, `.pptx`, `.pdf`), and media files (`.mp3`, `.mp4`) inside their matching Level 3 category folders (`docs/`, `references/`, `images/`, etc.), never loose alongside subdirectories at Level 2 root.
3. **Eliminate System Junk and Shortcuts:** Never store OS shortcut files (`.lnk`), and remove or ignore environment display/cache metadata (`desktop.ini`, `.DS_Store`, `Thumbs.db`).

## 7. Violation Comparison and Normalization Table

| Legacy / Violation | Standardized Form | Engineering Rationale |
| --- | --- | --- |
| `calculus_01` (uses `_` in 1 part) | `calculus-01` | Single-part name uses pure `kebab-case`. |
| `2022_10_30-modern-cultural-achievements` | `2022_10_30-modern_cultural_achievements` | Multi-part name: date (`2022_10_30`) separated by `-` from `_`-joined content (`modern_cultural_achievements`). |
| `day_29-test-voice_01.mp3` | `day_29-voice_test_01.mp3` | Multi-part name: `day_29` (part 1) separated by `-` from `voice_test_01` (part 2). |
| `pháp-luật-đại-cương/` (accented Unicode) | `phap-luat-dai-cuong/` | Preserves local identity in unaccented lowercase ASCII with single-part `kebab-case`. |
| `General-Law/` (forced translation) | `phap-luat-dai-cuong/` | Identity preservation exception avoids record-lookup recognition loss. |
| `reference/` alongside `references/` | `references/` | Enforces plural noun convention for reference pools. |
| `essay/` alongside `exercises/` | `exercises/` or `assignments/` | Consolidates small essays into standard plural exercise pools. |
| `desktop.ini`, `file.lnk` | *(Deleted)* | Purges OS metadata and shortcut clutter carrying zero domain value. |

## 8. Verification Checklist

Every newly created or reorganized file and folder must pass all 6 mechanical gates:

- [ ] **Gate 1 (Delimiter Rule):** Single-part names use `-` (`kebab-case`) only; multi-part names (`>= 2` parts) use `-` between parts and `_` inside each part.
- [ ] **Gate 2 (Language and ASCII Check):** Zero accented characters, uppercase letters, or spaces; English used by default, with lowercase ASCII transliteration reserved strictly for local identity-preservation exceptions.
- [ ] **Gate 3 (Depth Check):** Zero data files placed deeper than Level 4 under organized storage roots.
- [ ] **Gate 4 (Root Hygiene Check):** Level 2 scope directories hold zero loose media/document files alongside subdirectories and at most 1 index/overview file.
- [ ] **Gate 5 (Plurality Check):** 100% of Level 3 functional folders follow the plural English nouns in Section 5.
- [ ] **Gate 6 (Date Format Check):** Multi-part dated artifacts follow `YYYY_MM_DD-<content>` or `YYYY_MM-<content>`.
