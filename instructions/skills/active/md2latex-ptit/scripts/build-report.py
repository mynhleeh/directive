#!/usr/bin/env python3
"""Build, preflight, assemble, and log-audit helper for md2latex-ptit."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from contextlib import nullcontext
from pathlib import Path
from typing import Iterable

SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_ROOT / "assets" / "templates"
PRESETS_DIR = SKILL_ROOT / "assets" / "presets"
LUA_FILTER_PATH = Path(__file__).resolve().parent / "report-prep.lua"

UNSUPPORTED_DIAGRAM_LANGS = {"mermaid", "plantuml", "dot", "graphviz", "d2"}
RASTER_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


EXCLUDED_DIR_NAMES = {"readme.md", "index.md"}


def _natural_sort_key(path: Path) -> list[tuple[int, int | str]]:
    parts = re.findall(r"\d+|\D+", path.name.lower())
    return [(0, int(p)) if p.isdigit() else (1, p) for p in parts]


def _strip_yaml_comment(line: str) -> str:
    in_quote = ""
    for i, ch in enumerate(line):
        if ch in ("'", '"'):
            if in_quote == ch:
                in_quote = ""
            elif not in_quote:
                in_quote = ch
        elif ch == "#" and not in_quote and (i == 0 or line[i - 1].isspace()):
            return line[:i]
    return line


def _parse_yaml_scalar(val: str) -> object:
    v = val.strip()
    if len(v) >= 2 and ((v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'")):
        return v[1:-1]
    low = v.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    return v


def _parse_simple_yaml(text: str) -> dict:
    raw_lines = [_strip_yaml_comment(l).rstrip() for l in text.replace("\r\n", "\n").splitlines()]
    lines = [(len(l) - len(l.lstrip(" ")), l.strip()) for l in raw_lines if l.strip()]
    root: dict = {}
    stack: list[tuple[int, dict | list]] = [(-1, root)]

    for idx, (indent, stripped) in enumerate(lines):
        while len(stack) > 1:
            top_indent, top_container = stack[-1]
            if indent < top_indent:
                stack.pop()
            elif indent == top_indent and not (isinstance(top_container, list) and stripped.startswith("- ")):
                stack.pop()
            else:
                break

        parent = stack[-1][1]
        if stripped.startswith("- ") and isinstance(parent, list):
            item_raw = stripped[2:].strip()
            kv_m = re.match(r"^([A-Za-z0-9_.-]+):\s*(.*)$", item_raw)
            if kv_m:
                item_dict: dict = {}
                key, rest = kv_m.group(1), kv_m.group(2)
                if rest == "":
                    nxt_is_list = idx + 1 < len(lines) and lines[idx + 1][1].startswith("- ")
                    child: dict | list = [] if nxt_is_list else {}
                    item_dict[key] = child
                    parent.append(item_dict)
                    stack.append((indent, item_dict))
                    stack.append((indent + 1, child))
                else:
                    item_dict[key] = _parse_yaml_scalar(rest)
                    parent.append(item_dict)
                    stack.append((indent, item_dict))
            else:
                parent.append(_parse_yaml_scalar(item_raw))
            continue

        kv_m = re.match(r"^([A-Za-z0-9_.-]+):\s*(.*)$", stripped)
        if kv_m and isinstance(parent, dict):
            key, rest = kv_m.group(1), kv_m.group(2)
            if rest == "":
                nxt_is_list = idx + 1 < len(lines) and lines[idx + 1][0] >= indent and lines[idx + 1][1].startswith("- ")
                child_container: dict | list = [] if nxt_is_list else {}
                parent[key] = child_container
                stack.append((indent, child_container))
            else:
                parent[key] = _parse_yaml_scalar(rest)
    return root


def _split_frontmatter(text: str) -> tuple[str, str]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    match = re.match(r"^---\n(.*?\n)---(?:\n+|$)", normalized, flags=re.DOTALL)
    if not match:
        return "", normalized
    return match.group(0), normalized[match.end() :]


def _shift_markdown_headings(body: str, shift: int) -> str:
    if shift == 0:
        return body
    out_lines: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    for line in body.split("\n"):
        fence_m = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if fence_m:
            marker = fence_m.group(1)
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
                fence_len = len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_len:
                in_fence = False
            out_lines.append(line)
            continue
        if not in_fence:
            h_m = re.match(r"^(#{1,6})(\s+.*)$", line)
            if h_m:
                new_level = max(1, min(6, len(h_m.group(1)) + shift))
                out_lines.append(("#" * new_level) + h_m.group(2))
                continue
        out_lines.append(line)
    return "\n".join(out_lines)


def _resolve_chapter_sources(
    inputs: Iterable[Path] | None,
    manifest: Path | None,
    directory: Path | None,
    output: Path,
) -> list[Path]:
    provided = sum(x is not None for x in (inputs, manifest, directory))
    if provided != 1:
        raise ValueError("Specify exactly one of inputs, manifest, or directory.")

    if inputs is not None:
        files = [Path(p) for p in inputs]
    elif manifest is not None:
        mpath = Path(manifest)
        if not mpath.is_file():
            raise FileNotFoundError(f"Manifest not found: {mpath}")
        raw = mpath.read_text(encoding="utf-8-sig")
        if mpath.suffix.lower() == ".json":
            entries = json.loads(raw)
            files = [(mpath.parent / str(item)) for item in entries]
        else:
            files = []
            for raw_line in raw.splitlines():
                stripped = raw_line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                files.append(mpath.parent / stripped)
    else:
        dpath = Path(directory)  # type: ignore[arg-type]
        if not dpath.is_dir():
            raise NotADirectoryError(f"Directory not found: {dpath}")
        out_resolved = output.resolve()
        all_candidates = [
            p
            for p in dpath.glob("*.md")
            if p.resolve() != out_resolved
            and p.name.lower() not in EXCLUDED_DIR_NAMES
            and not p.name.lower().startswith("assembled")
            and not p.stem.lower().endswith("-tong-hop")
        ]
        numbered = [p for p in all_candidates if re.match(r"^\d+[-_].*\.md$", p.name)]
        selected = numbered if numbered else all_candidates
        files = sorted(selected, key=_natural_sort_key)

    missing = [str(p) for p in files if not p.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing chapter files: {', '.join(missing)}")
    if not files:
        raise ValueError("No Markdown chapter files found to assemble.")
    return files


def assemble_markdown(
    inputs: list[Path] | None,
    manifest: Path | None,
    directory: Path | None,
    output: Path,
    shift_headings: int = 0,
) -> Path:
    out_path = Path(output)
    sources = _resolve_chapter_sources(inputs, manifest, directory, out_path)
    chunks: list[str] = []
    for src in sources:
        raw = src.read_text(encoding="utf-8-sig")
        _, body = _split_frontmatter(raw)
        shifted = _shift_markdown_headings(body.strip("\n"), shift_headings)
        if shifted.strip():
            chunks.append(shifted.strip())

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n\n".join(chunks) + "\n", encoding="utf-8")
    return out_path


def _is_list_item(line: str) -> bool:
    return bool(re.match(r"^\s*(?:[-*+]|\d+[.)])\s+\S", line))


def _is_nonlist_prose_line(line: str) -> bool:
    s = line.strip()
    if not s or _is_list_item(line):
        return False
    if s.startswith(("#", ">", "|", "```", "~~~", "<!--")):
        return False
    if re.match(r"^(?:---+|\*\*\*+|___+)$", s):
        return False
    return True


def _strip_inline_code(line: str) -> str:
    return re.sub(r"(`+)(?!`)(.+?)(?<!`)\1(?!`)", "", line)


def _extract_image_targets(line: str) -> list[str]:
    clean = _strip_inline_code(line)
    targets: list[str] = []
    for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", clean):
        raw_target = m.group(1).strip()
        if raw_target.startswith("<") and ">" in raw_target:
            target = raw_target[1 : raw_target.index(">")]
        else:
            target = raw_target.split()[0]
        targets.append(target)
    for m in re.finditer(r"<img[^>]+src=[\"']([^\"']+)[\"']", clean, flags=re.IGNORECASE):
        targets.append(m.group(1).strip())
    return targets


def _split_pipe_cells(line: str) -> list[str]:
    # Strip inline code and dollar-delimited math spans so $a | b$ isn't split mistakenly unless unescaped |
    row = line.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return re.split(r"(?<!\\)\|", row)


def _check_table_row_defects(line: str, idx: int, expected_cols: int | None) -> tuple[list[str], int | None]:
    row_issues: list[str] = []
    no_code = _strip_inline_code(line)
    for m in re.finditer(r"(?<!\\)\$([^$]+)(?<!\\)\$", no_code):
        if re.search(r"(?<!\\)\|", m.group(1)):
            row_issues.append(
                f"Line {idx}: unescaped pipe '|' inside table math span breaks Pandoc pipe table; use \\vert or \\mid."
            )
    if re.match(r"^\s*\|[\s:\-\|]+\|\s*$", line):
        sep_cols = len(_split_pipe_cells(no_code))
        return row_issues, sep_cols
    if expected_cols is not None:
        masked_math = re.sub(r"(?<!\\)\$[^$]+(?<!\\)\$", "MATH", no_code)
        actual_cols = len(_split_pipe_cells(masked_math))
        if actual_cols != expected_cols:
            row_issues.append(
                f"Line {idx}: table row has {actual_cols} columns, expected {expected_cols}."
            )
    return row_issues, expected_cols


def _asset_exists(target: str, search_dirs: list[Path]) -> bool:
    if target.startswith(("http://", "https://", "data:", "#")):
        return True
    candidate = Path(target)
    candidates = [candidate]
    if candidate.suffix.lower() in RASTER_SUFFIXES:
        candidates.append(candidate.with_suffix(".pdf"))
    for base in search_dirs:
        for cand in candidates:
            full = cand if cand.is_absolute() else (base / cand)
            if full.is_file():
                return True
    return False


def preflight_markdown(
    md_path: Path,
    engine: str = "lualatex",
    resource_paths: list[Path] | None = None,
    fix_lists: bool = False,
) -> dict:
    path = Path(md_path)
    issues: list[str] = []
    warnings: list[str] = []
    fixed_lists = 0
    has_utf8_code = False

    if not path.is_file():
        return {
            "issues": [f"Markdown file not found: {path}"],
            "warnings": [],
            "fixed_lists": 0,
            "has_utf8_code": False,
            "passed": False,
        }

    raw = path.read_text(encoding="utf-8-sig")
    frontmatter, body = _split_frontmatter(raw)
    search_dirs = [path.parent] + [Path(p) for p in (resource_paths or [])]

    lines = body.split("\n")
    rebuilt_lines: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    fence_start = 0
    in_list_block = False
    table_cols: int | None = None

    for idx, line in enumerate(lines, start=1):
        fence_m = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if fence_m:
            marker = fence_m.group(1)
            info = fence_m.group(2).strip().split()
            lang = info[0].lower() if info else ""
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
                fence_len = len(marker)
                fence_start = idx
                if lang in UNSUPPORTED_DIAGRAM_LANGS:
                    issues.append(
                        f"Line {idx}: raw `{lang}` fence cannot compile directly in LaTeX; pre-render to PDF or PNG first."
                    )
            elif marker[0] == fence_char and len(marker) >= fence_len:
                in_fence = False
            in_list_block = False
            table_cols = None
            rebuilt_lines.append(line)
            continue

        if in_fence:
            if any(ord(ch) > 127 for ch in line):
                has_utf8_code = True
            rebuilt_lines.append(line)
            continue

        stripped = line.strip()
        prev_line = rebuilt_lines[-1] if rebuilt_lines else ""

        if stripped == "":
            in_list_block = False
            table_cols = None
            rebuilt_lines.append(line)
            continue

        is_indented_cont = bool(re.match(r"^(?:  +|\t)\S", line)) and in_list_block
        if _is_list_item(line):
            if not in_list_block and _is_nonlist_prose_line(prev_line):
                if fix_lists:
                    rebuilt_lines.append("")
                    fixed_lists += 1
                else:
                    issues.append(
                        f"Line {idx}: tight list lacks blank line after previous paragraph (Pandoc collapses into paragraph)."
                    )
            in_list_block = True
        elif not is_indented_cont:
            in_list_block = False

        for target in _extract_image_targets(line):
            if not _asset_exists(target, search_dirs):
                issues.append(f"Line {idx}: missing image asset '{target}'.")

        if stripped.startswith("|"):
            t_issues, table_cols = _check_table_row_defects(line, idx, table_cols)
            issues.extend(t_issues)
            if re.match(r"^\s*\|[\s:\-\|]+\|\s*$", line) and table_cols and table_cols >= 6:
                warnings.append(
                    f"Line {idx}: wide table with {table_cols} columns; verify landscape or \\scriptsize layout."
                )
        else:
            table_cols = None

        rebuilt_lines.append(line)

    if in_fence:
        issues.append(f"Unclosed fenced code block opened at body line {fence_start}.")

    if has_utf8_code and engine.lower() == "pdflatex":
        warnings.append(
            "Non-ASCII UTF-8 characters found inside code blocks while targeting pdflatex; enable code-verbatim: true (fvextra) or switch to lualatex/xelatex."
        )

    if fix_lists and fixed_lists > 0:
        path.write_text(frontmatter + "\n".join(rebuilt_lines), encoding="utf-8")

    return {
        "issues": issues,
        "warnings": warnings,
        "fixed_lists": fixed_lists,
        "has_utf8_code": has_utf8_code,
        "passed": len(issues) == 0,
    }


_VI_DIACRITIC_RE = re.compile(
    r"[ăâđêôơưĂÂĐÊÔƠƯàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]"
)


def _parse_kv_pairs(pairs: list[str] | None) -> dict[str, object]:
    out: dict[str, object] = {}
    for item in pairs or []:
        if "=" not in item:
            raise ValueError(f"Expected KEY=VALUE argument, got '{item}'.")
        k, v = item.split("=", 1)
        out[k.strip()] = _parse_yaml_scalar(v)
    return out


def inspect_markdown(
    md_path: Path | None = None,
    *,
    inputs: list[Path] | None = None,
    manifest: Path | None = None,
    directory: Path | None = None,
    resource_paths: list[Path] | None = None,
) -> dict:
    source_mode_count = sum(x is not None for x in (inputs, manifest, directory))
    if source_mode_count > 1 or (md_path is not None and source_mode_count > 0):
        raise ValueError("Provide either md_path or one of inputs/manifest/directory.")

    if source_mode_count == 1:
        with tempfile.TemporaryDirectory() as td:
            asm = Path(td) / "_inspect.md"
            sources = _resolve_chapter_sources(inputs, manifest, directory, asm)
            assemble_markdown(inputs, manifest, directory, asm)
            raw = asm.read_text(encoding="utf-8-sig")
            search_dirs = list(dict.fromkeys([p.parent.resolve() for p in sources] + [Path(p).resolve() for p in (resource_paths or [])]))
    elif md_path is not None:
        p = Path(md_path)
        if not p.is_file():
            raise FileNotFoundError(f"Markdown file not found: {p}")
        raw = p.read_text(encoding="utf-8-sig")
        search_dirs = list(dict.fromkeys([p.parent.resolve()] + [Path(rp).resolve() for rp in (resource_paths or [])]))
    else:
        raise ValueError("No Markdown file or directory specified.")

    fm_raw, body = _split_frontmatter(raw)
    fm_body = re.sub(r"^---\n|\n---(?:\n+|$)", "", fm_raw, flags=re.DOTALL)
    frontmatter = _parse_simple_yaml(fm_body) if fm_body.strip() else {}

    lines = body.split("\n")
    word_count = len(body.split())
    vi_hits = len(_VI_DIACRITIC_RE.findall(body))
    fm_lang = str(frontmatter.get("lang", "")).lower()
    detected_lang = "vi" if (fm_lang.startswith("vi") or vi_hits >= 3) else "en"

    in_fence = False
    fence_char = ""
    fence_len = 0
    seen_first_h1 = False
    has_pre_h1_prose = False
    first_h1_idx: int | None = None
    first_h1_cover_signals = False
    first_h1_prose_after = False

    headings_count = 0
    min_level = 7
    max_level = 0
    numbered_count = 0
    appendix_count = 0
    has_code_in_headings = False

    table_count = 0
    max_cols = 0
    has_html_br = False
    in_table = False

    code_blocks = 0
    code_langs: list[str] = []
    has_utf8_code = False
    unsupported_diagrams: list[str] = []

    fig_count = 0
    missing_assets: list[str] = []
    landscape_count = 0
    has_pdf_siblings = False
    inline_cite_count = 0
    callout_count = 0

    for idx, line in enumerate(lines, start=1):
        fence_m = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if fence_m:
            marker = fence_m.group(1)
            info = fence_m.group(2).strip().split()
            lang = info[0].lower() if info else ""
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
                fence_len = len(marker)
                code_blocks += 1
                if lang:
                    if lang not in code_langs:
                        code_langs.append(lang)
                    if lang in UNSUPPORTED_DIAGRAM_LANGS and lang not in unsupported_diagrams:
                        unsupported_diagrams.append(lang)
            elif marker[0] == fence_char and len(marker) >= fence_len:
                in_fence = False
            in_table = False
            continue

        if in_fence:
            if any(ord(ch) > 127 for ch in line):
                has_utf8_code = True
            continue

        stripped = line.strip()
        h_m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if h_m:
            lvl = len(h_m.group(1))
            htext = h_m.group(2).strip()
            headings_count += 1
            min_level = min(min_level, lvl)
            max_level = max(max_level, lvl)
            if not seen_first_h1 and lvl == 1:
                seen_first_h1 = True
                first_h1_idx = idx
            elif first_h1_idx is not None:
                first_h1_idx = None  # Stop tracking cover window after next heading
            if re.match(r"^(?:\d+\.(?:\d+\.?)*|[A-Z]\.\d+(?:\.\d+)*)\s+", htext):
                numbered_count += 1
            if lvl == 1 and re.match(r"^(?:appendix|phụ\s+lục)\s+[A-Za-z0-9]+", htext, flags=re.IGNORECASE):
                appendix_count += 1
            if "`" in htext:
                has_code_in_headings = True
            in_table = False
            continue

        if not seen_first_h1 and stripped and not stripped.startswith("<!--"):
            has_pre_h1_prose = True
        if first_h1_idx is not None and stripped:
            if stripped.startswith((">", "-", "*", "|", "---")):
                first_h1_cover_signals = True
            else:
                first_h1_prose_after = True

        if re.match(r"^\s*>\s*\[!(?:NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]", line, flags=re.IGNORECASE):
            callout_count += 1

        if stripped.startswith("|"):
            if "<br" in line.lower():
                has_html_br = True
            if re.match(r"^\s*\|[\s:\-\|]+\|\s*$", line):
                cols = len(_split_pipe_cells(_strip_inline_code(line)))
                max_cols = max(max_cols, cols)
                if not in_table:
                    table_count += 1
                    in_table = True
        else:
            in_table = False

        no_code = _strip_inline_code(line)
        inline_cite_count += len(re.findall(r"\[[^\]]*@[A-Za-z0-9_:\-]+[^\]]*\]", no_code))

        if "{.landscape}" in line:
            landscape_count += 1
        for target in _extract_image_targets(line):
            fig_count += 1
            if not _asset_exists(target, search_dirs):
                missing_assets.append(target)
            elif Path(target).suffix.lower() in RASTER_SUFFIXES and _asset_exists(str(Path(target).with_suffix(".pdf")), search_dirs):
                has_pdf_siblings = True

    first_h1_looks_like_cover = bool(first_h1_cover_signals and not first_h1_prose_after)
    rec_docclass = str(frontmatter.get("documentclass") or ("report" if (appendix_count > 0 or headings_count >= 5 or len(lines) >= 180) else "article"))
    rec_engine = "lualatex" if (detected_lang == "vi" or has_utf8_code or max_cols >= 5) else "xelatex"
    rec_toc = bool(frontmatter["toc"]) if "toc" in frontmatter else (headings_count >= 4)
    rec_cover = str(frontmatter.get("cover-style") or ("boxed" if rec_docclass == "report" else "minimal"))
    rec_strip_cover = "before-first-h1" if has_pre_h1_prose else ("first-h1-cover" if first_h1_looks_like_cover else "none")

    decision_points = [
        {
            "parameter": "engine",
            "recommended": rec_engine,
            "alternatives": ["lualatex", "xelatex", "pdflatex"],
            "reason": "LuaLaTeX/XeLaTeX handle UTF-8 natively; LuaLaTeX adds full microtype expansion.",
        },
        {
            "parameter": "documentclass & cover-style",
            "recommended": f"{rec_docclass} + {rec_cover}",
            "alternatives": ["report + boxed", "report + minimal", "article + minimal", "article + none"],
            "reason": f"Detected {headings_count} headings, {len(lines)} lines, appendix_count={appendix_count}.",
        },
        {
            "parameter": "toc & lists",
            "recommended": f"toc={rec_toc}, lof={fig_count > 0}, lot={table_count > 0}",
            "alternatives": ["--toc / --no-toc", "--compact-toc", "--lof", "--lot"],
            "reason": "Short articles often skip TOC/LOF/LOT; academic reports typically include TOC.",
        },
    ]
    if has_pre_h1_prose or first_h1_looks_like_cover:
        decision_points.append({
            "parameter": "strip-cover",
            "recommended": rec_strip_cover,
            "alternatives": ["none", "before-first-h1", "first-h1-cover"],
            "reason": "Manual title/cover content detected near top of Markdown.",
        })
    if inline_cite_count > 0 and "bibliography" not in frontmatter:
        decision_points.append({
            "parameter": "bibliography backend",
            "recommended": "citeproc",
            "alternatives": ["citeproc", "biblatex", "natbib"],
            "reason": f"Found {inline_cite_count} inline citation marker(s); supply .bib path if needed.",
        })

    return {
        "frontmatter": frontmatter,
        "detected_lang": detected_lang,
        "line_count": len(lines),
        "word_count": word_count,
        "headings": {
            "count": headings_count,
            "min_level": 0 if min_level == 7 else min_level,
            "max_level": max_level,
            "numbered_count": numbered_count,
            "appendix_count": appendix_count,
            "has_code_in_headings": has_code_in_headings,
        },
        "cover_signals": {
            "has_frontmatter_title": "title" in frontmatter,
            "has_pre_h1_prose": has_pre_h1_prose,
            "first_h1_looks_like_cover": first_h1_looks_like_cover,
        },
        "tables": {
            "count": table_count,
            "max_cols": max_cols,
            "has_html_br": has_html_br,
        },
        "code": {
            "block_count": code_blocks,
            "languages": code_langs,
            "has_utf8_code": has_utf8_code,
            "unsupported_diagrams": unsupported_diagrams,
        },
        "figures": {
            "count": fig_count,
            "missing_assets": missing_assets,
            "landscape_count": landscape_count,
            "has_vector_pdf_siblings": has_pdf_siblings,
        },
        "citations": {
            "inline_cite_count": inline_cite_count,
            "frontmatter_bib": frontmatter.get("bibliography"),
        },
        "callouts": {"count": callout_count},
        "recommended_options": {
            "engine": rec_engine,
            "documentclass": rec_docclass,
            "lang": detected_lang,
            "toc": rec_toc,
            "cover_style": rec_cover,
            "strip_cover": rec_strip_cover,
            "strip_heading_numbers": numbered_count > 0,
            "adaptive_tables": table_count > 0,
            "code_verbatim": False,
        },
        "decision_points": decision_points,
    }


def _unwrap_tex_log_lines(raw_lines: list[str]) -> list[str]:
    unwrapped: list[str] = []
    new_record_prefixes = (
        "! ",
        "l.",
        "Runaway argument?",
        "Overfull ",
        "Underfull ",
        "Missing character:",
        "LaTeX Warning:",
        "LaTeX Error:",
        "Package ",
        "Class ",
        "Output written on ",
        "Transcript written on ",
        "No file ",
        "(",
        "[",
    )
    for line in raw_lines:
        if (
            unwrapped
            and line
            and not line.startswith(new_record_prefixes)
            and re.match(r"^(?:LaTeX|Package |Class |Missing character:|Overfull )", unwrapped[-1])
            and not unwrapped[-1].endswith(".")
        ):
            unwrapped[-1] = unwrapped[-1] + line
        else:
            unwrapped.append(line)
    return unwrapped


def parse_latex_log(
    log_path: Path,
    max_overfull: int = 0,
    overfull_threshold_pt: float = 1.0,
) -> dict:
    path = Path(log_path)
    if not path.is_file():
        raise FileNotFoundError(f"LaTeX log file not found: {path}")

    raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lines = _unwrap_tex_log_lines(raw_lines)
    errors: list[str] = []
    undefined_controls: list[str] = []
    overfull_hbox: list[str] = []
    missing_chars: list[str] = []
    undefined_refs: list[str] = []
    rerun_needed = False
    pages: int | None = None

    for idx, line in enumerate(lines):
        if line.startswith("! ") or line.startswith("Runaway argument?"):
            context = lines[idx + 1].strip() if idx + 1 < len(lines) and lines[idx + 1].startswith("l.") else ""
            entry = f"{line.strip()} {context}".strip()
            errors.append(entry)
            if "Undefined control sequence" in line:
                undefined_controls.append(entry)
            continue

        oh_m = re.search(r"Overfull \\hbox \(([\d.]+)pt too wide\)", line)
        if oh_m and float(oh_m.group(1)) > overfull_threshold_pt:
            overfull_hbox.append(line.strip())
            continue

        if "Missing character:" in line:
            missing_chars.append(line.strip())
            continue

        if (
            re.search(r"LaTeX Warning: (?:Reference|Citation) .+ undefined", line)
            or "There were undefined references" in line
            or "There were undefined citations" in line
        ):
            undefined_refs.append(line.strip())

        if (
            "Rerun to get cross-references right" in line
            or "Label(s) may have changed" in line
            or "Please (re)run Biber" in line
            or "Please rerun LaTeX" in line
            or "Table widths have changed" in line
        ):
            rerun_needed = True

        pg_m = re.search(r"Output written on .+?\((\d+)\s+page", line)
        if pg_m:
            pages = int(pg_m.group(1))

    passed = (
        len(errors) == 0
        and len(undefined_controls) == 0
        and len(missing_chars) == 0
        and len(overfull_hbox) <= max_overfull
        and len(undefined_refs) == 0
        and not rerun_needed
    )
    return {
        "errors": errors,
        "undefined_controls": undefined_controls,
        "overfull_hbox": overfull_hbox,
        "missing_chars": missing_chars,
        "undefined_refs": undefined_refs,
        "rerun_needed": rerun_needed,
        "pages": pages,
        "passed": passed,
    }


def _diagnose_tex_failure(engine: str, log_text: str, stderr_text: str) -> list[str]:
    combined = f"{stderr_text}\n{log_text}"
    hints: list[str] = []
    if "lualatex.fmt" in combined or "can't find the format file" in combined.lower():
        hints.append("Rebuild MiKTeX format cache: `miktex fndb refresh && miktex formats build lualatex --engine luahbtex`.")
    for m in re.finditer(r"File `([^']+\.sty)' not found", combined):
        hints.append(f"Install missing LaTeX package containing `{m.group(1)}` via MiKTeX Console or `mpm`.")
    if engine == "pdflatex" and ("Invalid UTF-8 byte" in combined or "Unicode character" in combined):
        hints.append("Re-run with `--code-verbatim` (fvextra) or switch to `--engine lualatex` / `--engine xelatex`.")
    return list(dict.fromkeys(hints))


def _select_template(engine: str, custom_template: Path | None) -> Path:
    if custom_template is not None:
        return Path(custom_template)
    name = "report-pdflatex.tex" if engine == "pdflatex" else "report-unicode.tex"
    return TEMPLATES_DIR / name


def _build_prep_metadata(
    strip_cover: str | None,
    code_verbatim: bool,
    strip_heading_numbers: bool | None = None,
    adaptive_tables: bool | None = None,
    callout_boxes: bool | None = None,
    prefer_vector_pdf: bool | None = None,
) -> dict:
    prep: dict[str, object] = {
        "strip-heading-numbers": True if strip_heading_numbers is None else strip_heading_numbers,
        "prefer-vector-pdf": True if prefer_vector_pdf is None else prefer_vector_pdf,
        "callout-boxes": True if callout_boxes is None else callout_boxes,
        "adaptive-tables": True if adaptive_tables is None else adaptive_tables,
        "code-verbatim": code_verbatim,
        "code-listings": not code_verbatim,
    }
    if strip_cover is not None:
        prep["strip-cover"] = strip_cover
    return {"prep": prep}


def _compile_tex(
    tex_path: Path,
    engine: str,
    build_dir: Path,
    texinputs_dirs: list[Path],
    bib_mode: str,
    max_overfull: int,
    overfull_threshold_pt: float,
) -> tuple[bool, dict | None, list[str], str]:
    env = os.environ.copy()
    search_str = os.pathsep.join(str(p.resolve()) for p in texinputs_dirs)
    existing_tex = env.get("TEXINPUTS", "")
    existing_bib = env.get("BIBINPUTS", "")
    env["TEXINPUTS"] = f"{search_str}{os.pathsep}{existing_tex}{os.pathsep}"
    env["BIBINPUTS"] = f"{search_str}{os.pathsep}{existing_bib}{os.pathsep}"

    def run_engine() -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [engine, "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
            cwd=build_dir,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

    proc = run_engine()
    if proc.returncode != 0:
        log_file = build_dir / f"{tex_path.stem}.log"
        log_txt = log_file.read_text(encoding="utf-8", errors="replace") if log_file.is_file() else ""
        audit = parse_latex_log(log_file, max_overfull, overfull_threshold_pt) if log_file.is_file() else None
        return False, audit, _diagnose_tex_failure(engine, log_txt, proc.stderr + proc.stdout), proc.stderr or proc.stdout

    if bib_mode == "biblatex" and (build_dir / f"{tex_path.stem}.bcf").is_file():
        if not shutil.which("biber"):
            return False, None, ["Install `biber` or pass `--citeproc` instead of `--biblatex`."], "`biber` binary not found in PATH."
        b_res = subprocess.run(["biber", tex_path.stem], cwd=build_dir, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if b_res.returncode != 0:
            return False, None, ["Verify `.bib` syntax and citation keys; or pass `--citeproc`."], f"biber failed:\n{b_res.stderr}\n{b_res.stdout}"
    elif bib_mode == "natbib":
        aux_txt = (build_dir / f"{tex_path.stem}.aux").read_text(encoding="utf-8", errors="replace") if (build_dir / f"{tex_path.stem}.aux").is_file() else ""
        if "\\bibdata" in aux_txt:
            if not shutil.which("bibtex"):
                return False, None, ["Install `bibtex` or pass `--citeproc` instead of `--natbib`."], "`bibtex` binary not found in PATH."
            b_res = subprocess.run(["bibtex", tex_path.stem], cwd=build_dir, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
            if b_res.returncode != 0:
                return False, None, ["Verify `.bib` syntax/encoding; for UTF-8 `.bib` files prefer `--citeproc` or `--biblatex`."], f"bibtex failed:\n{b_res.stderr}\n{b_res.stdout}"

    proc = run_engine()
    if proc.returncode == 0 and bib_mode in ("biblatex", "natbib"):
        proc = run_engine()
    log_file = build_dir / f"{tex_path.stem}.log"
    audit = parse_latex_log(log_file, max_overfull, overfull_threshold_pt) if log_file.is_file() else None
    if proc.returncode == 0 and audit and audit["rerun_needed"]:
        proc = run_engine()
        audit = parse_latex_log(log_file, max_overfull, overfull_threshold_pt) if log_file.is_file() else None

    if proc.returncode != 0:
        log_txt = log_file.read_text(encoding="utf-8", errors="replace") if log_file.is_file() else ""
        return False, audit, _diagnose_tex_failure(engine, log_txt, proc.stderr + proc.stdout), proc.stderr or proc.stdout

    return True, audit, [], ""


def _load_defaults_dict(defaults_path: Path | None) -> tuple[dict, list[Path]]:
    if defaults_path is None:
        return {}, []
    dpath = Path(defaults_path)
    if not dpath.is_file():
        raise FileNotFoundError(f"Defaults file not found: {dpath}")
    raw = dpath.read_text(encoding="utf-8-sig")
    parsed = json.loads(raw) if dpath.suffix.lower() == ".json" else _parse_simple_yaml(raw)
    extra_res = [
        (dpath.parent / str(p)).resolve()
        for p in (parsed.get("resource-path") or [])
        if str(p).strip() not in ("", ".", "./")
    ]
    return parsed, extra_res


def build_report(
    input_md: Path | None = None,
    *,
    inputs: list[Path] | None = None,
    manifest: Path | None = None,
    directory: Path | None = None,
    shift_headings: int = 0,
    engine: str = "lualatex",
    documentclass: str | None = None,
    top_level_division: str | None = None,
    lang: str | None = None,
    cover_style: str | None = None,
    strip_cover: str | None = None,
    strip_heading_numbers: bool | None = None,
    adaptive_tables: bool | None = None,
    callout_boxes: bool | None = None,
    prefer_vector_pdf: bool | None = None,
    toc: bool | None = None,
    lof: bool | None = None,
    lot: bool | None = None,
    number_sections: bool | None = None,
    defaults: Path | None = None,
    template: Path | None = None,
    resource_paths: list[Path] | None = None,
    bibliography: Path | None = None,
    csl: Path | None = None,
    citeproc: bool = False,
    biblatex: bool = False,
    natbib: bool = False,
    code_verbatim: bool = False,
    compact_toc: bool = False,
    fix_lists: bool = False,
    toc_depth: int | None = None,
    extra_vars: list[str] | None = None,
    extra_meta: list[str] | None = None,
    extra_prep: list[str] | None = None,
    out_pdf: Path | None = None,
    out_tex: Path | None = None,
    work_dir: Path | None = None,
    max_overfull: int = 0,
    overfull_threshold_pt: float = 1.0,
    tex_only: bool = False,
) -> dict:
    if not shutil.which("pandoc"):
        return {"passed": False, "stage": "environment", "engine": engine, "message": "`pandoc` binary not found in PATH.", "hints": ["Install Pandoc 3.x+."]}
    if not tex_only and not shutil.which(engine):
        return {"passed": False, "stage": "environment", "engine": engine, "message": f"`{engine}` binary not found in PATH.", "hints": [f"Install TeX engine `{engine}`."]}

    defaults_data, defaults_res = _load_defaults_dict(defaults)
    defaults_vars = dict(defaults_data.get("variables") or {}) if isinstance(defaults_data.get("variables"), dict) else {}
    defaults_meta = dict(defaults_data.get("metadata") or {}) if isinstance(defaults_data.get("metadata"), dict) else {}

    ctx = nullcontext(Path(work_dir)) if work_dir else tempfile.TemporaryDirectory()
    with ctx as td_raw:
        build_dir = Path(td_raw)
        build_dir.mkdir(parents=True, exist_ok=True)

        source_mode_count = sum(x is not None for x in (inputs, manifest, directory))
        if source_mode_count > 1 or (input_md is not None and source_mode_count > 0):
            return {"passed": False, "stage": "arguments", "engine": engine, "message": "Provide either a single input Markdown file OR one of --inputs/--manifest/--dir."}

        chapter_dirs: list[Path] = []
        if source_mode_count == 1:
            assembled_md = build_dir / "_assembled.md"
            sources = _resolve_chapter_sources(inputs, manifest, directory, assembled_md)
            chapter_dirs = [p.parent.resolve() for p in sources]
            assemble_markdown(inputs, manifest, directory, assembled_md, shift_headings=shift_headings)
            active_md = assembled_md
            default_stem = "report"
            base_dir = Path(directory) if directory else (Path(manifest).parent if manifest else Path(inputs[0]).parent)  # type: ignore[index]
        elif input_md is not None:
            active_md = Path(input_md)
            default_stem = active_md.stem
            base_dir = active_md.parent
        else:
            return {"passed": False, "stage": "arguments", "engine": engine, "message": "No input Markdown file or directory specified."}

        res_dirs = list(
            dict.fromkeys(
                [base_dir.resolve(), active_md.parent.resolve()]
                + chapter_dirs
                + defaults_res
                + [Path(p).resolve() for p in (resource_paths or [])]
            )
        )
        preflight = preflight_markdown(active_md, engine=engine, resource_paths=res_dirs, fix_lists=fix_lists)
        if not preflight["passed"]:
            return {
                "passed": False,
                "stage": "preflight",
                "engine": engine,
                "preflight": preflight,
                "message": "Preflight checks failed.",
                "hints": preflight["issues"],
            }

        fm_raw, _ = _split_frontmatter(active_md.read_text(encoding="utf-8-sig"))
        fm_body = re.sub(r"^---\n|\n---(?:\n+|$)", "", fm_raw, flags=re.DOTALL)
        md_frontmatter = _parse_simple_yaml(fm_body) if fm_body.strip() else {}
        md_prep = dict(md_frontmatter.get("prep") or {}) if isinstance(md_frontmatter.get("prep"), dict) else {}

        effective_verbatim = bool(code_verbatim or (engine == "pdflatex" and preflight["has_utf8_code"]))
        if effective_verbatim and engine == "pdflatex" and not code_verbatim:
            preflight["warnings"].append("Auto-enabled `--code-verbatim` (`fvextra`) because UTF-8 code lines target `pdflatex`.")

        effective_docclass = str(documentclass or defaults_vars.get("documentclass") or md_frontmatter.get("documentclass") or "report")
        effective_toc_depth = int(toc_depth if toc_depth is not None else defaults_data.get("toc-depth", md_frontmatter.get("toc-depth", 3)))
        if toc is not None:
            effective_toc = toc
        elif "table-of-contents" in defaults_data:
            effective_toc = bool(defaults_data["table-of-contents"])
        elif "toc" in md_frontmatter:
            effective_toc = bool(md_frontmatter["toc"])
        else:
            effective_toc = True
        top_div = top_level_division or ("section" if effective_docclass == "article" else "chapter")

        merged_prep = dict(defaults_meta.get("prep") or {}) if isinstance(defaults_meta.get("prep"), dict) else {}
        merged_prep.update(md_prep)
        prep_override = _build_prep_metadata(
            strip_cover,
            effective_verbatim,
            strip_heading_numbers=strip_heading_numbers,
            adaptive_tables=adaptive_tables,
            callout_boxes=callout_boxes,
            prefer_vector_pdf=prefer_vector_pdf,
        )["prep"]
        for k, v in prep_override.items():
            if (
                k not in merged_prep
                or k in ("code-verbatim", "code-listings")
                or (k == "strip-cover" and strip_cover is not None)
                or (k == "strip-heading-numbers" and strip_heading_numbers is not None)
                or (k == "adaptive-tables" and adaptive_tables is not None)
                or (k == "callout-boxes" and callout_boxes is not None)
                or (k == "prefer-vector-pdf" and prefer_vector_pdf is not None)
            ):
                merged_prep[k] = v
        merged_prep.update(_parse_kv_pairs(extra_prep))

        merged_meta = dict(defaults_meta)
        merged_meta["prep"] = merged_prep
        cli_meta_flags: list[tuple[str, object]] = []
        if lang is not None:
            merged_meta.pop("lang", None)
            cli_meta_flags.append(("lang", lang))
        for k, v in _parse_kv_pairs(extra_meta).items():
            merged_meta.pop(k, None)
            cli_meta_flags.append((k, v))

        merged_vars = dict(defaults_vars)
        merged_vars["documentclass"] = effective_docclass
        if cover_style is not None:
            merged_vars["cover-style"] = cover_style
        if lof is not None:
            merged_vars["lof"] = lof
        if lot is not None:
            merged_vars["lot"] = lot
        if number_sections is False:
            merged_vars["secnumdepth"] = -1
        if compact_toc:
            merged_vars["compact-toc"] = True
        if effective_verbatim:
            merged_vars["code-verbatim"] = True
            merged_meta.pop("code-verbatim", None)
        merged_vars.update(_parse_kv_pairs(extra_vars))

        tpl_path = _select_template(engine, template)
        merged_defaults: dict[str, object] = {
            "from": "markdown",
            "to": "latex",
            "standalone": True,
            "template": str(tpl_path.resolve()),
            "filters": [str(LUA_FILTER_PATH.resolve())],
            "table-of-contents": effective_toc,
            "toc-depth": effective_toc_depth,
            "wrap": "none",
            "eol": "lf",
            "resource-path": [str(build_dir.resolve())] + [str(p) for p in res_dirs],
            "variables": merged_vars,
        }
        if top_div != "default":
            merged_defaults["top-level-division"] = top_div
        if number_sections is True:
            merged_defaults["number-sections"] = True
        defaults_json_path = build_dir / "_merged_defaults.json"
        defaults_json_path.write_text(json.dumps(merged_defaults, ensure_ascii=False, indent=2), encoding="utf-8")

        override_meta_path = build_dir / "_prep_meta.json"
        override_meta_path.write_text(json.dumps(merged_meta, ensure_ascii=False, indent=2), encoding="utf-8")

        tex_file = build_dir / f"{default_stem}.tex"
        pandoc_cmd = [
            "pandoc",
            str(active_md.resolve()),
            f"--defaults={defaults_json_path.resolve()}",
            f"--metadata-file={override_meta_path.resolve()}",
            "-o",
            str(tex_file),
        ]
        for mk, mv in cli_meta_flags:
            if isinstance(mv, bool):
                pandoc_cmd.extend(["-M", f"{mk}={'true' if mv else 'false'}"])
            else:
                pandoc_cmd.extend(["-M", f"{mk}={mv}"])
        if csl is not None:
            csl_resolved = Path(csl).resolve()
            if not csl_resolved.is_file():
                return {"passed": False, "stage": "arguments", "engine": engine, "message": f"CSL style file not found: {csl_resolved}"}
            pandoc_cmd.append(f"--csl={csl_resolved}")

        bib_mode = "none"
        eff_bib = bibliography or (Path(defaults_data["bibliography"]) if defaults_data.get("bibliography") else None)
        if eff_bib is not None:
            bib_resolved = (defaults.parent / eff_bib).resolve() if (bibliography is None and defaults is not None and not eff_bib.is_absolute()) else Path(eff_bib).resolve()
            if not bib_resolved.is_file():
                return {"passed": False, "stage": "arguments", "engine": engine, "message": f"Bibliography file not found: {bib_resolved}"}
            bib_copy = build_dir / "_refs.bib"
            if bib_resolved != bib_copy.resolve():
                shutil.copy2(bib_resolved, bib_copy)
            if biblatex:
                pandoc_cmd.extend(["--biblatex", "--bibliography=_refs.bib"])
                bib_mode = "biblatex"
            elif natbib:
                pandoc_cmd.extend(["--natbib", "--bibliography=_refs"])
                bib_mode = "natbib"
            else:
                pandoc_cmd.extend(["--citeproc", f"--bibliography={bib_copy.as_posix()}"])
                bib_mode = "citeproc"
        elif citeproc:
            pandoc_cmd.append("--citeproc")
            bib_mode = "citeproc"

        p_res = subprocess.run(pandoc_cmd, cwd=build_dir, capture_output=True, text=True, encoding="utf-8")
        if p_res.returncode != 0:
            return {
                "passed": False,
                "stage": "pandoc",
                "engine": engine,
                "preflight": preflight,
                "message": p_res.stderr.strip() or "Pandoc conversion failed.",
                "hints": [],
            }

        saved_tex: str | None = None
        if out_tex is not None:
            out_tex_path = Path(out_tex)
            out_tex_path.parent.mkdir(parents=True, exist_ok=True)
            if tex_file.resolve() != out_tex_path.resolve():
                shutil.copy2(tex_file, out_tex_path)
            saved_tex = str(out_tex_path)

        if tex_only:
            return {
                "passed": True,
                "stage": "pandoc",
                "engine": engine,
                "tex_path": saved_tex or str(tex_file),
                "pdf_path": None,
                "preflight": preflight,
                "log_audit": None,
                "hints": [],
            }

        ok_compile, audit, hints, raw_err = _compile_tex(
            tex_file, engine, build_dir, [build_dir] + res_dirs, bib_mode, max_overfull, overfull_threshold_pt
        )
        compiled_pdf = build_dir / f"{tex_file.stem}.pdf"
        if not ok_compile or not compiled_pdf.is_file():
            return {
                "passed": False,
                "stage": "latex",
                "engine": engine,
                "tex_path": saved_tex,
                "pdf_path": None,
                "preflight": preflight,
                "log_audit": audit,
                "hints": hints,
                "message": raw_err.strip() or "LaTeX compilation failed.",
            }

        target_pdf = Path(out_pdf) if out_pdf is not None else (base_dir / f"{default_stem}.pdf")
        target_pdf.parent.mkdir(parents=True, exist_ok=True)
        if compiled_pdf.resolve() != target_pdf.resolve():
            shutil.copy2(compiled_pdf, target_pdf)

        passed = bool(audit and audit["passed"])
        return {
            "passed": passed,
            "stage": "complete",
            "engine": engine,
            "tex_path": saved_tex,
            "pdf_path": str(target_pdf),
            "preflight": preflight,
            "log_audit": audit,
            "hints": hints,
        }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="md2latex-ptit helper CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_asm = sub.add_parser("assemble", help="Assemble chapter Markdown files in deterministic order.")
    p_asm.add_argument("--inputs", nargs="+", type=Path, help="Ordered list of input Markdown files.")
    p_asm.add_argument("--manifest", type=Path, help="Manifest file (.txt or .json) listing chapter files.")
    p_asm.add_argument("--dir", type=Path, help="Directory of Markdown chapters sorted naturally.")
    p_asm.add_argument("--output", required=True, type=Path, help="Combined Markdown output path.")
    p_asm.add_argument("--shift-headings", type=int, default=0, help="ATX heading level delta.")

    p_pre = sub.add_parser("preflight", help="Audit Markdown before Pandoc conversion.")
    p_pre.add_argument("input", type=Path, help="Input Markdown file.")
    p_pre.add_argument("--engine", default="lualatex", choices=["lualatex", "xelatex", "pdflatex"])
    p_pre.add_argument("--resource-path", action="append", default=[], type=Path, help="Asset lookup directory.")
    p_pre.add_argument("--fix-lists", action="store_true", help="Insert blank lines before tight lists in-place.")
    p_pre.add_argument("--json", action="store_true", help="Emit JSON output.")

    p_log = sub.add_parser("audit-log", help="Parse LaTeX compilation .log file for defects.")
    p_log.add_argument("log", type=Path, help="Path to .log file.")
    p_log.add_argument("--max-overfull", type=int, default=0)
    p_log.add_argument("--overfull-threshold-pt", type=float, default=1.0)
    p_log.add_argument("--json", action="store_true", help="Emit JSON output.")

    p_ins = sub.add_parser("inspect", help="Profile Markdown structure and emit parameter choices for AI/user review.")
    p_ins.add_argument("input", nargs="?", type=Path, help="Input Markdown file.")
    p_ins.add_argument("--inputs", nargs="+", type=Path, help="Ordered chapter Markdown files.")
    p_ins.add_argument("--manifest", type=Path, help="Chapter manifest file.")
    p_ins.add_argument("--dir", type=Path, help="Directory of ordered Markdown chapters.")
    p_ins.add_argument("--resource-path", action="append", default=[], type=Path)
    p_ins.add_argument("--json", action="store_true", help="Emit JSON output.")

    p_bld = sub.add_parser("build", help="Assemble, preflight, render .tex, compile PDF, and audit logs.")
    p_bld.add_argument("input", nargs="?", type=Path, help="Input Markdown file.")
    p_bld.add_argument("--inputs", nargs="+", type=Path, help="Ordered chapter Markdown files.")
    p_bld.add_argument("--manifest", type=Path, help="Chapter manifest file.")
    p_bld.add_argument("--dir", type=Path, help="Directory of ordered Markdown chapters.")
    p_bld.add_argument("--shift-headings", type=int, default=0)
    p_bld.add_argument("--engine", default="lualatex", choices=["lualatex", "xelatex", "pdflatex"])
    p_bld.add_argument("--documentclass", choices=["report", "article"])
    p_bld.add_argument("--top-level-division", choices=["default", "part", "chapter", "section"])
    p_bld.add_argument("--lang", choices=["en", "vi"])
    p_bld.add_argument("--cover-style", choices=["boxed", "minimal", "none"])
    p_bld.add_argument("--strip-cover", choices=["none", "before-first-h1", "first-h1-cover"])
    p_bld.add_argument("--no-strip-heading-numbers", dest="strip_heading_numbers", action="store_false", default=None)
    p_bld.add_argument("--no-adaptive-tables", dest="adaptive_tables", action="store_false", default=None)
    p_bld.add_argument("--no-callout-boxes", dest="callout_boxes", action="store_false", default=None)
    p_bld.add_argument("--no-prefer-vector-pdf", dest="prefer_vector_pdf", action="store_false", default=None)
    p_bld.add_argument("--toc", dest="toc", action="store_true", default=None)
    p_bld.add_argument("--no-toc", dest="toc", action="store_false")
    p_bld.add_argument("--lof", dest="lof", action="store_true", default=None)
    p_bld.add_argument("--no-lof", dest="lof", action="store_false")
    p_bld.add_argument("--lot", dest="lot", action="store_true", default=None)
    p_bld.add_argument("--no-lot", dest="lot", action="store_false")
    p_bld.add_argument("--number-sections", dest="number_sections", action="store_true", default=None)
    p_bld.add_argument("--no-number-sections", dest="number_sections", action="store_false")
    p_bld.add_argument("--defaults", type=Path, help="Optional Pandoc YAML defaults file.")
    p_bld.add_argument("--template", type=Path, help="Optional custom LaTeX template.")
    p_bld.add_argument("--resource-path", action="append", default=[], type=Path)
    p_bld.add_argument("--bibliography", type=Path)
    p_bld.add_argument("--csl", type=Path, help="Optional CSL bibliography style file.")
    p_bld.add_argument("--citeproc", action="store_true")
    p_bld.add_argument("--biblatex", action="store_true")
    p_bld.add_argument("--natbib", action="store_true")
    p_bld.add_argument("--code-verbatim", action="store_true")
    p_bld.add_argument("--compact-toc", action="store_true")
    p_bld.add_argument("--fix-lists", action="store_true")
    p_bld.add_argument("--toc-depth", type=int, default=None)
    p_bld.add_argument("--var", dest="extra_vars", action="append", default=[], help="Template variable KEY=VALUE.")
    p_bld.add_argument("--meta", dest="extra_meta", action="append", default=[], help="Metadata field KEY=VALUE.")
    p_bld.add_argument("--prep", dest="extra_prep", action="append", default=[], help="Lua filter prep option KEY=VALUE.")
    p_bld.add_argument("--out-pdf", type=Path)
    p_bld.add_argument("--out-tex", type=Path)
    p_bld.add_argument("--work-dir", type=Path)
    p_bld.add_argument("--max-overfull", type=int, default=0)
    p_bld.add_argument("--overfull-threshold-pt", type=float, default=1.0)
    p_bld.add_argument("--tex-only", action="store_true")
    p_bld.add_argument("--json", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "assemble":
        out = assemble_markdown(args.inputs, args.manifest, args.dir, args.output, args.shift_headings)
        print(f"Assembled: {out}")
        return 0

    if args.command == "preflight":
        res = preflight_markdown(args.input, args.engine, args.resource_path, args.fix_lists)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(f"PASSED: {res['passed']} | fixed_lists={res['fixed_lists']} | has_utf8_code={res['has_utf8_code']}")
            for msg in res["issues"]:
                print(f"[ISSUE] {msg}", file=sys.stderr)
            for msg in res["warnings"]:
                print(f"[WARN]  {msg}")
        return 0 if res["passed"] else 1

    if args.command == "audit-log":
        res = parse_latex_log(args.log, args.max_overfull, args.overfull_threshold_pt)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(f"PASSED: {res['passed']} | pages={res['pages']} | rerun_needed={res['rerun_needed']}")
            for msg in res["errors"] + res["missing_chars"] + res["undefined_refs"] + res["overfull_hbox"]:
                print(f"[DEFECT] {msg}", file=sys.stderr)
        return 0 if res["passed"] else 1

    if args.command == "inspect":
        res = inspect_markdown(
            args.input,
            inputs=args.inputs,
            manifest=args.manifest,
            directory=args.dir,
            resource_paths=args.resource_path,
        )
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            rec = res["recommended_options"]
            print(f"LANG={res['detected_lang']} | LINES={res['line_count']} | HEADINGS={res['headings']['count']} | REC={rec}")
        return 0

    if args.command == "build":
        res = build_report(
            args.input,
            inputs=args.inputs,
            manifest=args.manifest,
            directory=args.dir,
            shift_headings=args.shift_headings,
            engine=args.engine,
            documentclass=args.documentclass,
            top_level_division=args.top_level_division,
            lang=args.lang,
            cover_style=args.cover_style,
            strip_cover=args.strip_cover,
            strip_heading_numbers=args.strip_heading_numbers,
            adaptive_tables=args.adaptive_tables,
            callout_boxes=args.callout_boxes,
            prefer_vector_pdf=args.prefer_vector_pdf,
            toc=args.toc,
            lof=args.lof,
            lot=args.lot,
            number_sections=args.number_sections,
            defaults=args.defaults,
            template=args.template,
            resource_paths=args.resource_path,
            bibliography=args.bibliography,
            csl=args.csl,
            citeproc=args.citeproc,
            biblatex=args.biblatex,
            natbib=args.natbib,
            code_verbatim=args.code_verbatim,
            compact_toc=args.compact_toc,
            fix_lists=args.fix_lists,
            toc_depth=args.toc_depth,
            extra_vars=args.extra_vars,
            extra_meta=args.extra_meta,
            extra_prep=args.extra_prep,
            out_pdf=args.out_pdf,
            out_tex=args.out_tex,
            work_dir=args.work_dir,
            max_overfull=args.max_overfull,
            overfull_threshold_pt=args.overfull_threshold_pt,
            tex_only=args.tex_only,
        )
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(f"PASSED: {res['passed']} | stage={res['stage']} | engine={res['engine']} | pdf={res.get('pdf_path')}")
            for h in res.get("hints", []):
                print(f"[HINT] {h}", file=sys.stderr)
            if not res["passed"] and res.get("message"):
                print(f"[ERROR] {res['message']}", file=sys.stderr)
        return 0 if res["passed"] else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
