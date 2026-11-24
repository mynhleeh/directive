---
trigger: glob
globs: "**/*.md, **/*.qmd, **/*.markdown"
description: "Markdown layout, content density, presentation form selection, physical formatting hygiene (whitespace, compact tables, zero thematic breaks, zero HTML entities), and mandatory awk/rg verification checks."
---

# Markdown Formatting & Layout Standards

Governs presentation form, structural density, physical Markdown hygiene, and automated verification for every Markdown file created or edited. Complements `technical-writing-principles.rule.md` without overriding semantic prose rules.

## 1. Scope, Precedence & Formatting Invariance

1. Applies to every `.md`, `.qmd`, and `.markdown` file created or edited in the workspace, including rules and skills.
2. **Untouched Legacy Files:** Existing files not edited by the current task are never rewritten solely for formatting. Any file modified by the current unit MUST pass all Section 5 checks before completion.
3. **Formatting-Only Edit Invariance:** When performing a formatting-only cleanup, text with all whitespace removed MUST remain identical to the original (`ORIG`), allowing only: deleted thematic-break lines, converted HTML entities or arrows, normalized table delimiter rows, and setext headings converted to `#`.
4. Where formatting conflicts arise on physical Markdown form, this rule supersedes stylistic prose rules (including `&#124;` entity guidance in `technical-writing-principles.rule.md`) per `core-collaboration-charter.rule.md`.

## 2. Presentation Form & Content Density

1. **Select Form by Content Shape (Never Default to One Form):**

| Content Shape | Required Presentation Form |
| --- | --- |
| 2 or more repeating attributes shared across items | Table |
| Mandatory chronological or execution step sequence | Numbered list (`1.`, `2.`, `3.`) |
| Unordered peer items, each 1 line or shorter | Bullet list (`-`) |
| Independent idea without repeating sibling structure | Short paragraph on its own line |
| Uniform attributes plus 1 extended explanation per item | Compact table followed by a short paragraph below |

   Prohibit tables for sequential narratives or single-data-column lists (use a list instead).
2. **Table Density Limit:** Place at most **2** consecutive tables inside a single `H2` or `H3` section without an intervening paragraph, list, or sub-heading. Exception: repeating specification units that each declare their own sub-heading.
3. **Zero Prose-Table Redundancy:** Paragraphs immediately before or after a complete table or diagram MUST only add new information or brief cross-references, never restate rows already listed in full. Exception: repeating fixed lookup templates per entity unit.
4. **Paragraph Line Cap:** Split, tabulate, or list any prose paragraph exceeding **8** consecutive lines.
5. **Traceability Identifier Preservation:** Never truncate, abbreviate, or paraphrase strings carrying requirement, use-case, rule, or error IDs, even when repetitive.

## 3. Whitespace, Dashes & Table Syntax

### 3.1. Whitespace Rules

1. Zero trailing spaces or tabs on any line.
2. Zero runs of **2** or more consecutive blank lines; separate adjacent blocks with exactly **1** blank line.
3. Start content on line 1 and end the file with exactly **1** newline character (no blank trailing line).
4. Zero tab characters outside code fences. Indent nested list items to the text column of the parent marker (`2` spaces under `-`, `3` spaces under `1.`).
5. Maximum **1** space between words and after punctuation outside code fences and table syntax.
6. Maintain consistent line endings within each file (never mix CRLF and LF).

### 3.2. Dashes & Thematic Breaks

1. Zero thematic breaks (`---`, `***`, `___`, or spaced variants) anywhere in document body text; separate sections with headings alone.
2. Permit `---` lines exclusively for the 2 YAML frontmatter delimiters and table header delimiter rows.
3. Zero decorative runs of `=`, `-`, `*`, or `_` on their own line, and zero setext underlines (`===`); always use ATX `#` headings.
4. Never end a document with a dash line.

### 3.3. Compact Table Integrity

1. **Compact Unpadded Cells:** Format cells with **1** space around pipes (`| value | value |`); never pad columns to visually align pipes.
2. **Delimiter Row:** Use exactly **3** hyphens per column (`| --- | --- |`), adding colons only when column alignment is explicitly required (`| :--- | ---: |`).
3. **Empty Cells:** Represent empty cells with two spaces between pipes (`|  |`, holding one space of empty content), never em-dashes.
4. **Spacing & Enclosure:** Surround every table with **1** blank line before and after, zero blank lines inside, and start/end every row with `|`.
5. **Column Count Parity & Pipe Escaping:** Header, delimiter, and every data row MUST share the exact same column count. Escape literal pipes inside table math or inline snippets as `\|` (never `&#124;`).

## 4. Headings, Lists, Emphasis, Fences & Characters

