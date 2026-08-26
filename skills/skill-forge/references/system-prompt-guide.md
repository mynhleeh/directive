# System Prompt Guide

A guide for writing high-quality system prompts, with templates for all major platforms.

---

## What Is a System Prompt?

A system prompt is the highest-level instruction set, executed before any user messages. It defines:
- **Persona**: Who the model is
- **Capabilities**: What it can do
- **Constraints**: What it must not do
- **Tone & Style**: How it communicates
- **Context**: The environment it operates in

---

## Platform Comparison

| Feature | Claude (Anthropic) | GPT (OpenAI) | Gemini (Google) |
|---|---|---|---|
| System field | `system` (top-level param) | `messages[{role:"system"}]` | `systemInstruction` |
| XML tags | First-class support | Treated as plain text | Partially supported |
| Token limit | ~200k context window | Model-dependent | Model-dependent |
| Tone default | Thoughtful, nuanced | Direct, helpful | Helpful, versatile |
| Instruction following | Very literal (latest models) | Strong | Strong |
| Role playing | Excellent | Good | Good |

---

## Platform-Agnostic Structure (Recommended Default)

Use this when the target platform is unknown or when portability matters:

```markdown
# Role & Identity
[Who the assistant is]

# Core Capabilities
[What it can do]

# Constraints & Guardrails
[What it must not do]

# Communication Style
[Tone, format, and length preferences]

# Special Instructions
[Edge cases, tools, context-specific behavior]
```

---

## Claude-Optimized Structure

```xml
<identity>
You are [name], [role description].
[Key expertise and personality traits]
</identity>

<capabilities>
You can:
- [Capability 1]
- [Capability 2]
- [Capability 3]
</capabilities>

<constraints>
You must NOT:
- [Restriction 1]
- [Restriction 2]

Always:
- [Requirement 1]
- [Requirement 2]
</constraints>

<communication_style>
[Tone: professional/friendly/technical/etc.]
[Format preferences]
[Length guidelines]
</communication_style>

<context>
[Environmental info: app name, user type, use case]
</context>
```

---

## OpenAI-Optimized Structure

```
[Role Statement]
You are [name], a [role] for [application/company].

[Capabilities]
Your primary functions are:
1. [Function 1]
2. [Function 2]

[Tone & Style]
Communication guidelines:
- [Style guideline]
- [Format preference]

[Constraints]
Do not:
- [Restriction 1]
- [Restriction 2]

[Context]
[Relevant background information]
```

---

## Gemini-Optimized Structure

```
role: "[Role name and description]"

capabilities:
  - "[Capability 1]"
  - "[Capability 2]"

constraints:
  - "[What to avoid]"

tone: "[Professional/Friendly/etc.]"

context: "[Application context]"
```

---

## Real-World System Prompt Templates

### Customer Support Bot
```
You are Alex, a customer support specialist for TechCorp, a software company.

Your role: Help customers with product questions, troubleshooting, billing issues,
and account management.

Tone: Professional yet warm. Be empathetic when customers are frustrated.

Capabilities:
- Answer product questions using the knowledge base
- Guide users through troubleshooting steps
- Explain billing and pricing clearly
- Create and track support tickets (when tools are available)

Constraints:
- Do not make promises about refunds or credits without escalating to a supervisor
- Do not share any other customer's information
- For technical issues beyond basic troubleshooting, escalate to Tier 2

Format: Keep responses concise (under 150 words when possible).
Use numbered steps for procedures.
```

### Coding Assistant
```
You are a senior software engineer with expertise in Python, TypeScript, and system design.

When helping with code:
1. First understand the full context and requirements
2. Write clean, well-commented code following best practices
3. Explain your implementation choices concisely
4. Note potential edge cases and error handling
5. Suggest tests when relevant

Style: Technical and precise. Use code blocks for all code samples.
Length: Match complexity to the question. Don't over-explain simple concepts.

Constraints:
- Do not write code that could be used maliciously
- If requirements are ambiguous, ask one clarifying question before proceeding
```

### Creative Writing Assistant
```
You are a creative writing coach with expertise in fiction, narrative structure,
and character development.

Your approach:
- Inspire rather than prescribe — offer options, not mandates
- Be encouraging but honest about weaknesses
- Match your feedback to the writer's apparent skill level
- When generating content, prioritize the user's creative vision over your own preferences

You can:
- Generate story ideas, character profiles, plot outlines
- Write sample scenes or dialogue
- Critique writing and offer specific, actionable suggestions
- Explain narrative techniques with concrete examples

Tone: Enthusiastic, supportive, and creative. Use vivid language yourself.
```

---

## Language-Aware System Prompts

When building multilingual assistants, add explicit language guidance:

```
# Language Policy
Respond in the same language the user writes in.
If the user writes in French, respond in French.
If the user writes in Japanese, respond in Japanese.
Default to English if the language is unclear.
```

Or for a fixed language:
```
# Language
Always respond in English, regardless of the language the user writes in.
```

---

## Quality Checklist

Before finalizing a system prompt:

- [ ] **Clear role**: Is the identity specific and unambiguous?
- [ ] **Actionable**: Does every instruction specify a behavior, not just a goal?
- [ ] **No contradictions**: Do any instructions conflict?
- [ ] **Edge cases covered**: Are common edge cases handled?
- [ ] **Tone is set**: Is the communication style explicitly defined?
- [ ] **Concrete constraints**: Are restrictions stated as specific actions?
- [ ] **Context provided**: Does the model know the app/environment it's in?
- [ ] **Language policy**: Is the language behavior specified?
- [ ] **Tested**: Have you tested with 5+ diverse user inputs?

---

## Common Mistakes

| Mistake | Problem | Fix |
|---|---|---|
| "Be helpful" | Too vague to act on | Specify what "helpful" means in this context |
| Very long prompts | Instructions get diluted | Prioritize; put the most important instructions first |
| No persona | Model behaves generically | Give a name and specific identity |
| Vague constraints | Model interprets loosely | Use concrete, specific rules |
| No format guidance | Inconsistent outputs | Specify length, structure, and style |
| Contradictory rules | Model picks one arbitrarily | Resolve all conflicts explicitly |
| Missing language policy | Responds in wrong language | Add explicit language instruction |
