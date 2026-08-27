# Deep Flashcard Generator — Card Types & Generation Rules

Read this when generating cards. This holds the full per-type rules, the Source Test, the Anchor Test, and the Diversity Rule.

## Guiding Principle

> **One card = One unit of knowledge (Minimum Information Principle)**

The card count is determined by the document content, not a fixed quota.

## The 5 Card Types

### Type 1 — Definition
Cover every key term, concept, and acronym present. At least 1 card per term.

### Type 2 — Mechanism / Process (How/Why)
Cover every mechanism, algorithm, workflow, or causal relationship mentioned. 1 card per topic.

### Type 3 — Comparison / Distinction
Cover every pair of concepts that could be confused or that appear side by side. 1 card per pair.

### Type 4 — How / Why (Source-Grounded)
Generate cards asking **How** or **Why** about mechanisms, processes, design rationale, and causal relationships — **only when the answer is explicitly or clearly stated in the document**.

**Permitted angles:**
- **How it works**: "How does [mechanism X] operate?" — answer must be in the document.
- **Why it is designed this way**: "Why is [component/approach] designed as described?" — answer must be in the document.
- **What happens when**: "What happens when [process/condition] occurs?" — answer must be in the document.
- **Prerequisites / conditions**: "What must be true for [concept X] to work?" — answer must be in the document.

**NOT permitted:**
- ✗ Questions whose answers require you to infer or speculate beyond what is written
- ✗ "What if" scenarios not addressed in the document
- ✗ Topics or subtopics not mentioned anywhere in the document

**Source Test** — Before creating any Type 4 card, ask yourself:
> *"Is the answer to this question directly stated or clearly implied in the document?"*
- **YES** → Create the card (no special prefix)
- **NO** → Skip entirely

### Type 5 — Knowledge Connection
After completing Types 1–4, identify conceptual links between 2 or more concepts that **both appear in the document**.

**Valid connection angles:**
- Causal chains: "Concept A enables Concept B, which in turn makes Concept C possible"
- Dependency maps: "What does Concept X depend on, and what depends on it?"
- Synthesis: "How do components A, B, C work together to achieve outcome Y?"
- Contrast within document: "How do A and B differ in purpose, even though they both serve function X?"

**Classification:** All connection cards are treated equally — no prefix. Connections may be explicitly stated or reasonably inferred, as long as all referenced concepts exist in the document.

**Anchor Test**: All concepts referenced must exist in the document.

**Number of connection cards**: No fixed quota. Create as many as meaningfully possible.

## Diversity Rule (Critical)

Actively vary question phrasing across all cards. Do NOT repeat the same sentence structure for multiple cards. Explore different angles and framings:
- What it is, what it does, why it exists, how it works
- What happens when it fails / is misused
- How it compares to something else in the document
- When to use it vs. when not to
- Real-world analogies, consequences
- **Design rationale**: why was it designed this way?
- **Prerequisite thinking**: what must be true for this to work?
- **Inversion**: what would the system look like WITHOUT this component/concept?
- **Stakeholder perspective**: how does this concept look from the user's vs. system's vs. developer's viewpoint?
- **Degree/scale**: what happens if this is pushed to extremes?
- **Connection**: how do 2+ concepts in the document relate, depend on, or contrast with each other?

The goal is a deck that feels **rich and multi-dimensional**, not a list of `"What is X?"` cards.
