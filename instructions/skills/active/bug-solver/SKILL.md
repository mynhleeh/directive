---
name: bug-solver
description: "Analyzes root causes of bugs, provides clear explanations with edge cases, searches the web for solutions, and directly states if unable to fix."
version: 1.0.0
tags: [bug, debug, fix, troubleshooting, analysis]
license: MIT
compatibility: [any-agent]
---

# Bug Solver

## When to Activate
Activate this skill when the user asks to analyze, explain, or fix a bug/error in their code, or when providing stack traces and error messages.

## Overview
This skill forces the agent to rigorously analyze the root cause of a bug, explain the reasoning clearly (including potential edge cases), and proactively use web search tools to find solutions on any platform. It strictly enforces a direct, no-fluff communication style in the user's preferred language, and mandates honesty when a fix is unknown.

## Instructions
1. **Root Cause Analysis**: Immediately analyze the provided code or error message to identify the fundamental root cause, rather than just treating symptoms.
2. **Clear Explanation & Edge Cases**: Explain exactly *why* the bug occurs. List any edge cases or alternative scenarios that might also be causing or contributing to the issue.
3. **Web Search**: You MUST proactively use your search tools (e.g., `search_web`) to look up the error message, bug pattern, or library-specific issues on any relevant platforms (e.g., StackOverflow, GitHub Issues, official documentation).
4. **Honesty (Direct Fallback)**: If you cannot find a solution or do not know how to fix the bug after searching, you MUST state directly "I don't know" or "I cannot fix this based on current information." Do not guess or hallucinate fixes.
5. **Directness**: Keep the response extremely direct. No fluff, no long-winded pleasantries. Get straight to the analysis and the fix.

## Output Contract
- **Language**: Translate all your output into the user's language (e.g., Vietnamese if the user speaks Vietnamese). This skill's internal instructions are in English, but the output must adapt.
- **Structure**:
  - **Root Cause**: Concise explanation of the bug.
  - **Possible Causes / Edge Cases**: Bullet points of potential triggers.
  - **Search Context**: A brief mention of what was found via web search (if applicable).
  - **Fix / Solution**: The code or steps to fix it (or a direct admission of inability to fix).

## Anti-Examples
| ❌ Avoid | ✅ Prefer | Why |
|---|---|---|
| "Hello! I would be happy to help you fix this bug..." | "The root cause is a null pointer exception in `app.js` line 42." | No fluff. Be direct. |
| Guessing a fix without checking documentation or searching. | Using `search_web` to verify the error code before providing a solution. | Prevents hallucinations. |
| Giving a generic explanation like "There is a syntax error." | "The variable `x` is undefined because the async call hasn't resolved yet. Edge cases: network timeout, empty response." | Detail and edge cases matter. |
| Making up a fix when unsure. | "I searched the web but couldn't find a definitive fix for this specific version. I do not know how to resolve this." | Honesty is strictly required. |
