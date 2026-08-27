# Deep Flashcard Generator — Language & Output Format

Read this when choosing the target language and formatting the TSV output.

## Language Rules (Strictly Enforced)

**Priority order**: User's explicit request > Document's dominant language.

If the user does not specify a language, auto-detect the dominant language of the attached document and use it for all cards.

> **The target language applies to ALL content — including how the question is phrased on the Front, not just the answer on the Back.**

This is a hard rule. If the target language is Vietnamese, the question itself must be written in Vietnamese. If the target language is English, the question must be in English.

**The only exception**: IT / technical terms (protocol names, algorithm names, tool names, data structures, design patterns, programming constructs) always stay in English regardless of the output language.

### Anti-examples (do not do this)

```
❌ WRONG — language split (Front English, Back Vietnamese):
Front: "What is Hệ điều hành?"
Back:  "HDH là phần mềm trung gian giữa phần cứng và người dùng."

❌ WRONG — language split (Front English, Back Vietnamese):
Front: "What is the difference between phần mềm hệ thống and phần mềm ứng dụng?"
Back:  "Phần mềm hệ thống quản lý phần cứng..."
```

```
✅ CORRECT — full Vietnamese:
Front: "Hệ điều hành đóng vai trò gì trong hệ thống máy tính?"
Back:  "HDH là phần mềm trung gian giữa phần cứng và người dùng/ứng dụng, giúp quản lý tài nguyên và cung cấp môi trường chạy cho các chương trình."

✅ CORRECT — full English:
Front: "What role does an Operating System play in a computer system?"
Back:  "The OS acts as an intermediary between hardware and user/application programs, managing resources and providing a runtime environment."
```

## Output Format (Strictly Enforced)

1. **2 columns, Tab-Separated (TSV)**: `front[TAB]back`
2. **One line = one card.** No line breaks inside card content.
3. **No header row** (do not write `front\tback` at the top).
4. **No tab characters inside card content**: use `;` or `|` as inline separators when listing items.
5. Wrap the entire output in a **single markdown text block**:

````
```text
[front of card 1]	[back of card 1]
[front of card 2]	[back of card 2]
[front of card 3]	[back of card 3]
```
````

6. **No conversational text, explanations, or any content outside the `text` block.**

## Card Type Notes

Generate **Basic cards only** (front / back). Do **NOT** use Cloze deletion format (`{{c1::...}}`).
