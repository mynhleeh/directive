# Engine Selection, Fonts, and Encoding

This guide helps you choose between **LuaLaTeX**, **XeLaTeX**, and **pdfLaTeX** when converting Markdown reports to PDF with `md2latex-ptit`.

## Engine Decision Matrix

| Feature | LuaLaTeX (Co-Default) | XeLaTeX (Co-Default) | pdfLaTeX (Legacy Fallback) |
| --- | --- | --- | --- |
| Template | `assets/templates/report-unicode.tex` | `assets/templates/report-unicode.tex` | `assets/templates/report-pdflatex.tex` |
| Native UTF-8 & System Fonts | Full Unicode via `fontspec` | Full Unicode via `fontspec` | Requires `T5,T1` + `babel` |
| Vietnamese Diacritics (`ă, â, đ, ệ, ơ, ư`) | Native | Native | Prose supported via `T5`; code needs fallback |
| `microtype` Support | Full protrusion + font expansion | Protrusion only (`expansion=false`) | Full protrusion + expansion (Type1 fonts) |
| Non-ASCII Comments Inside Code Fences | Supported directly in `listings` | Supported directly in `listings` | Breaks `listings`; requires `--code-verbatim` (`fvextra`) |
| Typical Compile Speed | Moderate (first MiKTeX run caches Lua fonts) | Fast | Fastest |

## Co-Default Selection Rules

1. **Use `lualatex` (default)** for Vietnamese and bilingual technical reports containing accented code comments, Unicode box-drawing (`├──`, `└──`), wide tables, and modern OpenType typography where full `microtype` expansion improves justification.
2. **Use `xelatex`** when targeting faster OpenType Unicode compilation or matching pre-existing XeLaTeX institution templates that disable `microtype` expansion.
3. **Use `pdflatex` only** for strict ASCII/English legacy environments, CI runners lacking system TrueType/OpenType fonts, or journal venues requiring pdfTeX output.

## Font Fallback Hierarchy

In `assets/templates/report-unicode.tex`, `fontspec` resolves fonts gracefully via `\IfFontExistsTF`:

- **Body serif (`mainfont`)**: `Times New Roman` -> `TeX Gyre Termes` -> `Latin Modern Roman`.
- **Monospace (`monofont`)**: `Consolas` -> `DejaVu Sans Mono` -> `Latin Modern Mono`.

Override either font cleanly in YAML frontmatter or defaults files without editing the template:

```yaml
---
lang: vi
mainfont: Times New Roman
monofont: Consolas
---
```

## Non-ASCII Code Fences on pdfLaTeX

Because LaTeX `listings` parses single bytes in legacy 8-bit `pdflatex`, Vietnamese comments, box-drawing characters, or typographic symbols inside fenced code blocks fail or corrupt output.

- **Automatic detection:** `preflight_markdown` sets `has_utf8_code = True` and emits a warning when targeting `--engine pdflatex`.
- **Safe resolution:** Pass `--code-verbatim` to `build-report.py build`, which switches template macro support to `fvextra` (`\begin{Verbatim}[breaklines=true,fontsize=\small]`) and disables `listings` syntax parsing, or switch to `--engine lualatex` / `--engine xelatex`.

## Windows MiKTeX Format Troubleshooting

If `lualatex` stops immediately with `Sorry, but "MiKTeX Configuration Utility" did not succeed` or `lualatex.fmt` missing:

```powershell
miktex fndb refresh
miktex formats build lualatex --engine luahbtex
```

Verify both `kpsewhich` package resolution and a test compile after refreshing formats.