1. **Headings:** Use `#` + **1** space + title (no closing `#`), surrounded by **1** blank line before and after. Descend levels by **1** step at a time (`H2 -> H3`, never `H2 -> H4`).
2. **Lists:** Use `-` exclusively for unordered lists and sequential `1.`, `2.`, `3.` for ordered lists, with **1** space after the marker and zero blank lines between items of the same list.
3. **Emphasis:** Write `**bold**` and `*italic*` with zero spaces inside markers; prohibit empty `****`.
4. **Code Fences:** Use 3 backticks (never `~~~`) with an explicit language tag (`text` if generic) and **1** blank line before and after.
5. **Clean Characters:** Write raw `&`, `<`, `>`, and ASCII arrows `->` in prose and tables; prohibit HTML entities (`&amp;`, `&lt;`, `&gt;`, numeric entities) and Unicode arrows (`→`, `⇒`) outside code spans/fences. Prohibit non-breaking spaces (`U+00A0`), zero-width spaces (`U+200B`), and UTF-8 BOM.

## 5. Mandatory Deterministic Verification (`awk` & `rg`)

Run the preprocessor and checks below in a POSIX shell (such as bash or Git Bash on Windows) on every created or edited Markdown file (`FILE`). Every check MUST yield **0** matches (empty output or `0` on `-c` counts), except line-ending uniformity (violation only if both CRLF and LF counts exceed `0`) and `diff -w -B ORIG FILE` (applicable only to formatting-only edits).

```text
awk 'NR==1&&/^---$/{fm=1;next} fm&&/^---$/{fm=0;next} fm{next} match($0,/^ *(\x60\x60\x60+|~~~+)/){m=substr($0,RSTART,RLENGTH);gsub(/ /,"",m);if(!f){f=1;o=m;print "@@FENCE@@"}else if(substr(m,1,1)==substr(o,1,1)&&length(m)>=length(o)&&$0~/^ *[\x60~]+ *$/){f=0};next} f{next} {gsub(/`[^`]*`/,"X");print} END{if(f)print "@@UNCLOSED@@"}' FILE > STRIPPED

# Whitespace and line boundaries
rg -n ' +$|\t+$' STRIPPED
rg -U -n '\n\n\n' STRIPPED
rg --pcre2 -U -n '\n\n\z' FILE
rg --pcre2 -U -c '[^\n]\z' FILE
rg --pcre2 -U -c '\A\s*\n' FILE
rg -n '\t' STRIPPED
rg -n '^[^|]*[^| ] {2,}[^ ]' STRIPPED
rg -c '\r$' FILE
rg -c -v '\r$' FILE

# Thematic breaks and setext headings
rg --pcre2 -n '^\s*([-*_])(\s*\1){2,}\s*$' STRIPPED
rg -n '^=+\s*$' STRIPPED

# Compact tables
rg -n '[^| ] {2,}\|' STRIPPED
rg -n '\| {2,}[^| ]' STRIPPED
rg --pcre2 -n '(?<!\x5c)\|[^| ]|[^| \x5c]\|' STRIPPED
rg -n '\|\s*:?-{4,}:?\s*(\||$)' STRIPPED
rg -n '\|\s*:?-{1,2}:?\s*(\||$)' STRIPPED
rg -n '^\|[:-]' STRIPPED
rg -n '\| {3,}\||\|\||\| \|' STRIPPED
rg --pcre2 -U -n '^[^|\n][^\n]*\n\|' STRIPPED
rg --pcre2 -U -n '^\|[^\n]*\n[^|\n]' STRIPPED
rg --pcre2 -U -n '^\|[^\n]*\n\n\|' STRIPPED
rg -n '^\|.*[^|\s]\s*$' STRIPPED

# Headings, lists, emphasis, fences, entities, invisible characters
rg -n '^#{1,6}[^# ]' STRIPPED
rg -n '^#{1,6} .*\s#+\s*$' STRIPPED
rg --pcre2 -U -n '[^\n]\n#{1,6} ' STRIPPED
rg --pcre2 -U -n '^#{1,6} [^\n]*\n[^\n]' STRIPPED
rg -n '^\s*[*+] ' STRIPPED
rg -n '^\s*(-|\d+\.)  +\S' STRIPPED
rg --pcre2 -U -c '^\s*- [^\n]*\n\n\s*- ' STRIPPED
rg --pcre2 -U -c '^\d+\. [^\n]*\n\n\d+\. ' STRIPPED
rg -n '(^|\s)\*\*(\s|$)|\*\*\*\*' STRIPPED
rg --pcre2 -U -n '[^\n]\n@@FENCE@@' STRIPPED
rg --pcre2 -U -n '@@FENCE@@\n[^\n]' STRIPPED
rg -n '@@UNCLOSED@@' STRIPPED
rg -n '&(#\d+|#x[0-9a-fA-F]+|[A-Za-z]+);' STRIPPED
rg -n '→|⇒' STRIPPED
rg -n '\x{00A0}|\x{200B}' FILE
grep -c $'\xef\xbb\xbf' FILE
```

Count these 3 properties directly by inspection (target = **0** defects): consecutive heading level jumps greater than `1`, out-of-sequence ordered lists (`1., 2., 3.`), and opening code fences lacking a language tag.
