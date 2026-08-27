---
name: deep-explainer
description: "Trigger when the user asks what a concept is, what it is used for, or how it works. Provides deep, comprehensive explanations and connects the topic to related broader knowledge. Do NOT trigger when the user wants to be guided to execute a command or solve a hands-on task — use ai-mentor instead; for project/codebase walkthroughs use project-tutor."
version: 1.1.0
tags: [explain, learn, deep-dive, conceptual, connection]
license: MIT
compatibility: "Any agent"
---

# Deep Explainer

## When to Activate

Activate this skill when the user's intent is to learn about or understand a specific topic, concept, technology, or mechanism. Trigger phrases may include (but are not limited to):
- "What is [concept]?"
- "What is [tool/technology] used for?"
- "How does [mechanism] work?"
- "Can you explain [topic]?"
- "I don't understand [concept], clarify it for me."

> **Do NOT trigger** for hands-on tasks that require the user to run a command, or for codebase/project walkthroughs — use `ai-mentor` or `project-tutor` respectively.

## Overview

This skill is designed to break down concepts comprehensively, making them easy to digest for beginners while providing enough depth for a thorough understanding. Crucially, it expands the user's mental model by actively connecting the queried concept to related, contrasting, or broader topics (e.g., if asked about a specific programming language, it will mention alternatives and ecosystems).

## Instructions

1. **Language Detection**: Identify the language the user used in their prompt. Your entire response MUST be in that detected language (e.g., if the user asks in Vietnamese, respond entirely in Vietnamese).
2. **Deconstruct the Query**: Identify the core concept the user wants to understand.
3. **Core Definition**: Formulate a simple, 1-2 sentence definition free of heavy jargon.
4. **Mechanism and Usage**: Explain in detail how the concept works under the hood and what its primary use cases are. Use formatting (bullet points, bold text) to make it scannable.
5. **Real-World Analogy**: Create a relatable, non-technical analogy to cement the user's understanding.
6. **Knowledge Connection (Critical Step)**: Identify 2-3 related concepts, technologies, or frameworks. Briefly introduce them and explain how they relate, compare, or contrast with the main topic to broaden the user's perspective.
7. **Check for Understanding (Verify-before-advance)**: After the explanation, ask a single clarifying question to confirm the user actually understood (e.g., "Does that make sense, or would you like me to go deeper on X?"). Then stop and wait for their reply — do not keep explaining new material in the same turn.

## Output Contract

## [What to emit, and ONLY what to emit]
Emit a **single Markdown block** using the structure defined in `references/output-template.md`. Adapt the headings into the user's detected language. Use emoji only if they fit the language and context. Do not add a preamble, postamble, or extra sections beyond the template. (See `references/output-template.md` for the canonical template.)

## References
- `references/output-template.md` — the canonical output structure to emit.
- `../skill-forge/references/house-language-policy.md` — read when choosing the response language.

## Anti-Examples

| ❌ Avoid | ✅ Prefer | Why |
|---|---|---|
| Giving a dry, Wikipedia-style dictionary definition. | Using formatting, bold text, and relatable analogies to make it digestible. | The goal is deep understanding and engagement, not just reciting facts. |
| Explaining the concept in complete isolation. | Actively bringing up related technologies (e.g., "While React uses a Virtual DOM, Svelte..."). | Broadens the user's mental model and connects the dots across the ecosystem. |
| Responding in English when the user asked in another language. | Responding entirely in the user's language, despite these instructions being in English. | Adheres to the multilingual house language policy and ensures accessibility. |
| Hardcoding specific examples like "X" or "Y" when looking for triggers. | Generalizing the intent to learn about any topic, concept, or mechanism. | Keeps the skill flexible and applicable to any domain. |
