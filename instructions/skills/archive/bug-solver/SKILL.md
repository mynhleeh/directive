---
name: bug-solver
description: "Analyzes root causes of bugs, provides clear explanations with edge cases, searches the web for solutions, and directly states if unable to fix. Trigger whenever the user asks to analyze, explain, or fix a bug/error, or provides a stack trace or error message. Do NOT trigger for general 'explain a concept' questions — use deep-explainer."
version: 1.1.0
tags: [bug, debug, fix, troubleshooting, analysis]
license: MIT
compatibility: "Any agent"
---

# Bug Solver

## When to Activate
Activate this skill when the user asks to analyze, explain, or fix a bug/error in their code, or when providing stack traces and error messages.

## Overview
This skill forces the agent to rigorously analyze the root cause of a bug, explain the reasoning clearly (including potential edge cases), and proactively use web search tools to find solutions on any platform. It strictly enforces a direct, no-fluff communication style in the user's preferred language, and mandates honesty when a fix is unknown.

## Instructions
1. **Root Cause Analysis**: Immediately analyze the provided code or error message to identify the fundamental root cause, rather than just treating symptoms.
2. **Diagnose Before Prescribing**: Classify the cause first — is it a runtime error, a logic bug, a config/type issue, or an environment discrepancy? Choose the repair based on the classification, not on a guess.
3. **Clear Explanation & Edge Cases**: Explain exactly *why* the bug occurs. List any edge cases or alternative scenarios that might also be causing or contributing to the issue.
4. **Web Search**: Proactively use any available search tool (e.g., web-fetch, GitHub search, or an environment-specific search function) to look up the error message, bug pattern, or library-specific issues on relevant platforms (StackOverflow, GitHub Issues, official docs). **Fallback**: if no web-search tool is available in the current environment, state your assumption ("no search tool available; resolving from existing knowledge") and clearly flag the limits of the answer.
5. **Honesty (Direct Fallback)**: If you cannot find a solution or do not know how to fix the bug after searching, you MUST state directly "I don't know" or "I cannot fix this based on current information." Do not guess or hallucinate fixes.
6. **Verify the Fix**: After proposing a solution, confirm it addresses the root cause (not just the symptom) and mention how to verify it resolves — e.g., a test to run, an expected output, or a regression check.

## Output Contract

## [What to emit, and ONLY what to emit]
Emit a **single response** in the user's language (this skill's instructions are English, but the output must adapt to the user's language). Use this structure, with no preamble or postamble:
- **Root Cause** — concise explanation of the bug.
- **Possible Causes / Edge Cases** — bullet points of potential triggers.
- **Search Context** — a brief note of what was found via web search (or state the fallback assumption).
- **Fix / Solution** — the code or steps to fix it (or a direct admission of inability to fix).

## References
- `../skill-forge/references/house-language-policy.md` — read when choosing the response language.
- `../skill-forge/references/prompt-patterns.md` — read for grounding/no-hallucination patterns.

## Anti-Examples
| ❌ Avoid | ✅ Prefer | Why |
|---|---|---|
| "Hello! I would be happy to help you fix this bug..." | "The root cause is a null pointer exception in `app.js` line 42." | No fluff. Be direct. |
| Guessing a fix without checking documentation or searching. | Verifying the error code against docs/a search result before providing a solution. | Prevents hallucinations. |
| Giving a generic explanation like "There is a syntax error." | "The variable `x` is undefined because the async call hasn't resolved yet. Edge cases: network timeout, empty response." | Detail and edge cases matter. |
| Making up a fix when unsure. | "I searched the web but couldn't find a definitive fix for this specific version. I do not know how to resolve this." | Honesty is strictly required. |
