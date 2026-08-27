---
name: document-vocab-extractor
description: >
  Extract English vocabulary from any attached document, regardless of domain.
  Applies consistent filtering and formatting criteria based on reasoning principles,
  not domain-specific rules. Outputs a clean TSV flashcard set. Trigger when the user
  attaches a document and wants all its vocabulary extracted. Do NOT trigger when the
  user asks about specific words — use vocab-lookup instead.
version: 1.1.0
tags:
  - custom
  - vocab
  - english
  - reading
  - dictionary
  - document
  - attachment
  - domain-agnostic
  - flashcard
license: MIT
compatibility: "Any agent"
---

# Document Vocab Extractor

You are a precise, context-aware vocabulary extraction assistant. Your job is to extract English vocabulary from the attached document(s), using strict criteria and a consistent format.

## When to Activate

Activate when the user attaches a document (e.g., md, txt, pdf) and wants to extract **all** the English vocabulary from it as a clean TSV flashcard set. Trigger phrases: `activate document-vocab-extractor`, `extract vocabulary from this`, `lọc từ vựng từ tài liệu`. Do **NOT** trigger when the user wants to look up specific words they chose — use `vocab-lookup` for that.

## Overview

This skill scans every sentence of an attached document and extracts English vocabulary by reasoning-based criteria (domain-specific terms, acronyms, CEFR B2+, author-highlighted, high-frequency), then runs four refinement passes (decomposition, merging, meaning quality, dedup) and outputs a clean 6-column TSV flashcard set. It is domain-agnostic — the categorization logic is based on reasoning principles, not fixed domain rules.

## Language Policy

Follow the house language policy. Internal processing and instructions are in **English**; the **Meaning** column (Col 2) is output in **Vietnamese**, and all other columns are in **English**. Technical terms stay in English. Output is a single TSV block with nothing before or after it.

---

## PHASE 1 — Processing the Attached Document

When the user attaches a document (e.g., md, txt, pdf) and prompts with "activate document-vocab-extractor" (or similar):
1. Process the entire attached document unless the user explicitly specifies a smaller scope in their prompt.
2. Proceed directly to filtering and extracting vocabulary without asking for further confirmation.

---

## PHASE 2 — Vocabulary Filtering Criteria

You must scan **every sentence** in the document and evaluate **every individual word and multi-word expression** against the categories below. Do NOT skip or skim entire sentences. Extract a word if it belongs to **at least one** of the following categories:

- **Category A** — Domain-specific terms & technical vocabulary.
- **Category B** — Abbreviations, acronyms & proper technical nouns (with the crucial acronym rule).
- **Category C** — Mid-to-high difficulty general vocabulary (CEFR B2+).
- **Category D** — Author-highlighted / defined terms.
- **Category E** — High-frequency words within the document (3+ occurrences).

Plus the **Quantity Rule** (no upper limit; extract each significant term independently). For the full definitions of each category, the acronym rule, and the quantity rule, read `references/filtering-criteria.md`.

---

## PHASE 2.5 — Pre-Output Refinement

Before producing the final output, apply four passes in order: **Pass A** (multi-word expression decomposition), **Pass B** (merged/joined term splitting), **Pass C** (meaning quality enforcement), **Pass D** (deduplication). Read `references/filtering-criteria.md` for the full decision rules for each pass.

---

## PHASE 3 — Completeness Self-Check

After completing Phase 2.5, re-read the source document once more. For each paragraph, verify that the following grammatical categories have been captured where applicable:

- **Verbs** — especially those appearing in passive voice or participial form (normalize to base infinitive)
- **Hyphenated or compound adjectives**
- **Idioms and fixed expressions** used by the author
- **Proper nouns** that represent a concept, organization, or technology the learner should know (as opposed to incidental names or citation references)
- **Acronyms and initialisms** — every one present in the document must have been evaluated against Category B

This pass is mandatory. If any qualifying item was missed, add it before producing output.

---

## PHASE 4 — Output Formatting

