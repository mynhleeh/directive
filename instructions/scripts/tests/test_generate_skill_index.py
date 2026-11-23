"""Unit tests for instructions/scripts/generate_skill_index.py."""

import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import instructions.scripts.generate_skill_index as gsi


class TestParseFrontmatter(unittest.TestCase):
    def test_single_line_unquoted(self):
        text = "---\nname: my-skill\ndescription: Simple single line description\n---\n# Body\n"
        name, desc = gsi.parse_frontmatter(text)
        self.assertEqual(name, "my-skill")
        self.assertEqual(desc, "Simple single line description")

    def test_single_line_quoted(self):
        text = '---\nname: "quoted-skill"\ndescription: "Quoted description with spaces"\n---\n'
        name, desc = gsi.parse_frontmatter(text)
        self.assertEqual(name, "quoted-skill")
        self.assertEqual(desc, "Quoted description with spaces")

    def test_block_scalar_gt(self):
        text = "---\nname: block-skill\ndescription: >\n  First line of block\n  second line of block\nversion: 1.0\n---\n"
        name, desc = gsi.parse_frontmatter(text)
        self.assertEqual(name, "block-skill")
        self.assertEqual(desc, "First line of block second line of block")

    def test_block_scalar_pipe(self):
        text = "---\nname: pipe-skill\ndescription: |\n  Line 1\n  Line 2\n---\n"
        name, desc = gsi.parse_frontmatter(text)
        self.assertEqual(name, "pipe-skill")
        self.assertEqual(desc, "Line 1 Line 2")

    def test_fallback_to_body_paragraph(self):
        text = "---\nname: no-desc-skill\nversion: 1.0\n---\n# Heading\n\nThis is the first body paragraph.\nIt continues here.\n\nSecond paragraph."
        name, desc = gsi.parse_frontmatter(text)
        self.assertEqual(name, "no-desc-skill")
        self.assertEqual(desc, "This is the first body paragraph. It continues here.")

    def test_no_frontmatter(self):
        text = "# Just markdown without frontmatter\nSome content."
        name, desc = gsi.parse_frontmatter(text)
        self.assertIsNone(name)
        self.assertIsNone(desc)


class TestCleanDescription(unittest.TestCase):
    def test_unicode_arrows(self):
        self.assertEqual(gsi.clean_description("Step 1 → Step 2 ⇒ Step 3"), "Step 1 -> Step 2 -> Step 3")

    def test_dashes(self):
        self.assertEqual(gsi.clean_description("A — B – C"), "A - B - C")

    def test_pipe_escaping(self):
        self.assertEqual(gsi.clean_description("Option A | Option B"), r"Option A \| Option B")
        # Ensure already escaped pipe is not double escaped
        self.assertEqual(gsi.clean_description(r"Option A \| Option B"), r"Option A \| Option B")

    def test_whitespace_collapsing(self):
        self.assertEqual(gsi.clean_description("Multiple   spaces\tand\n\nnewlines"), "Multiple spaces and newlines")

    def test_trailing_backslash(self):
        cleaned = gsi.clean_description("Ending with backslash\\")
        self.assertFalse(cleaned.endswith("\\"))


