# Execution Protocol — longCOT, Audit Loop, Weak-Model-First

Reference for `SKILL.md` v3.0.0. Read this file at **STAGE 2 THINK** (pick the mode's sub-questions) and **STAGE 4 EVALUATE** (run the stranger-audit). It makes the pipeline executable by an average model: every step is a fixed question or a countable check, never a judgment call.

> **Weak-model-first rule (Principle 1):** if any step below reads like "be careful" or "use good judgment," it is broken — replace it with a numbered question or a pass/fail boundary.

---

## 1. STAGE 2 THINK — Fixed Sub-Questions per Mode

Run **all** sub-questions for your mode, in order, inside the internal chain-of-thought. Do not skip any; do not merge two into one. Each must be answered with a concrete fact or decision, then compressed into the `## Working Notes` block (1 line per decision, one-line rationale).

### Common prelude (all modes)
1. **Restate:** What exactly is the user asking for? (≤2 lines, own words)
2. **Classify:** mode · artifact type · intensity tier · platform · language — one word each.
3. **Known vs missing:** list what the input provides (KNOWN) and what it lacks (AMBIGUOUS/MISSING).
   - If AMBIGUOUS/MISSING contains anything that would change the artifact → **STOP, go to CLARIFY gate** (ask max 3, one batch, each with a default option).
   - If the input is complete → proceed.
4. **Acceptance criteria:** write 2–4 countable criteria the final output must satisfy (these feed STAGE 5 TEST).

### CREATE (skill / prompt / schema / rules)
5. **Type recipe:** which reference file is canonical for this type? (`skill-guide.md` + `house-structure-conventions.md` for skills, `system-prompt-guide.md` for system prompts, `function-schema-guide.md` for schemas, `rules-guide.md` for rules)
6. **Tier check:** does the requested depth match micro / standard / deep engine? (`domain-engine-tiers.md`) If the request is one workflow but the tier chosen is "deep engine," the tier is wrong.
7. **Countability scan:** for each planned instruction, is there a number, threshold, or fixed recipe? If an instruction would require judgment to execute, rewrite it before generation.
8. **Example plan:** which examples illustrate the artifact? Are they neutral and generalizable (no real brand/domain names, no single-case hardcode)?

### CRITIQUE
5. **Defect inventory:** list each issue with the criterion it fails (Clarity / Completeness / Consistency / Specificity / Format fit / Language) — one line per defect.
6. **Root cause:** for each defect, what *principle* was violated? (Fix the principle, not the instance — Principle 2.)
7. **Auto-fixable vs needs-ask:** which defects can be fixed unambiguously, and which require the user (ambiguous intent)? Needs-ask → CLARIFY gate.

### CONVERT
5. **Mapping table:** which row of the platform matrix applies? (OpenAI ↔ Anthropic ↔ MCP ↔ Gemini ↔ platform-agnostic)
6. **Loss audit:** which fields exist in source but have no target equivalent (`strict`, `title`, `outputSchema`, type casing, XML tags)? Each is either dropped with justification or preserved with an alternative.
7. **Round-trip plan:** convert back in the notes and diff — list expected differences before running it.

### EXPLAIN
5. **Essential shape:** what is the concept's core mechanism in one sentence?
6. **Generalization:** does the user's question reference a specific case? Abstract it to the general pattern first (Principle 2).
7. **Audience calibration:** what level is the user (beginner/intermediate/expert) — from their wording, not guessed expertise.

### DISTILL
5. **Workflow extraction:** tools/actions used, step order, corrections, input/output formats — enumerated from the source.
6. **Artifact types:** which artifact type(s) emerge? (skill family? single skill? prompt?)
7. **Transmutation:** for every specific user case in the source, what general rule covers the whole class of cases?
8. **Provenance plan:** source + tier, generalization moves, excluded unverified content — to be written into the ledger.

### NAVIGATE
5. **Axis decision:** Q1/Q2/Q3 from `taxonomy-navigation.md` — one answer each.
6. **Tier & lifecycle:** source tier (1–7) and active/archive/external placement. If tier ambiguous → CLARIFY gate.

---

## 2. STAGE 4 EVALUATE — Stranger-Audit Mechanics

Review the finished artifact as a stranger reviewing someone else's work. **Never audit in the same pass that wrote it** — re-read from the top after generation.

### Procedure
1. Re-read the artifact once, top to bottom, with no editing intent.
2. Run every criterion below; mark each PASS or FAIL with the evidence (quote the failing line).
3. For each FAIL, apply the fix recipe; do not rewrite anything that passed.
4. Re-check only the fixed items (targeted re-audit, not a full redo).
5. Iterate with STAGE 5 TEST — max 2 iterations total. Over the cap: emit with residual defects flagged in the Working Notes block.

### Countable criteria (all artifact types)
| # | Criterion | Countable check | Fix recipe |
|---|---|---|---|
| 1 | Output contract | Exactly one output block; nothing before it except `## Working Notes`; nothing after | Trim; move extras to Suggested Additions |
| 2 | Countable rules | 0 instructions requiring judgment — every rule has a number, threshold, or fixed recipe | Rewrite vague verbs: "be accurate" → "if not 100% certain, omit" |
| 3 | Neutral examples | 0 real brand/domain names in examples; 0 single-case hardcodes | Swap to a neutral fictional domain; generalize the intent |
| 4 | Source-grounding | Every claim traces to user input or a cited tier (1–7) | Drop or re-cite unverified claims (Tier 5 never becomes a premise) |
| 5 | Consistency | 0 contradictions between sections; 0 conflicts with `SKILL.md` (which wins) | Fix lower-precedence side; flag if ambiguous |
| 6 | Language | Output language matches user; internal terms stay English | Re-serialize the output block |
| 7 | Line budget | Skill ≤ 500 lines / 5000 tokens; depth in `references/` | Move depth to a new reference file |
| 8 | Trigger test (skills only) | description fires for 3 should-trigger queries, stays silent for 3 should-not queries | Rewrite description for near-miss negatives |

### Common failure modes (model shortcuts)
| Shortcut | Detection | Fix |
|---|---|---|
| Auditing in the same pass | No re-read happened; PASS marks without quotes | Force a fresh re-read before any PASS |
| Checking its own examples instead of the input | Artifact echoes example content | Contamination scan: type out the supporting sentence from the *input* for each claim |
| Passing judgment criteria | "Looks good" instead of a count | Require a number or evidence quote per criterion |
| Skipping the loop | No fix applied, no iteration count recorded | Record iteration count (1 or 2) in Working Notes |

---

## 3. STAGE 5 TEST — Acceptance & Generality

Run after EVALUATE fixes. All four must pass; each failure returns to EVALUATE with a specific fix.

1. **Acceptance:** re-check the 2–4 criteria written in STAGE 1 prelude. Count them: N/4.
2. **Neutrality & generality:** scan every example and example-derived phrase. 0 occurrences of user-supplied proper nouns or single-case terms. (This is the anti-contamination scan.)
3. **Trigger test (skills):** 3 should-trigger queries hit the description; 3 should-not queries miss it. (Optimization loop from `skill-guide.md`.)
4. **Consistency:** grep the artifact for contradictory terms (e.g., two field counts, two directory names, two platform claims). 0 hits.

---

## 4. Weak-Model-First Rules (detail)

These make the pipeline executable by an average model. Apply them while writing *any* artifact.

1. **One instruction = one countable action.** Split "Improve the description and make it trigger well" into "Rewrite description ≤ 1024 chars; must include [action verb] + [when-to-trigger]; test with 3 should-trigger queries."
2. **Every judgment becomes a number.** "Keep it short" → "≤ 3 sentences." "Don't over-explain" → "≤ 1 line of rationale per rule."
3. **Every failure mode gets a fix recipe.** Never say "fix it"; say "if opener count > 25%, reword fronts 2, 5, 9 with the starter 'Define X as...'".
4. **Every pass/fail has evidence.** A PASS without a quote or count is a failed audit item.
5. **State defaults explicitly.** When inferring platform/tier/language, write the inference + one-line reason into Working Notes so the user can correct it in one glance.
6. **Never rely on the model's confidence.** "I'm confident this is right" is not a test; a re-read with a count is.

---

## Anti-Examples

| ❌ Avoid | ✅ Prefer | Why |
|---|---|---|
| "Think carefully about the requirements" | "List KNOWN vs AMBIGUOUS; if AMBIGUOUS has items that change the artifact, ask at CLARIFY (max 3)" | Vague instruction is skippable; a split list is not |
| "Make sure the output is high quality" | "Run the 8-count criteria; each PASS needs evidence; iterate max 2" | Quality is unfalsifiable; counts are not |
| "Don't copy the example" | "Type out the supporting sentence from the input for each claim; if you cannot, drop it" | Negative rules are weak; a mechanical scan is strong |
| "Use good judgment when converting" | "Run the mapping table + loss audit + round-trip diff" | Judgment varies by model; a diff is deterministic |
