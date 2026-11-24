---
name: md2latex-ptit
description: "Use when converting single-file or multi-file Markdown reports in English or Vietnamese to LaTeX or PDF, configuring LuaLaTeX, XeLaTeX, or pdfLaTeX templates and PTIT covers, or fixing broken Pandoc lists, wide tables, identifiers, Mermaid blocks, citations, and TeX logs. Do NOT use for docx/xlsx/pptx conversion, LaTeX posters (latex-posters), journal venue templates (venue-templates), or slides (scientific-slides)."
---

# Markdown to LaTeX Report Pipeline (md2latex-ptit)

**Violating the letter of the pipeline rules is violating the spirit of the rules.** Never improvise ad-hoc `pandoc` one-liners, never assume fixed parameters without inspecting the Markdown first, never strip Markdown headings destructively by hand, never regex-patch generated `.tex` files, and never declare a PDF done based solely on exit code `0` or file creation.

Use the deterministic toolchain bundled in this skill (`scripts/build-report.py`, `scripts/report-prep.lua`, `assets/templates/`, and `assets/presets/`) relative to `<SKILL_DIR>`.

## 1. Interactive Inspection & Adaptive Workflow

Always inspect first, let the user choose open formatting trade-offs, and adapt `build-report.py` flags dynamically to fit the document and target output:

1. **Assemble Multi-File Chapters (skip if single file):** Concatenate chapters cleanly before inspecting, noting that `assemble` strips per-file YAML frontmatter:

```bash
python <SKILL_DIR>/scripts/build-report.py assemble \
  --dir docs/chapters \
  --shift-headings 0 \
  --output build/assembled.md
```

2. **Inspect Markdown Structure (`inspect`) Before Choosing Parameters:** Run read-only `inspect` (and read the Markdown header) to detect language (`vi`/`en`), line/heading count, appendix markers, existing YAML frontmatter, pre-H1 cover prose, table column widths (`max_cols`), UTF-8 code lines, raw `mermaid`/`dot` blocks, and inline `[@citations]`:

```bash
python <SKILL_DIR>/scripts/build-report.py inspect report.md --json
```

3. **Present Options & Let the User Choose Open Decisions (Clarify Gate):** Do **not** blindly force `--engine lualatex --lang vi --cover-style boxed --toc` on every input. Unless the user already specified all layout choices explicitly in their prompt or YAML frontmatter (or asked for zero-question auto-build), summarize the `inspect` findings and ask the user to confirm key ambiguous choices (`decision_points`) with a crisp options table + grounded recommendation:
   - **Document layout:** Formal multi-chapter PTIT report (`--documentclass report`, `--cover-style boxed|minimal`, `--toc`, `--lof`/`--lot`) vs concise memo/spec (`--documentclass article`, `--cover-style none|minimal`, `--no-toc`).
   - **Engine:** `lualatex` (co-default, best for `vi`, UTF-8 code, full `microtype`) vs `xelatex` (co-default, fast OpenType) vs `pdflatex` (legacy ASCII/constrained fallback).
   - **Cover / headings / citations:** Which `--strip-cover` mode (`none`, `before-first-h1`, `first-h1-cover`), whether manual `# 1.` numbers stay or strip, whether to run `--fix-lists`, and `.bib` path + backend (`--citeproc`, `--biblatex`, `--natbib`) if inline citations exist.

4. **Pre-Render Raw Diagrams & Run Preflight Gate:** Convert any raw `mermaid`, `plantuml`, `dot`, `graphviz`, or `d2` code fences to cropped vector PDF first (`npx @mermaid-js/mermaid-cli -i arch.mmd -o figures/arch.pdf --pdfFit`), then verify cleanly with `preflight`:

```bash
python <SKILL_DIR>/scripts/build-report.py preflight report.md --engine <chosen> --resource-path figures --json
```

5. **Run Adaptive `build` With Chosen Parameters:** Never hardcode a static flag set—supply only the switches matching the document analysis and confirmed user choices (when Markdown frontmatter already configures keys like `documentclass`, `toc`, `cover-style`, `lang`, omitting overriding CLI flags lets frontmatter govern cleanly):

```bash
python <SKILL_DIR>/scripts/build-report.py build <input.md | --dir ...> \
  --engine <lualatex|xelatex|pdflatex> \
  --documentclass <report|article> \
  --lang <vi|en> \
  [--cover-style <boxed|minimal|none>] [--strip-cover <none|before-first-h1|first-h1-cover>] \
  [--toc|--no-toc] [--compact-toc] [--toc-depth 2] [--lof] [--lot] \
  [--no-number-sections] [--no-strip-heading-numbers] [--no-adaptive-tables] \
  [--bibliography refs.bib --citeproc|--biblatex|--natbib] [--csl style.csl] \
  [--var accent-color-rgb=0,51,153] [--meta subtitle=...] [--prep callout-boxes=true] \
  --work-dir build --out-tex build/report.tex --out-pdf build/report.pdf --json
```