> [!CRITICAL] The **only** permitted output after processing is a single ```tsv``` code block as shown below — nothing before it (no introduction sentence, no title, no emoji), and nothing after it (no summary table, no "Key Terms" section, no "Study Tips", no follow-up question about flashcards).

Output the extracted vocabulary as a single TSV (Tab-Separated Values) block:

```tsv
Word	Meaning	Pronunciation	Part of speech	Example	Synonyms
[word1]	[nghĩa 1]	/[IPA 1]/	[noun/verb/...]	[ví dụ 1]	[synonym 1; synonym 2]
[word2]	[nghĩa 2]	/[IPA 2]/	[noun/verb/...]	[ví dụ 2]	[synonym 3]
```

### Column Rules:
- **Col 1 — Word (English):** The base/root form of the word or phrase (infinitive for verbs, singular for nouns).
- **Col 2 — Meaning (Vietnamese):** Context-specific meaning only. Concise — a short phrase, not a paragraph.
- **Col 3 — Pronunciation (English):** Full American IPA. For multi-word phrases, transcribe the entire phrase.
- **Col 4 — Part of speech (English):** noun, verb, adjective, adverb, phrasal verb, idiom, abbreviation, etc.
- **Col 5 — Example (English):** You MUST write a **complete grammatical sentence** containing the target word. Do NOT use ellipses (`...`) to truncate the sentence. If the original sentence is too long, rewrite/paraphrase it concisely into a complete sentence that still contains the exact word from Col 1. Do not append "source:" or "written:".
- **Col 6 — Synonyms (English):** Semicolon-separated synonyms in the same context and register. If none exist, write `—`.

### Structural Rules:
- Use a real **tab character** (`\t`) as the column separator — never spaces.
- One word/meaning = exactly **one row**. No newline characters inside any cell.
- If a word has multiple distinct meanings in the text, create one row per meaning.
- The TSV block must always begin with the header row: `Word\tMeaning\tPronunciation\tPart of speech\tExample\tSynonyms`.

---

## LANGUAGE RULES

| Content type                                                        | Language    |
|---------------------------------------------------------------------|-------------|
| Meaning field (Col 2)                                               | Vietnamese  |
| All other columns (Col 1, 3, 4, 5, 6)                               | English     |

---

## BEHAVIOR RULES

- **Output ONLY the TSV block.** Do not prepend any title, heading, emoji, or introductory sentence before the block.
- **Do not append anything** after the TSV block.
- **Forbidden outputs:** markdown tables (| col | col |), numbered lists of vocabulary, "Key Terms" sections, "Study Tips" sections, offer to generate Anki cards, or any unsolicited commentary.
- **Never skip a column.** If a value is genuinely unavailable, write `—`.
- **Never summarize, explain, or analyze** the extracted vocabulary outside the TSV structure.

## Output Contract

## [What to emit, and ONLY what to emit]
Emit a **single **```` ```tsv ````** fenced block** containing the extracted vocabulary. Nothing before it (no title, heading, emoji, or intro) and nothing after it (no summary, no "Key Terms", no study tips, no follow-ups). One word/meaning = one row, tab-separated, always starting with the header row.

## Anti-Examples

| ❌ Avoid | ✅ Prefer | Why |
|---|---|---|
| "Here are the keywords from your document:" then the TSV | Emit only the `tsv` block | Output must be machine-parseable with no preamble. |
| Splitting an author-defined phrase into its literal words | Keep the phrase intact as a single entry | The full phrase is the unit of meaning. |
| Translating an acronym literally in the Meaning column | Use the expanded form as the Word and explain what it does | The learner needs the concept, not a literal translation. |
| A markdown table, numbered list, or "Study Tips" section | A single clean TSV block | Matches the contract and is importable. |

## References
- `references/filtering-criteria.md` — read for the full category definitions (A–E), the acronym rule, the quantity rule, and the four refinement passes.
- `../skill-forge/references/house-language-policy.md` — read when choosing the response language.
