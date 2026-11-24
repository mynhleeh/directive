# Lua Filter Transformations and Table Layout

`scripts/report-prep.lua` normalizes Markdown AST elements before Pandoc emits LaTeX so source Markdown stays clean, readable on GitHub, and free of raw TeX hacks.

## Metadata Configuration Keys (`prep`)

Configure filter behavior under YAML frontmatter `prep:` or JSON `--metadata-file`:

| Option | Type | Default | Behavior |
| --- | --- | --- | --- |
| `prep.strip-cover` | string | `"none"` | `"none"`, `"before-first-h1"`, or `"first-h1-cover"` |
| `prep.strip-heading-numbers` | bool | `true` | Removes manual prefixes (`1.`, `1.1`, `A.1`, `Appendix A:`, `Phụ lục B:`) |
| `prep.code-listings` | bool | `true` | Renders code fences using `listings` `\begin{lstlisting}` |
| `prep.code-verbatim` | bool | `false` | Drops `[language=...]` on `listings`, or uses `fvextra` `Verbatim` when `code-listings: false` |
| `prep.prefer-vector-pdf` | bool | `true` | Swaps `.png`/`.jpg`/`.webp` images to sibling `.pdf` if present on disk |
| `prep.callout-boxes` | bool | `true` | Converts GFM `> [!NOTE]` alerts into `\begin{reportcallout}` `tcolorbox` blocks |
| `prep.adaptive-tables` | bool | `true` | Sets proportional `\real{...}` widths and wraps 2–4 col (`\footnotesize`) or 5+ col (`\scriptsize`) |
| `landscape-figures` | list | `[]` | Image filenames or paths to render via `\landscapefigure{src}{caption}` |

## Cover Stripping Modes

- **`none`:** Retains all Markdown content (recommended when Markdown has only YAML frontmatter and report chapters).
- **`before-first-h1`:** Discards manual Markdown title text appearing before the first `#` H1 heading so Pandoc's PTIT cover template renders cleanly instead.
- **`first-h1-cover`:** Discards an initial `# Report Title` cover heading and immediately following cover metadata paragraphs/blockquotes up to the next Markdown heading.

## Headings, Appendices, and Breakable Identifiers

- **Chapter/Appendix normalization:** Level-1 headings matching `Appendix <ID>:` or `Phụ lục <ID>:` insert `\appendix` once before the first appendix chapter and strip the redundant literal label so LaTeX auto-numbers chapters (`Appendix A ...` / `Phụ lục A ...`).
- **Breakable inline identifiers:** Inline code (`Code`) escapes special TeX symbols (`\_`, `\#`, `\&`, `\%`) and inserts `\allowbreak{}` after `_`, `.`, `/`, `(`, and `:` outside headings and wraps inline code inside headings with `\texorpdfstring{\texttt{...}}{...}` to prevent `hyperref` PDF bookmark warnings without nested `\texorpdfstring`.

## Adaptive Tables and HTML Line Breaks

Pipe tables in GitHub-Flavored Markdown frequently overflow margins in `longtable` when Pandoc receives zero/uniform column widths:

1. `<br>`, `<br/>`, and `<br />` HTML line breaks inside table cells convert into `\newline ` so multi-line cell specs survive LaTeX compilation.
2. Column widths are computed from maximum non-raw cell text lengths using a square-root weight normalized across all columns (`colspecs[c][2]`), forcing Pandoc to emit `\real{...}` wrapped `p{...}` columns.
3. Tables with `2–4` columns are wrapped in `{\footnotesize ...}`, while wide `5+` column tables wrap in `{\scriptsize ...}`.

## Figures, Adjacent Captions, and Landscape Pages

- Standalone images (`![](arch.png)` or `![alt](arch.png)`) check sibling `.pdf` files first when `prep.prefer-vector-pdf` is enabled.
- An immediately following italic/caption paragraph (`*Hình 1: Kiến trúc tổng thể*` or `*Figure 2: Flow*`) automatically merges into the figure caption while stripping duplicate figure numbering prefixes.
- Images tagged `{.landscape}` or listed in `landscape-figures` emit `\landscapefigure{src}{caption}` using `pdflscape` rotated full-width layout.

## Supported GFM Callouts

| GFM Marker | LaTeX Environment Call |
| --- | --- |
| `> [!NOTE]` | `\begin{reportcallout}{Note}{calloutnote}` |
| `> [!TIP]` | `\begin{reportcallout}{Tip}{callouttip}` |
| `> [!IMPORTANT]` | `\begin{reportcallout}{Important}{calloutimportant}` |
| `> [!WARNING]` | `\begin{reportcallout}{Warning}{calloutwarning}` |
| `> [!CAUTION]` | `\begin{reportcallout}{Caution}{calloutcaution}` |
