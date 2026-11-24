from __future__ import annotations

import json
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_ROOT / "assets" / "templates"
PRESETS_DIR = SKILL_ROOT / "assets" / "presets"
SCRIPTS_DIR = SKILL_ROOT / "scripts"


def make_minimal_png(path: Path, width: int = 32, height: int = 32) -> None:
    """Write a valid RGB PNG without external libraries."""
    raw_row = b"\x00" + (b"\x00\x33\x99" * width)
    raw = raw_row * height

    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    idat = zlib.compress(raw)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")
    path.write_bytes(png)


class TemplateSmokeTests(unittest.TestCase):
    def _run_pandoc_and_tex(
        self,
        tmp_path: Path,
        template_name: str,
        engine: str,
        lang: str,
        md_text: str,
        extra_meta: dict,
    ) -> tuple[Path, str]:
        template = TEMPLATES_DIR / template_name
        self.assertTrue(template.is_file(), f"Missing template: {template}")

        logo = tmp_path / "logo.png"
        make_minimal_png(logo)
        md_file = tmp_path / "report.md"
        md_file.write_text(md_text, encoding="utf-8")

        meta_file = tmp_path / "meta.json"
        meta = {
            "lang": lang,
            "cover-style": "boxed",
            "institution": "INSTITUTION NAME",
            "faculty": "FACULTY OF INFORMATION TECHNOLOGY",
            "cover-logo": "logo.png",
            "title": "TECHNICAL REPORT",
            "subtitle": "Multi-Engine Template Verification",
            "course": "Course Code 101",
            "team": "Team 01",
            "members": [{"name": "Author One", "id": "ID001"}],
            "instructor": "Instructor Name",
            "location-year": "City, 2026",
            "toc": True,
            "lof": True,
            **extra_meta,
        }
        meta_file.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")

        tex_file = tmp_path / "report.tex"
        pandoc_cmd = [
            "pandoc",
            str(md_file),
            "--from=markdown",
            "--to=latex",
            "--standalone",
            f"--template={template}",
            "--top-level-division=chapter",
            "--toc",
            f"--metadata-file={meta_file}",
            f"--resource-path={tmp_path}",
            "--wrap=none",
            "--eol=lf",
            "--fail-if-warnings",
            "-o",
            str(tex_file),
        ]
        res_p = subprocess.run(pandoc_cmd, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res_p.returncode, 0, f"Pandoc failed:\n{res_p.stderr}")
        self.assertTrue(tex_file.is_file())

        for _pass in range(2):
            res_t = subprocess.run(
                [engine, "-interaction=nonstopmode", "-halt-on-error", f"-output-directory={tmp_path}", str(tex_file)],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(res_t.returncode, 0, f"{engine} failed:\n{res_t.stdout[-2000:]}\n{res_t.stderr}")

        pdf_file = tmp_path / "report.pdf"
        log_file = tmp_path / "report.log"
        self.assertTrue(pdf_file.is_file())
        self.assertGreater(pdf_file.stat().st_size, 1024)
        log_text = log_file.read_text(encoding="utf-8", errors="replace")
        self.assertNotIn("! LaTeX Error", log_text)
        self.assertNotIn("Missing character:", log_text)
        return tex_file, log_text

    def test_presets_exist(self) -> None:
        for name in ("defaults-lualatex.yaml", "defaults-xelatex.yaml", "defaults-pdflatex.yaml"):
            preset = PRESETS_DIR / name
            self.assertTrue(preset.is_file(), f"Missing preset: {preset}")

    def test_templates_compile_lualatex_vi(self) -> None:
        if not shutil.which("lualatex"):
            self.skipTest("lualatex not available")
        with tempfile.TemporaryDirectory() as td:
            md = "# Tổng quan hệ thống\n\nNội dung tiếng Việt có dấu: ế, ộ, ử, ỹ.\n\n## Bảng dữ liệu\n\nDữ liệu mẫu.\n"
            tex, _log = self._run_pandoc_and_tex(Path(td), "report-unicode.tex", "lualatex", "vi", md, {})
            tex_src = tex.read_text(encoding="utf-8")
            self.assertIn(r"\ifluatex", tex_src)
            self.assertIn("Chương", tex_src)

    def test_templates_compile_xelatex_en(self) -> None:
        if not shutil.which("xelatex"):
            self.skipTest("xelatex not available")
        with tempfile.TemporaryDirectory() as td:
            md = "# System Overview\n\nEnglish text with code `sample_identifier`.\n\n## Architecture\n\nDetails.\n"
            tex, _log = self._run_pandoc_and_tex(Path(td), "report-unicode.tex", "xelatex", "en", md, {})
            tex_src = tex.read_text(encoding="utf-8")
            self.assertIn(r"\ifxetex", tex_src)
            self.assertIn("Chapter", tex_src)

    def test_templates_compile_pdflatex_ascii_and_verbatim(self) -> None:
        if not shutil.which("pdflatex"):
            self.skipTest("pdflatex not available")
        with tempfile.TemporaryDirectory() as td1:
            md_en = "# Overview\n\n```python\ndef add(a, b):\n    return a + b\n```\n"
            tex1, _ = self._run_pandoc_and_tex(Path(td1), "report-pdflatex.tex", "pdflatex", "en", md_en, {})
            self.assertNotIn("DefineVerbatimEnvironment{lstlisting}", tex1.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as td2:
            md_vi = "# Tổng quan\n\n```sql\n-- Ghi chú tiếng Việt UTF-8\nSELECT 1;\n```\n"
            tex2, _ = self._run_pandoc_and_tex(
                Path(td2),
                "report-pdflatex.tex",
                "pdflatex",
                "vi",
                md_vi,
                {"code-verbatim": True},
            )
            self.assertIn("DefineVerbatimEnvironment{lstlisting}", tex2.read_text(encoding="utf-8"))


class LuaFilterTests(unittest.TestCase):
    def _run_lua(self, md_text: str, meta: dict | None = None, cwd: Path | None = None) -> str:
        lua_filter = SCRIPTS_DIR / "report-prep.lua"
        self.assertTrue(lua_filter.is_file(), f"Missing Lua filter: {lua_filter}")
        with tempfile.TemporaryDirectory() as td:
            work = cwd or Path(td)
            md_path = Path(td) / "input.md"
            md_path.write_text(md_text, encoding="utf-8")
            cmd = [
                "pandoc",
                str(md_path),
                "--from=markdown",
                "--to=latex",
                "--top-level-division=chapter",
                f"--lua-filter={lua_filter}",
                "--wrap=none",
            ]
            if meta is not None:
                meta_path = Path(td) / "meta.json"
                meta_path.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                cmd.append(f"--metadata-file={meta_path}")
            res = subprocess.run(cmd, cwd=work, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(res.returncode, 0, f"Pandoc Lua filter failed:\n{res.stderr}")
            return res.stdout

    def test_lua_strip_cover_modes(self) -> None:
        md_preface = "Important preface text.\n\n# 1. Introduction\n\nBody.\n"
        out_none = self._run_lua(md_preface, {"prep": {"strip-cover": "none"}})
        self.assertIn("Important preface text.", out_none)

        md_before_h1 = "**INSTITUTION**\n\nTeam: 01\n\n# 1. Introduction\n\nBody.\n"
        out_before = self._run_lua(md_before_h1, {"prep": {"strip-cover": "before-first-h1"}})
        self.assertNotIn("INSTITUTION", out_before)
        self.assertIn(r"\chapter{Introduction}", out_before)

        md_first_h1 = "# Report Title\n\n> Metadata line\n\n## 1. Overview\n\nBody.\n"
        out_first = self._run_lua(md_first_h1, {"prep": {"strip-cover": "first-h1-cover"}})
        self.assertNotIn("Report Title", out_first)
        self.assertNotIn("Metadata line", out_first)
        self.assertIn("Overview", out_first)

    def test_lua_heading_numbers_and_appendix(self) -> None:
        md = "# 1. Overview\n\n## 1.1 Scope\n\n# Appendix A: SQL Scripts\n\n## A.1 Schema\n\n# Phụ lục B: Dữ liệu\n"
        out = self._run_lua(md)
        self.assertIn(r"\chapter{Overview}", out)
        self.assertIn(r"\section{Scope}", out)
        self.assertEqual(out.count(r"\appendix"), 1)
        self.assertIn(r"\chapter{SQL Scripts}", out)
        self.assertIn(r"\section{Schema}", out)
        self.assertIn(r"\chapter{Dữ liệu}", out)

    def test_lua_breakable_identifiers_and_headers(self) -> None:
        md = "# 1. Table `EMPLOYEE_CERTIFICATION`\n\nCall `service.process_order(item_id)` in `sql/01_schema_ddl.sql`.\n"
        out = self._run_lua(md)
        self.assertIn(r"EMPLOYEE\_\allowbreak{}CERTIFICATION", out)
        self.assertIn(r"service.\allowbreak{}process\_\allowbreak{}order(\allowbreak{}item\_\allowbreak{}id)", out)
        self.assertNotIn(r"\texorpdfstring{\texorpdfstring", out)

    def test_lua_code_blocks_and_verbatim(self) -> None:
        md = "```sql\nSELECT * FROM DUAL;\n```\n\n```json\n{\"ok\": true}\n```\n"
        out_hi = self._run_lua(md, {"prep": {"code-listings": True, "code-verbatim": False}})
        self.assertIn(r"\begin{lstlisting}[language=SQL]", out_hi)
        self.assertIn(r"\begin{lstlisting}[language=json]", out_hi)
        out_verb = self._run_lua(md, {"prep": {"code-listings": True, "code-verbatim": True}})
        self.assertNotIn("[language=SQL]", out_verb)
        self.assertIn(r"\begin{lstlisting}", out_verb)

    def test_lua_adaptive_tables(self) -> None:
        md_6col = (
            "| A | Column Long Header B | C | D | Description E | F |\n"
            "| --- | --- | --- | --- | --- | --- |\n"
            "| 1 | value_two | 3 | 4 | longer cell text here | ok |\n"
        )
        out_6 = self._run_lua(md_6col)
        self.assertIn(r"\scriptsize", out_6)

        md_5col = (
            "| ID | Name | Module | Status | Notes |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| 1 | Alpha | Core | Active | Detailed note spanning column |\n"
        )
        out_5 = self._run_lua(md_5col)
        self.assertIn(r"\scriptsize", out_5)

        md_2col = "| Field | Value<br>`line_two` |\n| --- | --- |\n| Key | Val |\n"
        out_2 = self._run_lua(md_2col)
        self.assertIn(r"\footnotesize", out_2)
        self.assertIn(r"\real{", out_2)

    def test_lua_figures_captions_and_landscape(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "arch.png").write_bytes(b"png")
            (root / "arch.pdf").write_bytes(b"%PDF-1.4\n")
            (root / "normal.png").write_bytes(b"png")
            md = (
                "![](arch.png){.landscape}\n\n"
                "*Hình 1: Kiến trúc tổng thể*\n\n"
                "![](normal.png)\n\n"
                "*Figure 2: Normal flow*\n"
            )
            out = self._run_lua(md, {"prep": {"prefer-vector-pdf": True}}, cwd=root)
            self.assertIn(r"\landscapefigure{arch.pdf}{Kiến trúc tổng thể}", out)
            self.assertIn(r"\includegraphics", out)
            self.assertIn(r"\caption{Normal flow}", out)

    def test_lua_gfm_callouts(self) -> None:
        md = (
            "> [!NOTE]\n> Verify engine logs.\n\n"
            "> [!WARNING]\n> Do not skip preflight.\n\n"
            "> [!CAUTION]\n> Avoid raw mermaid fences.\n"
        )
        out = self._run_lua(md)
        self.assertIn(r"\begin{reportcallout}{Note}{calloutnote}", out)
        self.assertIn(r"\begin{reportcallout}{Warning}{calloutwarning}", out)
        self.assertIn(r"\begin{reportcallout}{Caution}{calloutcaution}", out)
        self.assertNotIn("[!NOTE]", out)


class CliHelpersTests(unittest.TestCase):
    def _import_build_report(self):
        script = SCRIPTS_DIR / "build-report.py"
        self.assertTrue(script.is_file(), f"Missing CLI script: {script}")
        import importlib.util

        spec = importlib.util.spec_from_file_location("build_report", script)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)
        return mod

    def test_assemble_markdown_inputs_dir_manifest_and_heading_shift(self) -> None:
        mod = self._import_build_report()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ch0 = root / "00-preface.md"
            ch1 = root / "01-intro.md"
            ch0.write_text("---\ntitle: Ignored\n---\n\n# Preface\n\nIntro paragraph.\n", encoding="utf-8")
            ch1.write_text(
                "# Intro\n\n```python\n# not a heading\nprint('ok')\n```\n\n## Details\n",
                encoding="utf-8",
            )
            out_dir = root / "assembled_dir.md"
            mod.assemble_markdown(None, None, root, out_dir, shift_headings=1)
            txt = out_dir.read_text(encoding="utf-8")
            self.assertIn("## Preface", txt)
            self.assertIn("## Intro", txt)
            self.assertIn("### Details", txt)
            self.assertIn("# not a heading", txt)
            self.assertNotIn("title: Ignored", txt)

            manifest = root / "chapters.txt"
            manifest.write_text("# comment\n01-intro.md\n00-preface.md\n", encoding="utf-8")
            out_man = root / "assembled_manifest.md"
            mod.assemble_markdown(None, manifest, None, out_man, shift_headings=0)
            mtxt = out_man.read_text(encoding="utf-8")
            self.assertLess(mtxt.index("# Intro"), mtxt.index("# Preface"))

    def test_preflight_markdown_diagnostics_and_fix_lists(self) -> None:
        mod = self._import_build_report()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            res_dir = root / "assets"
            res_dir.mkdir()
            (res_dir / "ok.png").write_bytes(b"png")

            bad = root / "bad.md"
            bad.write_text(
                "# Title\n\nIntro line:\n- first item\n- second item\n\n"
                "```mermaid\ngraph TD; A-->B;\n```\n\n"
                "```sql\n-- Ghi chú tiếng Việt\nSELECT 1;\n```\n\n"
                "![](missing.png)\n\n![](ok.png)\n",
                encoding="utf-8",
            )
            res = mod.preflight_markdown(bad, engine="pdflatex", resource_paths=[res_dir], fix_lists=False)
            self.assertFalse(res["passed"])
            self.assertTrue(res["has_utf8_code"])
            joined = "\n".join(res["issues"] + res["warnings"])
            self.assertIn("mermaid", joined.lower())
            self.assertIn("missing.png", joined)
            self.assertTrue(any("list" in item.lower() for item in res["issues"]))

            clean = root / "clean.md"
            clean.write_text("# Title\n\nIntro line:\n- item A\n\n![](ok.png)\n", encoding="utf-8")
            res_fix = mod.preflight_markdown(clean, engine="lualatex", resource_paths=[res_dir], fix_lists=True)
            self.assertTrue(res_fix["passed"], f"Expected clean pass after fix_lists, got: {res_fix}")
            self.assertEqual(res_fix["fixed_lists"], 1)
            self.assertIn("Intro line:\n\n- item A", clean.read_text(encoding="utf-8"))

    def test_parse_latex_log_classification_and_thresholds(self) -> None:
        mod = self._import_build_report()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            dirty_log = root / "dirty.log"
            dirty_log.write_text(
                "This is LuaHBTeX\n"
                "! Undefined control sequence.\n"
                "l.42 \\badmacro\n"
                "Overfull \\hbox (14.25pt too wide) in paragraph at lines 55--60\n"
                "Missing character: There is no ệ (U+1EC7) in font Foo!\n"
                "LaTeX Warning: Reference `sec:missing' on page 2 undefined on input line 70.\n"
                "LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right.\n"
                "Output written on report.pdf (5 pages, 12345 bytes).\n",
                encoding="utf-8",
            )
            dirty = mod.parse_latex_log(dirty_log)
            self.assertFalse(dirty["passed"])
            self.assertEqual(dirty["pages"], 5)
            self.assertTrue(dirty["rerun_needed"])
            self.assertEqual(len(dirty["undefined_controls"]), 1)
            self.assertEqual(len(dirty["overfull_hbox"]), 1)
            self.assertEqual(len(dirty["missing_chars"]), 1)
            self.assertEqual(len(dirty["undefined_refs"]), 1)

            clean_log = root / "clean.log"
            clean_log.write_text(
                "Overfull \\hbox (0.65pt too wide) in paragraph at lines 10--12\n"
                "Output written on report.pdf (12 pages, 98765 bytes).\n",
                encoding="utf-8",
            )
            clean = mod.parse_latex_log(clean_log, max_overfull=0, overfull_threshold_pt=1.0)
            self.assertTrue(clean["passed"])
            self.assertEqual(clean["pages"], 12)
            self.assertEqual(clean["overfull_hbox"], [])
            self.assertFalse(clean["rerun_needed"])

    def test_cli_subcommands_preflight_and_audit_log_json(self) -> None:
        script = SCRIPTS_DIR / "build-report.py"
        self.assertTrue(script.is_file(), f"Missing CLI script: {script}")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            md = root / "doc.md"
            md.write_text("# Title\n\nParagraph.\n", encoding="utf-8")
            log = root / "doc.log"
            log.write_text("Output written on doc.pdf (2 pages, 4096 bytes).\n", encoding="utf-8")

            r1 = subprocess.run(
                [sys.executable, str(script), "preflight", str(md), "--json"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(r1.returncode, 0, r1.stderr)
            self.assertTrue(json.loads(r1.stdout)["passed"])

            r2 = subprocess.run(
                [sys.executable, str(script), "audit-log", str(log), "--json"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(r2.returncode, 0, r2.stderr)
            payload = json.loads(r2.stdout)
            self.assertTrue(payload["passed"])
            self.assertEqual(payload["pages"], 2)


class EndToEndBuildTests(unittest.TestCase):
    FIXTURES_DIR = SKILL_ROOT / "tests" / "fixtures"
    BUILD_SCRIPT = SCRIPTS_DIR / "build-report.py"

    def _run_build(self, args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.BUILD_SCRIPT), "build", *args, "--json"],
            cwd=cwd or self.FIXTURES_DIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_e2e_lualatex_vi(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td)
            out_pdf = out_dir / "report-vi.pdf"
            out_tex = out_dir / "report-vi.tex"
            res = self._run_build([
                str(self.FIXTURES_DIR / "sample-vi.md"),
                "--engine",
                "lualatex",
                "--lang",
                "vi",
                "--resource-path",
                str(self.FIXTURES_DIR),
                "--out-pdf",
                str(out_pdf),
                "--out-tex",
                str(out_tex),
            ])
            self.assertEqual(res.returncode, 0, f"LuaLaTeX VI build failed:\n{res.stderr}\n{res.stdout}")
            data = json.loads(res.stdout)
            self.assertTrue(data["passed"], data)
            self.assertEqual(data["engine"], "lualatex")
            self.assertTrue(out_pdf.is_file() and out_pdf.stat().st_size > 5000)
            tex_text = out_tex.read_text(encoding="utf-8")
            self.assertIn(r"\chapter{Tổng quan kiến trúc}", tex_text)
            self.assertIn(r"\appendix", tex_text)

    def test_e2e_xelatex_en_with_citeproc(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td)
            out_pdf = out_dir / "report-en.pdf"
            out_tex = out_dir / "report-en.tex"
            res = self._run_build([
                str(self.FIXTURES_DIR / "sample-en.md"),
                "--engine",
                "xelatex",
                "--lang",
                "en",
                "--bibliography",
                str(self.FIXTURES_DIR / "refs.bib"),
                "--citeproc",
                "--resource-path",
                str(self.FIXTURES_DIR),
                "--out-pdf",
                str(out_pdf),
                "--out-tex",
                str(out_tex),
            ])
            self.assertEqual(res.returncode, 0, f"XeLaTeX EN build failed:\n{res.stderr}\n{res.stdout}")
            data = json.loads(res.stdout)
            self.assertTrue(data["passed"], data)
            self.assertTrue(out_pdf.is_file() and out_pdf.stat().st_size > 5000)
            tex_text = out_tex.read_text(encoding="utf-8")
            self.assertIn("Vaswani", tex_text)

    def test_e2e_pdflatex_vi_code_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td)
            out_pdf = out_dir / "pdflatex-vi.pdf"
            out_tex = out_dir / "pdflatex-vi.tex"
            res = self._run_build([
                str(self.FIXTURES_DIR / "sample-vi.md"),
                "--engine",
                "pdflatex",
                "--lang",
                "vi",
                "--code-verbatim",
                "--resource-path",
                str(self.FIXTURES_DIR),
                "--out-pdf",
                str(out_pdf),
                "--out-tex",
                str(out_tex),
            ])
            self.assertEqual(res.returncode, 0, f"pdfLaTeX VI verbatim fallback failed:\n{res.stderr}\n{res.stdout}")
            data = json.loads(res.stdout)
            self.assertTrue(data["passed"], data)
            self.assertTrue(out_pdf.is_file() and out_pdf.stat().st_size > 5000)
            tex_text = out_tex.read_text(encoding="utf-8")
            self.assertIn(r"\usepackage{fvextra}", tex_text)

    def test_e2e_pdflatex_ascii_listings(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ascii_md = root / "ascii-report.md"
            ascii_md.write_text(
                "---\nlang: en\ntitle: ASCII Engine Benchmark\n---\n\n# 1. Benchmark\n\n```sql\nSELECT 1 AS ok FROM DUAL;\n```\n",
                encoding="utf-8",
            )
            out_pdf = root / "ascii.pdf"
            out_tex = root / "ascii.tex"
            res = self._run_build([
                str(ascii_md),
                "--engine",
                "pdflatex",
                "--lang",
                "en",
                "--out-pdf",
                str(out_pdf),
                "--out-tex",
                str(out_tex),
            ], cwd=root)
            self.assertEqual(res.returncode, 0, f"pdfLaTeX ASCII listings failed:\n{res.stderr}\n{res.stdout}")
            data = json.loads(res.stdout)
            self.assertTrue(data["passed"], data)
            self.assertTrue(out_pdf.is_file() and out_pdf.stat().st_size > 3000)
            self.assertIn(r"\begin{lstlisting}[language=SQL]", out_tex.read_text(encoding="utf-8"))

    def test_e2e_multifile_dir_citeproc_and_broken_preflight_gate(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td)
            out_pdf = out_dir / "multi.pdf"
            res = self._run_build([
                "--dir",
                str(self.FIXTURES_DIR / "chapters"),
                "--engine",
                "lualatex",
                "--lang",
                "en",
                "--bibliography",
                str(self.FIXTURES_DIR / "refs.bib"),
                "--citeproc",
                "--out-pdf",
                str(out_pdf),
            ])
            self.assertEqual(res.returncode, 0, f"Multi-file citeproc build failed:\n{res.stderr}\n{res.stdout}")
            data = json.loads(res.stdout)
            self.assertTrue(data["passed"], data)
            self.assertTrue(out_pdf.is_file() and out_pdf.stat().st_size > 3000)

            broken_pdf = out_dir / "broken.pdf"
            bad_res = self._run_build([
                str(self.FIXTURES_DIR / "sample-broken.md"),
                "--engine",
                "lualatex",
                "--out-pdf",
                str(broken_pdf),
            ])
            self.assertNotEqual(bad_res.returncode, 0)
            self.assertFalse(broken_pdf.exists())


class RegressionFixesTests(unittest.TestCase):
    FIXTURES_DIR = SKILL_ROOT / "tests" / "fixtures"
    BUILD_SCRIPT = SCRIPTS_DIR / "build-report.py"

    def _run_lua(self, md_text: str, meta: dict | None = None, cwd: Path | None = None) -> str:
        lua_filter = SCRIPTS_DIR / "report-prep.lua"
        with tempfile.TemporaryDirectory() as td:
            md_path = Path(td) / "input.md"
            md_path.write_text(md_text, encoding="utf-8")
            cmd = [
                "pandoc",
                str(md_path),
                "--from=markdown",
                "--to=latex",
                "--top-level-division=chapter",
                f"--lua-filter={lua_filter}",
                "--wrap=none",
            ]
            if meta is not None:
                meta_path = Path(td) / "meta.json"
                meta_path.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                cmd.append(f"--metadata-file={meta_path}")
            res = subprocess.run(cmd, cwd=cwd or Path(td), capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(res.returncode, 0, res.stderr)
            return res.stdout

    def _run_build(self, args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.BUILD_SCRIPT), "build", *args, "--json"],
            cwd=cwd or self.FIXTURES_DIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_lua_utf8_dashes_caps_nested_headers_and_caption_guard(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "arch.png").write_bytes(b"png")
            md = (
                "# Cover Title\n\n"
                "> Subtitle info\n\n"
                "## 1. Overview with **`nested_id`** and `a~b^c`\n\n"
                "![](arch.png)\n\n"
                "*HÌNH 1 – Kiến trúc chính*\n\n"
                "![](arch.png)\n\n"
                "*Note: measured locally.*\n\n"
                "| A | B |\n| --- | --- |\n| Top | Line1<BR>Line2 |\n\n"
                "# Appendix A — SQL Scripts\n"
            )
            out = self._run_lua(
                md,
                {"prep": {"strip-cover": "first-h1-cover", "adaptive-tables": False}},
                cwd=root,
            )
            self.assertIn(r"\chapter{\texorpdfstring{Overview", out)
            self.assertEqual(out.count(r"\texorpdfstring"), 1)
            self.assertIn(r"\textbf{\texttt{nested\_\allowbreak{}id}}", out)
            self.assertIn(r"Overview with nested\_id", out)
            self.assertIn(r"\textasciitilde", out)
            self.assertIn(r"\caption{Kiến trúc chính}", out)
            self.assertNotIn(r"\caption{Note: measured locally.}", out)
            self.assertIn(r"\emph{Note: measured locally.}", out)
            self.assertIn(r"\newline", out)
            self.assertNotIn(r"\footnotesize", out)
            self.assertIn(r"\chapter{SQL Scripts}", out)

    def test_preflight_wrapped_list_inline_code_math_pipe_and_dir_exclusion(self) -> None:
        import importlib.util

        spec = importlib.util.spec_from_file_location("build_report", self.BUILD_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "README.md").write_text("# Ignore README\n", encoding="utf-8")
            (root / "INDEX.md").write_text("# Ignore INDEX\n", encoding="utf-8")
            (root / "01-body.md").write_text(
                "# Body\n\n"
                "- Item one\n  wrapped continuation line\n- Item two\n\n"
                "Example markdown syntax `` `![alt](missing_in_code.png)` `` stays ignored.\n\n"
                "| Col1 | Col2 |\n| --- | --- |\n| Norm | $|a | b|$ |\n",
                encoding="utf-8",
            )
            assembled = root / "assembled.md"
            mod.assemble_markdown(None, None, root, assembled)
            atxt = assembled.read_text(encoding="utf-8")
            self.assertNotIn("Ignore README", atxt)
            self.assertNotIn("Ignore INDEX", atxt)

            res = mod.preflight_markdown(root / "01-body.md", engine="lualatex", fix_lists=False)
            joined = "\n".join(res["issues"])
            self.assertNotIn("missing_in_code.png", joined)
            self.assertNotIn("tight list", joined.lower())
            self.assertFalse(res["passed"])
            self.assertTrue(any("table" in x.lower() or "pipe" in x.lower() for x in res["issues"]))

    def test_parse_latex_log_rerun_and_wrapped_warnings(self) -> None:
        import importlib.util

        spec = importlib.util.spec_from_file_location("build_report", self.BUILD_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        with tempfile.TemporaryDirectory() as td:
            log_file = Path(td) / "wrapped.log"
            log_file.write_text(
                "LaTeX Warning: Reference `sec:very_long_section_identifier_here' on page 3 und\nefined on input line 99.\n"
                "Package biblatex Warning: Please (re)run Biber on the file:\n"
                "(biblatex)                Please rerun LaTeX.\n"
                "Output written on report.pdf (4 pages, 50000 bytes).\n",
                encoding="utf-8",
            )
            parsed = mod.parse_latex_log(log_file)
            self.assertTrue(parsed["rerun_needed"])
            self.assertEqual(len(parsed["undefined_refs"]), 1)
            self.assertFalse(parsed["passed"])

    def test_e2e_defaults_preset_no_double_concat_and_same_workdir_outpdf(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "build"
            out_dir.mkdir()
            out_pdf = out_dir / "report.pdf"
            out_tex = out_dir / "report.tex"
            res = self._run_build([
                "--dir",
                str(self.FIXTURES_DIR / "chapters"),
                "--defaults",
                str(PRESETS_DIR / "defaults-xelatex.yaml"),
                "--engine",
                "xelatex",
                "--lang",
                "en",
                "--cover-style",
                "boxed",
                "--compact-toc",
                "--bibliography",
                str(self.FIXTURES_DIR / "refs.bib"),
                "--citeproc",
                "--resource-path",
                str(self.FIXTURES_DIR),
                "--work-dir",
                str(out_dir),
                "--out-tex",
                str(out_tex),
                "--out-pdf",
                str(out_pdf),
            ])
            self.assertEqual(res.returncode, 0, f"Preset/work-dir collision failed:\n{res.stderr}\n{res.stdout}")
            data = json.loads(res.stdout)
            self.assertTrue(data["passed"], data)
            tex = out_tex.read_text(encoding="utf-8")
            self.assertIn(r"\newcommand{\reportlang}{en}", tex)
            self.assertNotIn("enen", tex)
            self.assertIn(r"\newcommand{\coverstyle}{boxed}", tex)
            self.assertNotIn("boxedboxed", tex)
            self.assertTrue(out_pdf.is_file() and out_pdf.stat().st_size > 5000)

    def test_e2e_pdflatex_auto_verbatim_and_vi_chapter_heading_and_article_class(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td)
            out_pdf = out_dir / "pdflatex-auto.pdf"
            out_tex = out_dir / "pdflatex-auto.tex"
            res = self._run_build([
                str(self.FIXTURES_DIR / "sample-vi.md"),
                "--engine",
                "pdflatex",
                "--lang",
                "vi",
                "--resource-path",
                str(self.FIXTURES_DIR),
                "--out-pdf",
                str(out_pdf),
                "--out-tex",
                str(out_tex),
            ])
            self.assertEqual(res.returncode, 0, f"pdfLaTeX auto-verbatim failed:\n{res.stderr}\n{res.stdout}")
            data = json.loads(res.stdout)
            self.assertTrue(data["passed"], data)
            tex = out_tex.read_text(encoding="utf-8")
            self.assertIn(r"\selectlanguage{vietnamese}", tex)
            self.assertIn(r"\renewcommand{\chaptername}{\chapternameword}", tex)

            art_pdf = out_dir / "article.pdf"
            art_tex = out_dir / "article.tex"
            art_res = self._run_build([
                str(self.FIXTURES_DIR / "sample-en.md"),
                "--engine",
                "lualatex",
                "--documentclass",
                "article",
                "--resource-path",
                str(self.FIXTURES_DIR),
                "--out-pdf",
                str(art_pdf),
                "--out-tex",
                str(art_tex),
            ])
            self.assertEqual(art_res.returncode, 0, f"Article documentclass failed:\n{art_res.stderr}\n{art_res.stdout}")
            self.assertTrue(json.loads(art_res.stdout)["passed"])
            at = art_tex.read_text(encoding="utf-8")
            self.assertIn(r"\documentclass[a4paper,12pt]{article}", at)
            self.assertNotIn(r"\chapter{", at)

    def test_e2e_biblatex_and_natbib_with_spaces_in_path(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            bib_dir = root / "ref dir with spaces"
            bib_dir.mkdir()
            bib_path = bib_dir / "my refs.bib"
            shutil.copy2(self.FIXTURES_DIR / "refs.bib", bib_path)

            md = root / "doc.md"
            md.write_text("# Overview\n\nWork builds on classical typesetting [@knuth1984].\n", encoding="utf-8")

            if shutil.which("biber"):
                p1 = root / "biblatex.pdf"
                t1 = root / "biblatex.tex"
                r1 = self._run_build([
                    str(md),
                    "--engine",
                    "lualatex",
                    "--bibliography",
                    str(bib_path),
                    "--biblatex",
                    "--out-pdf",
                    str(p1),
                    "--out-tex",
                    str(t1),
                ], cwd=root)
                self.assertEqual(r1.returncode, 0, f"biblatex build failed:\n{r1.stderr}\n{r1.stdout}")
                self.assertTrue(json.loads(r1.stdout)["passed"])
                self.assertIn(r"\printbibliography", t1.read_text(encoding="utf-8"))

            if shutil.which("bibtex"):
                p2 = root / "natbib.pdf"
                t2 = root / "natbib.tex"
                r2 = self._run_build([
                    str(md),
                    "--engine",
                    "pdflatex",
                    "--bibliography",
                    str(bib_path),
                    "--natbib",
                    "--out-pdf",
                    str(p2),
                    "--out-tex",
                    str(t2),
                ], cwd=root)
                self.assertEqual(r2.returncode, 0, f"natbib build failed:\n{r2.stderr}\n{r2.stdout}")
                self.assertTrue(json.loads(r2.stdout)["passed"])
                self.assertIn(r"\bibliography{", t2.read_text(encoding="utf-8"))


class DynamicAdaptationTests(unittest.TestCase):
    FIXTURES_DIR = SKILL_ROOT / "tests" / "fixtures"
    BUILD_SCRIPT = SCRIPTS_DIR / "build-report.py"

    def test_inspect_markdown_profiles_and_decision_points(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            memo = root / "memo.md"
            memo.write_text("# Quick Note\n\nSimple note.\n\n## Next Steps\n\nDone.\n", encoding="utf-8")

            r_memo = subprocess.run(
                [sys.executable, str(self.BUILD_SCRIPT), "inspect", str(memo), "--json"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(r_memo.returncode, 0, r_memo.stderr)
            d_memo = json.loads(r_memo.stdout)
            self.assertEqual(d_memo["detected_lang"], "en")
            self.assertEqual(d_memo["recommended_options"]["documentclass"], "article")
            self.assertFalse(d_memo["recommended_options"]["toc"])
            self.assertTrue(len(d_memo["decision_points"]) >= 2)

            vi_complex = root / "vi_complex.md"
            vi_complex.write_text(
                "**HỌC VIỆN CÔNG NGHỆ**\n\nNhóm 01\n\n"
                "# 1. Tổng quan hệ thống\n\n"
                "Tham khảo tài liệu [@vaswani2017].\n\n"
                "> [!NOTE]\n> Ghi chú hệ thống.\n\n"
                "| A | B | C | D | E | F |\n| --- | --- | --- | --- | --- | --- |\n| 1 | 2<br>3 | 4 | 5 | 6 | 7 |\n\n"
                "```python\n# Bình luận tiếng Việt\nprint(1)\n```\n\n"
                "# Phụ lục A: Mã nguồn\n",
                encoding="utf-8",
            )
            r_vi = subprocess.run(
                [sys.executable, str(self.BUILD_SCRIPT), "inspect", str(vi_complex), "--json"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(r_vi.returncode, 0, r_vi.stderr)
            d_vi = json.loads(r_vi.stdout)
            self.assertEqual(d_vi["detected_lang"], "vi")
            self.assertTrue(d_vi["cover_signals"]["has_pre_h1_prose"])
            self.assertEqual(d_vi["tables"]["max_cols"], 6)
            self.assertTrue(d_vi["tables"]["has_html_br"])
            self.assertGreaterEqual(d_vi["headings"]["numbered_count"], 1)
            self.assertEqual(d_vi["headings"]["appendix_count"], 1)
            self.assertTrue(d_vi["code"]["has_utf8_code"])
            self.assertEqual(d_vi["citations"]["inline_cite_count"], 1)
            self.assertEqual(d_vi["callouts"]["count"], 1)
            self.assertEqual(d_vi["recommended_options"]["documentclass"], "report")
            self.assertEqual(d_vi["recommended_options"]["strip_cover"], "before-first-h1")
            self.assertEqual(d_vi["recommended_options"]["engine"], "lualatex")

    def test_build_dynamic_flags_no_toc_article_var_meta_prep_and_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            fm_doc = root / "fm_article.md"
            fm_doc.write_text(
                "---\ndocumentclass: article\ntoc: false\ncover-style: none\nlang: en\ntitle: Short Note\n---\n\n"
                "# Introduction\n\nBody paragraph.\n",
                encoding="utf-8",
            )
            pdf_fm = root / "fm.pdf"
            tex_fm = root / "fm.tex"
            r_fm = subprocess.run(
                [
                    sys.executable,
                    str(self.BUILD_SCRIPT),
                    "build",
                    str(fm_doc),
                    "--engine",
                    "xelatex",
                    "--out-pdf",
                    str(pdf_fm),
                    "--out-tex",
                    str(tex_fm),
                    "--json",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(r_fm.returncode, 0, f"{r_fm.stderr}\n{r_fm.stdout}")
            fm_data = json.loads(r_fm.stdout)
            self.assertTrue(fm_data["passed"])
            self.assertEqual(fm_data["log_audit"]["pages"], 1)
            tex_fm_txt = tex_fm.read_text(encoding="utf-8")
            self.assertIn(r"\documentclass[a4paper,12pt]{article}", tex_fm_txt)
            self.assertIn(r"\newcommand{\coverstyle}{none}", tex_fm_txt)
            self.assertNotIn(r"\tableofcontents", tex_fm_txt)

            pdf_dyn = root / "dyn.pdf"
            tex_dyn = root / "dyn.tex"
            r_dyn = subprocess.run(
                [
                    sys.executable,
                    str(self.BUILD_SCRIPT),
                    "build",
                    str(self.FIXTURES_DIR / "sample-en.md"),
                    "--engine",
                    "lualatex",
                    "--no-toc",
                    "--cover-style",
                    "minimal",
                    "--no-strip-heading-numbers",
                    "--no-adaptive-tables",
                    "--no-number-sections",
                    "--var",
                    "accent-color-rgb=120,20,20",
                    "--meta",
                    "subtitle=CustomDynamicSubtitle",
                    "--prep",
                    "callout-boxes=false",
                    "--bibliography",
                    str(self.FIXTURES_DIR / "refs.bib"),
                    "--citeproc",
                    "--resource-path",
                    str(self.FIXTURES_DIR),
                    "--out-pdf",
                    str(pdf_dyn),
                    "--out-tex",
                    str(tex_dyn),
                    "--json",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(r_dyn.returncode, 0, f"{r_dyn.stderr}\n{r_dyn.stdout}")
            self.assertTrue(json.loads(r_dyn.stdout)["passed"])
            tex_dyn_txt = tex_dyn.read_text(encoding="utf-8")
            self.assertNotIn(r"\tableofcontents", tex_dyn_txt)
            self.assertIn(r"\definecolor{ptitblue}{RGB}{120,20,20}", tex_dyn_txt)
            self.assertIn("CustomDynamicSubtitle", tex_dyn_txt)
            self.assertIn(r"\setcounter{secnumdepth}{-1}", tex_dyn_txt)
            self.assertIn(r"\chapter{1. System Overview}", tex_dyn_txt)
            self.assertNotIn(r"\begin{reportcallout}", tex_dyn_txt)
            self.assertNotIn(r"{\scriptsize", tex_dyn_txt)


if __name__ == "__main__":
    unittest.main()
