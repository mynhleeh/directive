# Deep Explainer — Output Template

This is the canonical output structure emitted by the Deep Explainer skill. Read this when you need to produce an explanation. Adapt the section headings into the user's detected language while keeping the structure identical.

```markdown
## 🎯 [Core Concept Title]
[A simple, 1-2 sentence definition without heavy jargon.]

## ⚙️ How it Works & Use Cases
[Detailed breakdown of the mechanism and its practical applications. Use bullet points or numbered lists where appropriate.]

## 💡 Real-World Analogy
[A relatable, everyday analogy to make the abstract concept concrete.]

## 🔗 Knowledge Connection
[Briefly introduce 2-3 related concepts/technologies. Compare/contrast them with the main topic to expand the user's understanding.]
```

## Rules
- Emit ONLY this single block. Do not add a preamble, postamble, or extra sections.
- Emoji headings are optional and used for scannability; keep them only if they read naturally in the target language.
- If the user's language differs from English, translate the headings (and content) but keep the section order and the technical terms in English.
- End the response with a single check-for-understanding question (see step 7 in `SKILL.md`), then stop.
