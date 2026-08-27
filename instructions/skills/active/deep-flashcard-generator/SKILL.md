---
name: deep-flashcard-generator
description: "Reads any attached document (PDF, DOCX, TXT, images, etc.), exhaustively extracts core concepts and generates high-quality Anki-ready flashcards using a strict source-only approach. Every card — definition, mechanism, comparison, How/Why, and knowledge connection — must be directly grounded in the provided document. Works with any subject. Trigger whenever the user attaches a document and wants study flashcards. Do NOT trigger when the user wants a summary, translation, quiz, or vocabulary lookup rather than flashcards — use doc-drill or vocab-lookup for those."
version: 1.1.0
tags:
  - flashcards
  - anki
  - study
  - knowledge-extraction
license: MIT
compatibility: "Any agent"
---

# Deep Flashcard Generator

> Turn any attached document into a high-quality, multi-dimensional Anki flashcard deck — exhaustively extracted from the source with strict fidelity. Every card is directly grounded in the provided document.

## When to Activate

Activate when the user attaches a document (PDF, DOCX, TXT, slides, images, notes) and wants to study it by generating Anki-ready flashcards. Works with a **minimal prompt**: `activate deep-flashcard-generator` + an attached document. Any parameter not explicitly stated by the user → apply the skill's defaults.

> **Do NOT trigger** when the user wants a summary, translation, a quiz, or a vocabulary lookup of specific words. Use `doc-drill` (document quiz), `document-vocab-extractor` (extract all vocabulary), or `vocab-lookup` (look up specific words) for those.

## Overview

This skill turns any attached document into a **multi-dimensional Anki flashcard deck**, exhaustively extracted from the source with strict fidelity. Cards span definitions, mechanisms, comparisons, How/Why reasoning, and knowledge connections — all grounded in the document. The pipeline enforces a **source-test / anchor-test** gate: if the answer is not clearly in the document, the card is omitted rather than invented.

## Language Policy

Follow the house language policy. **Priority order**: user's explicit request > document's dominant language. If the user does not specify a language, auto-detect the dominant language of the attached document and use it for all cards. The target language applies to **all content**, including how the question is phrased on the front. Internal processing follows these English instructions; output matches the user's/document's language. IT/technical terms always stay in English.

---

## Role

You are an expert **document analyst and instructional designer**. Your mission:

1. **Read and deeply understand** the entire attached document.
2. **Exhaustively extract** every concept, mechanism, process, comparison, and How/Why explanation — leave nothing important behind.
3. **Connect knowledge** by identifying relationships between 2 or more concepts that both appear in the document — causal chains, dependency maps, synthesis, contrasts. All connection cards are treated as regular cards with no special prefix.
4. **Guarantee absolute accuracy (100%)** — never speculate, never fabricate information not in the source. If you are not 100% certain about a fact, **omit the card entirely**. You may use universally known, well-established facts to support an answer only when the core concept is clearly stated in the document.

---

## Step 1: Document Analysis

Before creating any cards, silently scan the entire document and identify (internal list, do not output):
- **Concepts / Terms**: All definitions, key terms, and acronyms present.
- **Mechanisms / Processes**: How systems, algorithms, or workflows operate.
- **Comparisons / Distinctions**: Pairs of concepts that are commonly confused or placed side by side.
- **Real-world Applications**: Specific use cases or examples mentioned.
- **Relationships**: Dependencies, hierarchies, or causal chains between concepts in the document.

---

## Step 2: Card Generation Strategy (Exhaustive Extraction)

There is **no fixed card count**; the number of cards is determined by the document content and the guiding principle:

> **One card = One unit of knowledge (Minimum Information Principle)**

Generate cards across 5 types: definition, mechanism/process, comparison/distinction, How/Why (source-grounded), and knowledge connection. For the full per-type rules, permitted angles, the **Source Test**, the **Anchor Test**, and the **Diversity Rule**, read `references/card-types.md`.

---

## Step 3: Card Writing Rules (Mandatory)

### Front
- Short, clear, unambiguous. Phrased to provoke active recall.
- Can be a direct question, a fill-in-the-blank statement, or a scenario prompt — as long as it is unambiguous and tests a single concept.
- **Avoid**: Yes/No questions, questions answerable by elimination or pattern-matching.

### Back
- Short to medium length: **max 2–3 sentences** or a compact list (≤ 4 bullets).
- Direct, accurate, easy to recall.
- If an explanation exceeds 3 sentences → **split into multiple cards** instead of cramming into one.
- No filler openers like "This is...", "The answer is...".

### Accuracy
- Never speculate or fabricate information.
- If uncertain about any content → skip the card entirely.
- All cards must be grounded in the document. You may use universally known, well-established facts only to support an answer whose core concept is clearly in the document — never to introduce new topics.

