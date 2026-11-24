# PTIT Cover Customization, Diagrams, and Log Audits

## PTIT Boxed Cover Presets and Variables

Both `report-unicode.tex` and `report-pdflatex.tex` render a formal Vietnamese or English PTIT title page without altering template code. Copy the matching preset from `assets/presets/` into your project and populate neutral placeholders:

```yaml
lang: vi                  # 'en' or 'vi' (switches Institution, Student ID, Instructor, Page headers)
cover-style: boxed        # 'boxed' (double border), 'minimal' (clean rule), or 'none' (chapter 1 immediately)
institution: HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG
faculty: KHOA CÔNG NGHỆ THÔNG TIN 1
cover-logo: logo.png      # Relative path resolved via --resource-path
title: BÁO CÁO BÀI TẬP LỚN
subtitle: Phân tích, Thiết kế và Triển khai Hệ thống
course: Mã học phần [Nhóm lớp]
team: "Nhóm 01"
members:
  - name: Sinh viên A
    id: B24XXXX001
  - name: Sinh viên B
    id: B24XXXX002
instructor: Giảng viên hướng dẫn
location-year: "Hà Nội, 2026"
compact-toc: false        # Set true to compress Table of Contents spacing via tocloft
```

When `--cover-style boxed` is active and frontmatter defines `title`, keep `prep.strip-cover` at `before-first-h1` or `first-h1-cover` if your source Markdown also starts with manual cover prose.

## Dynamic CLI Overrides (`--var`, `--meta`, `--prep`, Layout Flags)

Inspect any Markdown input first with `inspect --json` to retrieve `recommended_options` and `decision_points`, then pass only the overrides matching user preference:

- `--documentclass report|article`, `--top-level-division default|part|chapter|section`
- `--toc` / `--no-toc`, `--compact-toc`, `--toc-depth N`, `--lof` / `--no-lof`, `--lot` / `--no-lot`, `--no-number-sections`
- `--var KEY=VALUE` for template styling (`accent-color-rgb=120,20,20`, `mainfont=...`, `phase=Phase 2`, `show-member-role=true`)
- `--meta KEY=VALUE` and `--prep KEY=VALUE` (or `--no-strip-heading-numbers`, `--no-adaptive-tables`, `--no-callout-boxes`, `--no-prefer-vector-pdf`) to override Markdown frontmatter without modifying source files.

## Pre-Rendering Diagrams (`mermaid`, `drawio`, `dot`)

LaTeX engines cannot execute Mermaid or Draw.io source fences directly. `preflight_markdown` blocks raw `mermaid`, `plantuml`, `dot`, `graphviz`, and `d2` code fences before Pandoc runs.

Pre-render diagrams to cropped **vector PDF** (recommended) or high-DPI **PNG**:

```powershell
npx @mermaid-js/mermaid-cli -i arch.mmd -o arch.pdf --pdfFit
dot -Tpdf schema.dot -o schema.pdf
```

Save both raster (`arch.png`) and vector (`arch.pdf`) side by side if needed: `report-prep.lua` (`prep.prefer-vector-pdf: true`) embeds `.pdf` automatically during LaTeX compilation while Markdown viewers keep `.png`. Tag wide charts `{.landscape}` to invoke `\landscapefigure`.

## Deterministic Log Audit Rubric (`audit-log`)

Every build passes only when `parse_latex_log` returns zero blocking defects:

| Log Metric | Pass Condition | Remediation if Failed |
| --- | --- | --- |
| `errors` & `undefined_controls` | `0` items | Fix TeX macro typo, escape raw LaTeX tokens, or rebuild MiKTeX format cache |
| `missing_chars` | `0` items | Replace missing Unicode symbol in code/text or switch `pdflatex` to `lualatex` |
| `undefined_refs` | `0` items | Re-run compilation pass, verify `\label`/figure captions or `.bib` citation keys |
| `overfull_hbox` (`> 1.0pt`) | `<= max_overfull` (`0` default) | Convert wide inline code to Markdown backticks for `\allowbreak{}`, narrow table columns, or use `{.landscape}` |