6. **Enforce Zero-Defect Log Audit Gate:** File creation proves nothing. Require `log_audit.passed == true` from `build --json` (or `audit-log build/<stem>.log --max-overfull 0 --json`) with `errors == []`, `undefined_controls == []`, `missing_chars == []`, `undefined_refs == []`, `rerun_needed == false`, and `len(overfull_hbox) <= max_overfull`.

## 2. Dynamic Parameter Decision Matrix

| Document / Output Signal (`inspect`) | Recommended Parameters | Alternative Choices to Offer User |
| --- | --- | --- |
| Long report (`>= 5` headings, `>= 180` lines, or `# Appendix` / `# Phụ lục`) | `--documentclass report --cover-style boxed --toc` | `--cover-style minimal`, `--compact-toc`, `--lof`, `--lot`, `--defaults <preset.yaml>` |
| Short design note, lab memo, or spec (`< 5` headings, no appendix) | `--documentclass article --cover-style minimal --no-toc` | `--cover-style none` (start directly at Section 1), `--toc`, `--no-number-sections` |
| Vietnamese text (`detected_lang: vi`) or `has_utf8_code: true` | `--engine lualatex --lang vi` | `--engine xelatex` (fast OpenType); `--engine pdflatex --code-verbatim` only if legacy pdfTeX required |
| Manual title prose before H1, or `# Cover Title` + metadata before `## 1.` | `--strip-cover before-first-h1` or `first-h1-cover` | `--strip-cover none` + `--cover-style none` to keep Markdown's native title prose |
| Wide tables (`max_cols >= 5`) or `<br>` cell breaks | Keep `adaptive-tables: true` (default) | `--no-adaptive-tables` or `--var`/`landscape-figures` for custom widths |
| Inline `[@key]` citations found (`inline_cite_count > 0`) | `--bibliography <path> --citeproc` | `--biblatex` (`biber`), `--natbib` (`bibtex`), custom `--csl` |
| Custom branding, fonts, or PTIT member roles | `--var mainfont=... --var show-member-role=true --var accent-color-rgb=...` | Starter YAML preset copied from `assets/presets/defaults-*.yaml` |

## 3. Reference Guides & Starter Presets

| Domain Topic | Reference Guide |
| --- | --- |
| Engine matrix (`lualatex`/`xelatex`/`pdflatex`), `fontspec` fallbacks, MiKTeX format rebuilds | [engine-selection-and-fonts.md](references/engine-selection-and-fonts.md) |
| Lua filter keys (`prep.*`), adaptive tables, `<br>` cells, `{.landscape}`, GFM callouts | [lua-prep-and-tables.md](references/lua-prep-and-tables.md) |
| Multi-file `assemble` flags and `--citeproc` vs `--biblatex` vs `--natbib` | [citations-and-multifile.md](references/citations-and-multifile.md) |
| PTIT covers (`boxed`/`minimal`/`none`), CLI `--var`/`--meta` overrides, log audit rubric | [ptit-cover-and-templates.md](references/ptit-cover-and-templates.md) |

## 4. Rationalization Table & Red Flags

| Excuse Heard Under Pressure | Reality & Required Action |
| --- | --- |
| "Just assume `boxed` PTIT `report` with `--engine lualatex --lang vi --toc` and skip asking." | Hardcoded defaults turn a 1-page English note into a 4-page boxed Vietnamese report with an unwanted TOC. Always run `inspect`, align with desired output, and ask the user when layout choices are open. |
| "Deadline is tight; run bare `pandoc *.md --pdf-engine=pdflatex -o report.pdf` without `build-report.py`." | Bare `pandoc` loses Vietnamese code glyphs, flattens tight lists, breaks `<br>` tables, and skips log checks. Always use `build-report.py` with tailored flags. |
| "`report.pdf` exists on disk, so ignore `Missing character` or `Overfull \hbox`." | File existence hides missing glyphs and clipped columns. Require `audit-log` `passed: true`. |
| "Patch strings directly inside generated `.tex` or delete `# 1.` in source Markdown manually." | Fix root causes via Markdown assets, `--var`/`--meta`/`--prep` flags, or `report-prep.lua` (`--no-strip-heading-numbers` if manual numbers should stay). |

**Red Flags — STOP and Re-Align:** Running `build` without inspecting Markdown or confirming open layout choices; hardcoding `--cover-style boxed --toc` on short notes; invoking bare `pandoc` outside `build-report.py`; ignoring non-zero `audit-log` defects.