---

## Step 4: Card Type

Generate **Basic cards only** (front / back).  
**Do NOT** use Cloze deletion format (`{{c1::...}}`).

---

## Step 5: Language (Strictly Enforced)

**Priority order**: User's explicit request > Document's dominant language. If the user does not specify a language, auto-detect the dominant language of the attached document and use it for all cards. The target language applies to **all content**, including the front phrasing — but IT/technical terms stay in English. See full rules + correct/incorrect examples in `references/language-and-output.md`.

## Step 6: Output Format (Strictly Enforced)

Produce **2 columns, tab-separated (TSV)**, `front[TAB]back`, one card per line, no header row, no tabs inside card content, wrapped in a single `text` markdown block, and nothing outside it. See full rules + the canonical template in `references/language-and-output.md`.

## Output Contract

## [What to emit, and ONLY what to emit]
Emit a **single `text` fenced block** containing the TSV cards. No preamble, no postamble, no explanations, and nothing outside the block. See `references/language-and-output.md`.

## Anti-Examples

| ❌ Avoid | ✅ Prefer | Why |
|---|---|---|
| "What is Hệ điều hành?" (Front English, Back Vietnamese) | "Hệ điều hành đóng vai trò gì trong hệ thống máy tính?" (full Vietnamese) | The target language must apply to the front too. |
| Blending languages inside a single card | Writing the whole card in one target language, keeping only technical terms in English | Prevents confusing language-split cards. |
| Speculating when the answer isn't in the document | Omitting the card entirely | Accuracy/fidelity is the hard guarantee — never fabricate. |
| Adding prose or a summary before/after the TSV block | Emitting only the single `text` block | Output must be machine-parseable. |

## References
- `references/card-types.md` — read when generating card types and applying the Source Test / Anchor Test / Diversity Rule.
- `references/language-and-output.md` — read for language rules and the TSV output format.
- `../skill-forge/references/house-language-policy.md` — read when choosing the response language.

## Example Output

### English output (Topic: Networking)

```text
What is TCP?	Transmission Control Protocol — a connection-oriented transport protocol that guarantees ordered, error-checked delivery of data packets.
TCP vs UDP — which guarantees delivery and which prioritizes speed?	TCP guarantees delivery (connection-oriented, slower); UDP prioritizes speed (connectionless, no guarantee). Use TCP for web/email; UDP for video/gaming.
What happens during a TCP 3-way handshake?	SYN → SYN-ACK → ACK. Both parties synchronize sequence numbers before any data is sent.
How do the Transport layer and Application layer depend on each other?	The Application layer relies on the Transport layer to deliver its data reliably or quickly. Without a functioning transport protocol, application-level communication cannot occur.
Why does TCP use a 3-way handshake before sending data?	To synchronize sequence numbers between both parties and confirm both sides are ready — ensuring a reliable, ordered communication channel is established before any data is transmitted.
```

### Vietnamese output (Chủ đề: Hệ thống máy tính)

```text
Hệ điều hành đóng vai trò gì trong hệ thống máy tính?	HDH là phần mềm trung gian giữa phần cứng và người dùng/ứng dụng, quản lý tài nguyên và cung cấp môi trường chạy cho chương trình.
Điều gì phân biệt phần mềm hệ thống với phần mềm ứng dụng?	Phần mềm hệ thống quản lý và điều phối phần cứng (VD: HDH, driver, tiện ích). Phần mềm ứng dụng phục vụ nhu cầu cụ thể của người dùng (VD: trình soạn thảo, trình duyệt).
Tại sao HDH được coi là "lớp trừu tượng" giữa phần cứng và ứng dụng?	HDH che giấu độ phức tạp của phần cứng, cung cấp API thống nhất để ứng dụng giao tiếp mà không cần biết chi tiết phần cứng bên dưới.
Phần mềm hệ thống và phần cứng phối hợp với nhau như thế nào trong mô hình lớp?	Driver (phần mềm hệ thống) trừu tượng hóa phần cứng; HDH cung cấp môi trường thực thi cho ứng dụng. Ba lớp phụ thuộc vào nhau theo thứ bậc từ phần cứng lên ứng dụng.
Driver và HDH phụ thuộc lẫn nhau như thế nào?	Driver cần HDH để có môi trường chạy; HDH cần driver để điều khiển phần cứng cụ thể. Cả hai phụ thuộc lẫn nhau để hệ thống vận hành.
Hạn chế của kiến trúc phân lớp (layered architecture) trong hệ thống máy tính là gì?	Mỗi lớp thêm chi phí trừu tượng hóa (overhead). Trong các hệ thống yêu cầu hiệu năng cực cao, việc đi qua nhiều lớp có thể gây trễ.
```
