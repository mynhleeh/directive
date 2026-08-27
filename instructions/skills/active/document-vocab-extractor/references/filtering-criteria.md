# Document Vocab Extractor — Filtering Criteria & Refinement Passes

Read this when applying Phase 2 (Filtering) and Phase 2.5 (Refinement). This holds the full category definitions and the four passes.

## Category Definitions (Phase 2)

### Category A — Domain-Specific Terms & Technical Vocabulary
Any word, phrase, or expression that is specific to the subject domain of the document, regardless of whether it appears simple in everyday English. This includes specialized nouns, verbs, and adjectives used with a field-specific meaning. Apply this category using the domain implied by the document itself — do not assume a fixed domain in advance.

### Category B — Abbreviations, Acronyms & Proper Technical Nouns
Any abbreviation, acronym, initialism, or proper name that carries a specific technical or conceptual meaning within the context of the document.

**Crucial Acronym Rule:** When extracting an acronym, output its **full expanded form** as the main Word in Col 1. Do NOT translate the words literally. Instead, use the document context together with your knowledge to **explain what it is and what it does** in the Meaning column. Put the short acronym itself in the Synonyms column.

### Category C — Mid-to-High Difficulty General Vocabulary (CEFR B2+)
Any general English word or phrase that is at CEFR B2 level or above and appears in a context that gives it weight or importance. This includes abstract verbs, precise adjectives, formal nouns, and idiomatic expressions used in a professional or academic register.

### Category D — Author-Highlighted / Defined Terms
Any word or phrase that the author:
- Places in **quotation marks** or *italics*
- Defines explicitly using phrases like "known as", "called", "referred to as", "that is,", "defined as", "termed", or similar
- Introduces as a new concept or technical term for the first time

### Category E — High-Frequency Words Within the Document
Any word or phrase that appears **3 or more times** within the document, even if it seems common, because repetition signals importance within this specific context.

### Quantity Rule
- Do NOT set an upper limit on the number of words extracted.
- Output **all** words that satisfy at least one category above.
- Do not merge separate technical terms into a single compound entry — extract each significant term independently.

## Refinement Passes (Phase 2.5)

Apply these in order before producing the final output.

### Pass A — Multi-Word Expression Decomposition

For every multi-word candidate, apply this single decision question:

> *If I look up each component word individually and combine their meanings, do I arrive at the same meaning as the full phrase?*

- **Yes (meaning is compositional)** → The phrase is a literal combination. Decompose it and extract only the individual words that meet filtering criteria on their own.
- **No (meaning is non-compositional), OR the author explicitly named/defined this phrase as a unit** → Keep the phrase intact as a single entry.

This principle applies regardless of domain, word count, or language register. It covers technical compounds, idioms, proper nouns used as unified concepts, and author-defined terminology equally.

### Pass B — Merged / Joined Term Splitting

Scan the document for tokens where multiple distinct terms have been merged into one using any connecting symbol (slash, ampersand, plus sign, interpunct, or similar). When you find such a token:

1. Identify each component as an independent extraction candidate.
2. Apply all filtering criteria (Phase 2) and Pass A to each component separately.
3. Extract qualifying components as individual entries; do not carry the merged token into the output as-is.

This applies regardless of the specific symbol used, the number of components in the merged token, or the domain of the document.

### Pass C — Meaning Quality Enforcement

For every entry, evaluate whether the Meaning field (Col 2) genuinely explains *what the term is or does* from the learner's perspective — not merely restating or transliterating the word.

1. **Is the Meaning field substantively different from the Word field?**
   - No → proceed to step 2.
   - Yes → entry is acceptable; move on.
2. **Is this entry purely a bibliographic reference or citation marker** (i.e., its only function in the document is to credit a source, and it carries no independent concept the learner needs to understand)?
   - Yes → **remove the entry entirely from the output**.
   - No → proceed to step 3.
3. **Can a meaningful explanation be found?**
   - Search the internet for a concise definition. If search is unavailable, apply your own knowledge.
   - Write the Meaning in Vietnamese, no longer than two sentences, explaining what the term is or does.
   - If even after this step no substantive meaning can be constructed → remove the entry.

### Pass D — Deduplication

Review the full list and remove entries where the same Word appears with the same core meaning. If the same Word has genuinely distinct meanings in the document, retain one row per distinct meaning.
