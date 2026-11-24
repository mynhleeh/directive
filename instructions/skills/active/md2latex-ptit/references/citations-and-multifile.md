# Citations and Multi-File Assembly

Large engineering and academic reports frequently span chapter directories (`chapters/*.md`) and BibTeX libraries (`refs.bib`). `md2latex-ptit` automates assembly, heading normalization, and citation compilation.

## Multi-File Assembly (`assemble`)

Use `scripts/build-report.py assemble`—or pass multi-file flags directly to `build-report.py build`—with one of three deterministic ordering modes:

| Flag | Source Strategy | Notes |
| --- | --- | --- |
| `--dir DIR` | Natural numeric sort across `DIR/*.md` | Excludes assembled output; orders `00-preface.md`, `01-intro.md`, `02-arch.md` reliably |
| `--manifest FILE` | Reads `.txt` (line-per-path, `#` comments ignored) or `.json` array | Resolves relative chapter paths from `manifest` parent directory |
| `--inputs A.md B.md ...` | Explicit CLI order | Ideal for custom subsets or ad-hoc appendices |

- **Frontmatter stripping:** Individual chapter YAML headers (`--- ... ---`) are removed during concatenation so secondary frontmatter never leaks into body text.
- **Heading shifting:** Pass `--shift-headings +1` or `--shift-headings -1` to normalize ATX heading levels outside fenced code blocks cleanly.

```bash
python scripts/build-report.py assemble --dir docs/chapters --shift-headings 0 --output build/report.md
```

## Citation Modes Comparison

Pass `--bibliography path/to/refs.bib` to `build-report.py build` with one of three bibliography backends:

| Backend Flag | Pipeline Stage | Best Use Case | Multi-Pass Tool |
| --- | --- | --- | --- |
| `--citeproc` (default with `--bibliography`) | Pandoc resolves citations into `CSLReferences` | Most portable across LuaLaTeX, XeLaTeX, and pdfLaTeX; supports custom CSL styles | None required |
| `--biblatex` | Template `\printbibliography` | Custom BibLaTeX sorting/grouping, multi-section bibliographies | Runs `biber` automatically |
| `--natbib` | Template `\bibliographystyle` / `\bibliography` | Legacy journal compatibility or `pdflatex` BibTeX-only templates | Runs `bibtex` automatically |

## Troubleshooting Unresolved Citations

- If `audit-log` reports `LaTeX Warning: Citation ... undefined`, confirm the citation key in `refs.bib` matches `@key` (`[@vaswani2017]`), verify `refs.bib` path resolution, and inspect `rerun_needed` flags.
- For Vietnamese author names or UTF-8 fields inside `.bib` files, prefer `--citeproc` or `--biblatex` (`biber`) over legacy `--natbib` (`bibtex`).