class TestUnregisteredSourceGuard(unittest.TestCase):
    def test_unknown_source_raises_error(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            active_dir = tmp_path / "active"
            external_dir = tmp_path / "external"
            skills_root = tmp_path

            # Create an unregistered external source
            alien_skill = external_dir / "alien-repo" / "skills" / "alien-skill"
            alien_skill.mkdir(parents=True)
            (alien_skill / "SKILL.md").write_text("---\nname: alien\ndescription: Alien\n---\n", encoding="utf-8")

            with self.assertRaises(ValueError) as ctx:
                gsi.generate_index_content(active_dir, external_dir, skills_root)
            self.assertIn("Unregistered skill source(s) discovered", str(ctx.exception))
            self.assertIn("alien-repo", str(ctx.exception))


class TestCheckDriftDetection(unittest.TestCase):
    def test_check_passes_when_matching(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            out_file = tmp_path / "SKILL_INDEX.md"

            # Mock generate_index_content to return fixed text
            with patch("instructions.scripts.generate_skill_index.generate_index_content", return_value="EXPECTED\n"):
                out_file.write_text("EXPECTED\n", encoding="utf-8", newline="\n")
                with patch("sys.argv", ["generate_skill_index.py", "--check", "--output", str(out_file)]):
                    with patch("sys.stdout", new_callable=io.StringIO):
                        rc = gsi.main()
                        self.assertEqual(rc, 0)

    def test_check_fails_when_stale(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            out_file = tmp_path / "SKILL_INDEX.md"

            with patch("instructions.scripts.generate_skill_index.generate_index_content", return_value="NEW\n"):
                out_file.write_text("OLD\n", encoding="utf-8")
                with patch("sys.argv", ["generate_skill_index.py", "--check", "--output", str(out_file)]):
                    with patch("sys.stdout", new_callable=io.StringIO):
                        rc = gsi.main()
                        self.assertEqual(rc, 1)

    def test_check_fails_when_file_missing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            out_file = tmp_path / "NON_EXISTENT.md"

            with patch("instructions.scripts.generate_skill_index.generate_index_content", return_value="NEW\n"):
                with patch("sys.argv", ["generate_skill_index.py", "--check", "--output", str(out_file)]):
                    with patch("sys.stdout", new_callable=io.StringIO):
                        rc = gsi.main()
                        self.assertEqual(rc, 1)


class TestCollisionPrefixParity(unittest.TestCase):
    def test_prefixes(self):
        self.assertEqual(gsi.extract_skills.make_prefix("active"), "own")
        self.assertEqual(gsi.extract_skills.make_prefix("AI-Research-SKILLs"), "ars")
        self.assertEqual(gsi.extract_skills.make_prefix("Auto-Empirical-Research-Skills"), "aers")
        self.assertEqual(gsi.extract_skills.make_prefix("scientific-agent-skills"), "sas")
        self.assertEqual(gsi.extract_skills.make_prefix("superpowers"), "sup")
        self.assertEqual(gsi.extract_skills.make_prefix("ui-ux-pro-max-skill"), "uupms")
        self.assertEqual(gsi.extract_skills.make_prefix("orca"), "orc")
        self.assertEqual(gsi.extract_skills.make_prefix("anthropics"), "ant")

    def test_build_skill_name(self):
        # Unique name
        self.assertEqual(gsi.extract_skills.build_skill_name("active", "commit", False), "commit")
        # Duplicate name
        self.assertEqual(gsi.extract_skills.build_skill_name("active", "commit", True), "own-commit")
        self.assertEqual(gsi.extract_skills.build_skill_name("AI-Research-SKILLs", "paper", True), "ars-paper")


class TestGeneratedFormat(unittest.TestCase):
    def test_minimal_catalog_format(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            active_dir = tmp_path / "active"
            external_dir = tmp_path / "external"
            skill_b = active_dir / "zeta-skill"
            skill_a = active_dir / "alpha-skill"
            skill_b.mkdir(parents=True)
            skill_a.mkdir(parents=True)
            (skill_b / "SKILL.md").write_text("---\nname: zeta-skill\ndescription: Zeta desc\n---\n", encoding="utf-8")
            (skill_a / "SKILL.md").write_text("---\nname: alpha-skill\ndescription: Alpha desc\n---\n", encoding="utf-8")

            out = gsi.generate_index_content(active_dir, external_dir, tmp_path)
            self.assertNotIn("For human developers:", out)
            self.assertNotIn("For AI agents:", out)
            self.assertNotIn("Exported ID", out)
            self.assertIn("| # | Skill | Description |", out)
            # Alphabetical order inside source
            idx_a = out.index("[alpha-skill]")
            idx_b = out.index("[zeta-skill]")
            self.assertLess(idx_a, idx_b)


if __name__ == "__main__":
    unittest.main()
