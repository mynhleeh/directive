# directive-cli Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an interactive CLI/TUI tool in `directive-cli/` to discover, select, and scaffold agent configurations, rules, and skills into a targeted `.agents/` directory (defaulting to `directive-cli/output/`), featuring automatic Git submodule synchronization with offline resilience and interactive submodule management.

**Architecture:** A modular Python application cleanly separating `core/` (data models, filesystem scanner, conflict resolver/exporter, git manager) and `ui/` (Rich display, questionary interactive prompts), orchestrated by `main.py`. The legacy script `instructions/scripts/extract_skills.py` remains completely untouched.

**Tech Stack:** Python 3.10+, `rich>=13.0.0`, `questionary>=2.0.0`, `pytest>=7.0.0`

**Spec:** [docs/superpowers/specs/2026-09-16-directive-cli-design.md](file:///C:/Personal%20Files/repos/directive/docs/superpowers/specs/2026-09-16-directive-cli-design.md)

## Global Constraints
- Target output default: `directive-cli/output/` (creates `.agents/` inside it); custom path provided by user overrides this default.
- Keep `instructions/scripts/extract_skills.py` completely unmodified.
- All code for this tool resides in `directive-cli/` at the repository root.
- All work and commits must be on branch `cli-tool`.
- Use `pathlib.Path` and UTF-8 encoding for cross-platform Windows and Unix compatibility.
- Prefix duplicate skill names deterministically using `make_prefix` (`own-<name>` for active, abbreviated source group prefix for external submodules).
- Submodule synchronization must not block or crash if network/git fails; fallback gracefully to offline cached data.

---

### Task 1: Foundation, Data Models & Configuration

**Files:**
- Create: `directive-cli/__init__.py`
- Create: `directive-cli/requirements.txt`
- Create: `directive-cli/config.py`
- Create: `directive-cli/core/__init__.py`
- Create: `directive-cli/core/models.py`
- Create: `directive-cli/tests/__init__.py`
- Test: `directive-cli/tests/test_models.py`

**Interfaces:**
- Produces:
  - `config.DEFAULT_OUTPUT_DIR: Path`
  - `config.DEFAULT_AGENTS_SOURCE: Path`
  - `config.DEFAULT_RULES_SOURCE: Path`
  - `config.DEFAULT_SKILLS_ACTIVE: Path`
  - `config.DEFAULT_SKILLS_EXTERNAL: Path`
  - `models.AgentItem(name: str, source_path: Path, description: str)`
  - `models.RuleItem(name: str, source_path: Path, filename: str)`
  - `models.SkillItem(source_group: str, name: str, source_path: Path, export_name: str)`
  - `models.SkillGroup(name: str, raw_name: str, is_active: bool, skills: List[SkillItem])`

- [ ] **Step 1: Write the failing test for data models and configuration**

```python
# directive-cli/tests/test_models.py
from pathlib import Path
from directive_cli.core.models import AgentItem, RuleItem, SkillItem, SkillGroup
from directive_cli import config


def test_models_instantiation():
    agent = AgentItem(name="omni", source_path=Path("instructions/agents/omni"), description="Omni agent")
    assert agent.name == "omni"
    assert agent.description == "Omni agent"

    rule = RuleItem(name="file-org", source_path=Path("instructions/rules/rule.md"), filename="rule.md")
    assert rule.name == "file-org"
    assert rule.filename == "rule.md"

    skill = SkillItem(source_group="active", name="git-workflow", source_path=Path("active/git-workflow"))
    assert skill.export_name == ""
    assert skill.source_group == "active"

    group = SkillGroup(name="active (own)", raw_name="active", is_active=True, skills=[skill])
    assert len(group.skills) == 1
    assert group.is_active is True


def test_config_paths_exist_as_paths():
    assert isinstance(config.DEFAULT_OUTPUT_DIR, Path)
    assert config.DEFAULT_OUTPUT_DIR.name == "output"
    assert isinstance(config.DEFAULT_AGENTS_SOURCE, Path)
    assert isinstance(config.DEFAULT_RULES_SOURCE, Path)
    assert isinstance(config.DEFAULT_SKILLS_ACTIVE, Path)
    assert isinstance(config.DEFAULT_SKILLS_EXTERNAL, Path)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest directive-cli/tests/test_models.py -v`  
Expected: FAIL (ModuleNotFoundError: No module named 'directive_cli')

- [ ] **Step 3: Implement minimal code for requirements, config, and models**

```python
# directive-cli/__init__.py
"""Directive CLI package."""
__version__ = "0.1.0"
```

```text
# directive-cli/requirements.txt
rich>=13.0.0
questionary>=2.0.0
pytest>=7.0.0
```

```python
# directive-cli/config.py
from pathlib import Path

# Base repository root
REPO_ROOT = Path(__file__).resolve().parent.parent

# Default Source Directories
DEFAULT_AGENTS_SOURCE = REPO_ROOT / "instructions" / "agents"
DEFAULT_RULES_SOURCE = REPO_ROOT / "instructions" / "rules"
DEFAULT_SKILLS_ACTIVE = REPO_ROOT / "instructions" / "skills" / "active"
DEFAULT_SKILLS_EXTERNAL = REPO_ROOT / "instructions" / "skills" / "external"

# Default Output Directory (directive-cli/output/)
DEFAULT_OUTPUT_DIR = REPO_ROOT / "directive-cli" / "output"

# Git settings
SUBMODULE_TIMEOUT_SECONDS = 15
```

```python
# directive-cli/core/__init__.py
"""Core logic package."""
```

```python
# directive-cli/core/models.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class AgentItem:
    name: str
    source_path: Path
    description: str = ""


@dataclass
class RuleItem:
    name: str
    source_path: Path
    filename: str


@dataclass
class SkillItem:
    source_group: str
    name: str
    source_path: Path
    export_name: str = ""


@dataclass
class SkillGroup:
    name: str
    raw_name: str
    is_active: bool
    skills: List[SkillItem] = field(default_factory=list)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest directive-cli/tests/test_models.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add directive-cli/
git commit -m "feat(directive-cli): initialize models, config, and requirements"
```

---

### Task 2: Filesystem Scanner (`core/scanner.py`)

**Files:**
- Create: `directive-cli/core/scanner.py`
- Test: `directive-cli/tests/test_scanner.py`

**Interfaces:**
- Consumes:
  - `directive_cli.core.models.{AgentItem, RuleItem, SkillItem, SkillGroup}`
- Produces:
  - `scan_agents(base_dir: Path) -> List[AgentItem]`
  - `scan_rules(base_dir: Path) -> List[RuleItem]`
  - `scan_skills(active_dir: Path, external_dir: Path) -> List[SkillGroup]`

- [ ] **Step 1: Write the failing test for scanner**

```python
# directive-cli/tests/test_scanner.py
from pathlib import Path
import pytest
from directive_cli.core.scanner import scan_agents, scan_rules, scan_skills


@pytest.fixture
def mock_instructions(tmp_path):
    # Setup agents
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()
    agent_a = agents_dir / "agent-a"
    agent_a.mkdir()
    (agent_a / "agent.md").write_text("# Agent A\nDescription for A", encoding="utf-8")

    # Setup rules
    rules_dir = tmp_path / "rules"
    rules_dir.mkdir()
    (rules_dir / "format.rule.md").write_text("# Formatting rule", encoding="utf-8")

    # Setup skills active
    skills_active = tmp_path / "skills" / "active"
    skills_active.mkdir(parents=True)
    my_skill = skills_active / "my-skill"
    my_skill.mkdir()
    (my_skill / "SKILL.md").write_text("---\nname: my-skill\n---", encoding="utf-8")

    # Setup skills external submodule
    skills_ext = tmp_path / "skills" / "external"
    sub1 = skills_ext / "sub1"
    sub1.mkdir(parents=True)
    sub1_skill = sub1 / "nested" / "ext-skill"
    sub1_skill.mkdir(parents=True)
    (sub1_skill / "SKILL.md").write_text("---\nname: ext-skill\n---", encoding="utf-8")

    return agents_dir, rules_dir, skills_active, skills_ext


def test_scanner_functions(mock_instructions):
    agents_dir, rules_dir, skills_active, skills_ext = mock_instructions

    # Test scan_agents
    agents = scan_agents(agents_dir)
    assert len(agents) == 1
    assert agents[0].name == "agent-a"
    assert "Description for A" in agents[0].description

    # Test scan_rules
    rules = scan_rules(rules_dir)
    assert len(rules) == 1
    assert rules[0].filename == "format.rule.md"
    assert rules[0].name == "format"

    # Test scan_skills
    groups = scan_skills(skills_active, skills_ext)
    assert len(groups) == 2

    # Group 1: active
    active_group = next(g for g in groups if g.is_active)
    assert active_group.raw_name == "active"
    assert len(active_group.skills) == 1
    assert active_group.skills[0].name == "my-skill"

    # Group 2: sub1
    sub1_group = next(g for g in groups if not g.is_active)
    assert sub1_group.raw_name == "sub1"
    assert len(sub1_group.skills) == 1
    assert sub1_group.skills[0].name == "ext-skill"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest directive-cli/tests/test_scanner.py -v`  
Expected: FAIL (ImportError: cannot import name 'scan_agents' from 'directive_cli.core.scanner')

- [ ] **Step 3: Implement minimal scanner code**

```python
# directive-cli/core/scanner.py
import os
import re
from pathlib import Path
from typing import List
from directive_cli.core.models import AgentItem, RuleItem, SkillItem, SkillGroup


def _extract_description_from_file(file_path: Path) -> str:
    """Extract first non-heading sentence or prompt excerpt."""
    if not file_path.is_file():
        return ""
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        for line in content.splitlines():
            line_clean = line.strip()
            if not line_clean or line_clean.startswith("#") or line_clean.startswith("---"):
                continue
            if line_clean.startswith("description:"):
                return line_clean.replace("description:", "").strip().strip('"\'')
            return line_clean[:100]
    except Exception:
        pass
    return ""


def scan_agents(base_dir: Path) -> List[AgentItem]:
    """Scan instructions/agents directory for agent packages."""
    agents: List[AgentItem] = []
    if not base_dir.is_dir():
        return agents

    for child in sorted(base_dir.iterdir()):
        if child.is_dir():
            agent_file = child / "agent.md"
            desc = _extract_description_from_file(agent_file) if agent_file.exists() else ""
            agents.append(AgentItem(name=child.name, source_path=child, description=desc))
    return agents


def scan_rules(base_dir: Path) -> List[RuleItem]:
    """Scan instructions/rules directory for *.rule.md or *.md files."""
    rules: List[RuleItem] = []
    if not base_dir.is_dir():
        return rules

    for child in sorted(base_dir.iterdir()):
        if child.is_file() and child.name.endswith(".md"):
            clean_name = re.sub(r"\.rule\.md$", "", child.name)
            clean_name = re.sub(r"\.md$", "", clean_name)
            rules.append(RuleItem(name=clean_name, source_path=child, filename=child.name))
    return rules


def _scan_submodule_skills(sub_dir: Path) -> List[SkillItem]:
    """Scan a single external submodule directory for folders containing SKILL.md."""
    skills: List[SkillItem] = []
    seen = set()
    if not sub_dir.is_dir():
        return skills

    for root, _, files in os.walk(sub_dir):
        if "SKILL.md" in files:
            current = Path(root)
            skill_name = sub_dir.name if current == sub_dir else current.name
            if skill_name in seen:
                continue
            seen.add(skill_name)
            skills.append(
                SkillItem(
                    source_group=sub_dir.name,
                    name=skill_name,
                    source_path=current,
                )
            )
    return skills


def scan_skills(active_dir: Path, external_dir: Path) -> List[SkillGroup]:
    """Scan active skills and external submodule skills."""
    groups: List[SkillGroup] = []

    # 1. Active skills
    if active_dir.is_dir():
        active_skills: List[SkillItem] = []
        for child in sorted(active_dir.iterdir()):
            if child.is_dir() and (child / "SKILL.md").exists():
                active_skills.append(
                    SkillItem(
                        source_group="active",
                        name=child.name,
                        source_path=child,
                    )
                )
        groups.append(
            SkillGroup(
                name="active (own)",
                raw_name="active",
                is_active=True,
                skills=active_skills,
            )
        )

    # 2. External submodules
    if external_dir.is_dir():
        for sub in sorted(external_dir.iterdir()):
            if sub.is_dir():
                sub_skills = _scan_submodule_skills(sub)
                groups.append(
                    SkillGroup(
                        name=sub.name,
                        raw_name=sub.name,
                        is_active=False,
                        skills=sub_skills,
                    )
                )

    return groups
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest directive-cli/tests/test_scanner.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add directive-cli/core/scanner.py directive-cli/tests/test_scanner.py
git commit -m "feat(directive-cli): implement filesystem scanner for agents, rules, and skills"
```

---

### Task 3: Exporter & Conflict Resolver (`core/exporter.py`)

**Files:**
- Create: `directive-cli/core/exporter.py`
- Test: `directive-cli/tests/test_exporter.py`

**Interfaces:**
- Consumes:
  - `directive_cli.core.models.{AgentItem, RuleItem, SkillItem}`
- Produces:
  - `make_prefix(name: str) -> str`
  - `resolve_skill_names(skills: List[SkillItem]) -> List[SkillItem]`
  - `resolve_target_directory(target_path: Path) -> Path`
  - `export_scaffold(target_dir: Path, agents: List[AgentItem], rules: List[RuleItem], skills: List[SkillItem]) -> Dict[str, int]`

- [ ] **Step 1: Write the failing test for exporter and conflict resolver**

```python
# directive-cli/tests/test_exporter.py
from pathlib import Path
from directive_cli.core.models import AgentItem, RuleItem, SkillItem
from directive_cli.core.exporter import (
    make_prefix,
    resolve_skill_names,
    resolve_target_directory,
    export_scaffold,
)


def test_make_prefix():
    assert make_prefix("active") == "own"
    assert make_prefix("superpowers") == "sup"
    assert make_prefix("AI-Research-SKILLs") == "ars"
    assert make_prefix("ui-ux-pro-max-skill") == "uupms"


def test_resolve_skill_names_conflict():
    skill1 = SkillItem(source_group="active", name="commit", source_path=Path("active/commit"))
    skill2 = SkillItem(source_group="superpowers", name="commit", source_path=Path("ext/superpowers/commit"))
    skill3 = SkillItem(source_group="anthropics", name="unique-skill", source_path=Path("ext/anth/unique"))

    resolved = resolve_skill_names([skill1, skill2, skill3])
    # Conflict skills get prefix
    assert resolved[0].export_name == "own-commit"
    assert resolved[1].export_name == "sup-commit"
    # Unique skill keeps original name
    assert resolved[2].export_name == "unique-skill"


def test_resolve_target_directory():
    # If path already ends in .agents, keep it
    p1 = Path("/tmp/myproject/.agents")
    assert resolve_target_directory(p1) == p1

    # If path is arbitrary folder, append .agents
    p2 = Path("/tmp/myproject")
    assert resolve_target_directory(p2) == p2 / ".agents"


def test_export_scaffold(tmp_path):
    source_dir = tmp_path / "source"
    source_dir.mkdir()

    # Agent fixture
    agent_dir = source_dir / "agent1"
    agent_dir.mkdir()
    (agent_dir / "agent.md").write_text("agent content")
    agent = AgentItem(name="agent1", source_path=agent_dir)

    # Rule fixture
    rule_file = source_dir / "my.rule.md"
    rule_file.write_text("rule content")
    rule = RuleItem(name="my", source_path=rule_file, filename="my.rule.md")

    # Skill fixture
    skill_dir = source_dir / "skill1"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("skill content")
    skill = SkillItem(source_group="active", name="skill1", source_path=skill_dir, export_name="skill1")

    target = tmp_path / "output_test"
    counts = export_scaffold(target, agents=[agent], rules=[rule], skills=[skill])

    assert counts["agents"] == 1
    assert counts["rules"] == 1
    assert counts["skills"] == 1

    resolved_target = target / ".agents"
    assert (resolved_target / "agents" / "agent1" / "agent.md").exists()
    assert (resolved_target / "rules" / "my.rule.md").exists()
    assert (resolved_target / "skills" / "skill1" / "SKILL.md").exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest directive-cli/tests/test_exporter.py -v`  
Expected: FAIL (ImportError: cannot import name 'make_prefix' from 'directive_cli.core.exporter')

- [ ] **Step 3: Implement exporter and prefix logic**

```python
# directive-cli/core/exporter.py
import re
import shutil
from collections import Counter
from pathlib import Path
from typing import Dict, List
from directive_cli.core.models import AgentItem, RuleItem, SkillItem


def make_prefix(name: str) -> str:
    """Generate source group prefix identical to legacy extract_skills.py."""
    if name == "active":
        return "own"
    parts = [p for p in re.split(r"[-_]+", name) if p]
    if len(parts) == 1:
        return parts[0][:3].lower()
    return "".join(p[0].lower() for p in parts)


def resolve_skill_names(skills: List[SkillItem]) -> List[SkillItem]:
    """Attach export_name with prefix if duplicate skill names exist."""
    name_counts = Counter(s.name for s in skills)
    resolved: List[SkillItem] = []

    for skill in skills:
        if name_counts[skill.name] > 1:
            skill.export_name = f"{make_prefix(skill.source_group)}-{skill.name}"
        else:
            skill.export_name = skill.name
        resolved.append(skill)
    return resolved


def resolve_target_directory(target_path: Path) -> Path:
    """Ensure target directory resolves to a .agents directory."""
    if target_path.name == ".agents":
        return target_path
    return target_path / ".agents"


def _copy_item(src: Path, dst: Path) -> None:
    """Copy file or directory recursively, replacing destination if exists."""
    if src.is_dir():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    elif src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def export_scaffold(
    target_dir: Path,
    agents: List[AgentItem],
    rules: List[RuleItem],
    skills: List[SkillItem],
) -> Dict[str, int]:
    """Export selected agents, rules, and skills into target .agents directory."""
    dest_agents_root = resolve_target_directory(target_dir)

    counts = {"agents": 0, "rules": 0, "skills": 0}

    # 1. Export agents if any selected
    if agents:
        agents_dest = dest_agents_root / "agents"
        agents_dest.mkdir(parents=True, exist_ok=True)
        for agent in agents:
            _copy_item(agent.source_path, agents_dest / agent.name)
            counts["agents"] += 1

    # 2. Export rules if any selected
    if rules:
        rules_dest = dest_agents_root / "rules"
        rules_dest.mkdir(parents=True, exist_ok=True)
        for rule in rules:
            _copy_item(rule.source_path, rules_dest / rule.filename)
            counts["rules"] += 1

    # 3. Export skills if any selected
    if skills:
        skills_dest = dest_agents_root / "skills"
        skills_dest.mkdir(parents=True, exist_ok=True)
        resolved_skills = resolve_skill_names(skills)
        for skill in resolved_skills:
            _copy_item(skill.source_path, skills_dest / skill.export_name)
            counts["skills"] += 1

    return counts
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest directive-cli/tests/test_exporter.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add directive-cli/core/exporter.py directive-cli/tests/test_exporter.py
git commit -m "feat(directive-cli): implement exporter and conflict resolution engine"
```

---

### Task 4: Git Submodule Manager (`core/git_manager.py`)

**Files:**
- Create: `directive-cli/core/git_manager.py`
- Test: `directive-cli/tests/test_git_manager.py`

**Interfaces:**
- Produces:
  - `is_git_repo(root: Path) -> bool`
  - `derive_submodule_name(repo_url: str) -> str`
  - `sync_submodules(root: Path, timeout_seconds: int = 15) -> Tuple[bool, str]`
  - `add_submodule(root: Path, repo_url: str, custom_name: Optional[str] = None) -> Tuple[bool, str]`

- [ ] **Step 1: Write the failing test for git submodule manager**

```python
# directive-cli/tests/test_git_manager.py
from pathlib import Path
from unittest.mock import patch, MagicMock
import subprocess
from directive_cli.core.git_manager import (
    derive_submodule_name,
    sync_submodules,
    add_submodule,
)


def test_derive_submodule_name():
    assert derive_submodule_name("https://github.com/org/my-skills.git") == "my-skills"
    assert derive_submodule_name("https://github.com/org/awesome-agent") == "awesome-agent"
    assert derive_submodule_name("git@github.com:org/tool.git") == "tool"


@patch("subprocess.run")
def test_sync_submodules_success(mock_run, tmp_path):
    mock_run.return_value = MagicMock(returncode=0, stdout="Submodule synced", stderr="")
    success, msg = sync_submodules(tmp_path, timeout_seconds=5)
    assert success is True
    assert "OK" in msg


@patch("subprocess.run")
def test_sync_submodules_timeout(mock_run, tmp_path):
    mock_run.side_effect = subprocess.TimeoutExpired(cmd="git submodule update", timeout=5)
    success, msg = sync_submodules(tmp_path, timeout_seconds=5)
    assert success is False
    assert "timed out" in msg.lower()


@patch("subprocess.run")
def test_add_submodule(mock_run, tmp_path):
    mock_run.return_value = MagicMock(returncode=0, stdout="Added", stderr="")
    success, msg = add_submodule(tmp_path, "https://github.com/org/new-pack.git", custom_name="new-pack")
    assert success is True
    assert "new-pack" in msg
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest directive-cli/tests/test_git_manager.py -v`  
Expected: FAIL (ImportError: cannot import name 'derive_submodule_name' from 'directive_cli.core.git_manager')

- [ ] **Step 3: Implement git submodule manager**

```python
# directive-cli/core/git_manager.py
import re
import subprocess
from pathlib import Path
from typing import Optional, Tuple


def is_git_repo(root: Path) -> bool:
    """Check if root or ancestor is a Git repository."""
    return (root / ".git").exists() or (root.parent / ".git").exists()


def derive_submodule_name(repo_url: str) -> str:
    """Extract clean folder name from Git repository URL."""
    url = repo_url.strip()
    # Remove trailing slashes and .git
    url = re.sub(r"\.git/?$", "", url)
    parts = [p for p in re.split(r"[/:]+", url) if p]
    if parts:
        return parts[-1]
    return "new-submodule"


def sync_submodules(root: Path, timeout_seconds: int = 15) -> Tuple[bool, str]:
    """Execute git submodule update with timeout and offline safety."""
    try:
        cmd = ["git", "submodule", "update", "--init", "--recursive"]
        result = subprocess.run(
            cmd,
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        if result.returncode == 0:
            return True, "Submodules successfully synced (OK)."
        return False, f"Git error ({result.returncode}): {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return False, f"Git submodule sync timed out after {timeout_seconds} seconds."
    except Exception as exc:
        return False, f"Submodule sync failed: {str(exc)}"


def add_submodule(root: Path, repo_url: str, custom_name: Optional[str] = None) -> Tuple[bool, str]:
    """Add a new git submodule into instructions/skills/external/<name>."""
    sub_name = custom_name.strip() if custom_name else derive_submodule_name(repo_url)
    dest_path = root / "instructions" / "skills" / "external" / sub_name

    if dest_path.exists():
        return False, f"Destination folder already exists: {dest_path}"

    rel_dest = Path("instructions") / "skills" / "external" / sub_name
    cmd = ["git", "submodule", "add", repo_url.strip(), str(rel_dest).replace("\\", "/")]

    try:
        result = subprocess.run(
            cmd,
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return True, f"Successfully added submodule '{sub_name}'."
        return False, f"Failed to add submodule: {result.stderr.strip()}"
    except Exception as exc:
        return False, f"Error executing git submodule add: {str(exc)}"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest directive-cli/tests/test_git_manager.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add directive-cli/core/git_manager.py directive-cli/tests/test_git_manager.py
git commit -m "feat(directive-cli): implement git submodule sync and add manager"
```

---

### Task 5: Interactive TUI & Prompts Layer (`ui/`)

**Files:**
- Create: `directive-cli/ui/__init__.py`
- Create: `directive-cli/ui/console.py`
- Create: `directive-cli/ui/display.py`
- Create: `directive-cli/ui/prompts.py`
- Test: `directive-cli/tests/test_ui.py`

**Interfaces:**
- Produces:
  - `console.console`: Rich Console instance
  - `display.print_banner()`
  - `display.print_status(message: str, is_warning: bool)`
  - `display.show_summary_table(agents, rules, skills, target_path)`
  - `prompts.prompt_main_menu() -> str`
  - `prompts.prompt_target_directory(default_path: Path) -> Path`
  - `prompts.prompt_select_agents(agents: List[AgentItem]) -> List[AgentItem]`
  - `prompts.prompt_select_rules(rules: List[RuleItem]) -> List[RuleItem]`
  - `prompts.prompt_select_skills(skill_groups: List[SkillGroup]) -> List[SkillItem]`

- [ ] **Step 1: Write test for UI display and prompt helper logic**

```python
# directive-cli/tests/test_ui.py
from pathlib import Path
from directive_cli.core.models import AgentItem, RuleItem, SkillItem
from directive_cli.ui.display import build_summary_table


def test_build_summary_table():
    agents = [AgentItem(name="omni", source_path=Path(".")) ]
    rules = [RuleItem(name="rule", source_path=Path("."), filename="rule.md")]
    skills = [SkillItem(source_group="active", name="s1", source_path=Path("."))]

    table = build_summary_table(agents, rules, skills, Path("directive-cli/output"))
    assert table.title == "Export Summary"
    assert table.row_count == 3
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest directive-cli/tests/test_ui.py -v`  
Expected: FAIL (ModuleNotFoundError: No module named 'directive_cli.ui')

- [ ] **Step 3: Implement console, display, and prompts**

```python
# directive-cli/ui/__init__.py
"""UI presentation package."""
```

```python
# directive-cli/ui/console.py
from rich.console import Console

console = Console()
```

```python
# directive-cli/ui/display.py
from pathlib import Path
from typing import List
from rich.panel import Panel
from rich.table import Table
from directive_cli.ui.console import console
from directive_cli.core.models import AgentItem, RuleItem, SkillItem


def print_banner() -> None:
    banner_text = (
        "[bold cyan]DIRECTIVE CLI[/bold cyan]\n"
        "[dim]Interactive Scaffolding Tool for Agents, Rules & Skills[/dim]"
    )
    console.print(Panel(banner_text, border_style="cyan", expand=False))


def print_status(message: str, is_warning: bool = False) -> None:
    if is_warning:
        console.print(f"[yellow]⚠️  {message}[/yellow]")
    else:
        console.print(f"[green]✓  {message}[/green]")


def build_summary_table(
    agents: List[AgentItem],
    rules: List[RuleItem],
    skills: List[SkillItem],
    target_path: Path,
) -> Table:
    table = Table(title="Export Summary", border_style="blue")
    table.add_column("Category", style="cyan", no_wrap=True)
    table.add_column("Selected Count", justify="right", style="green")
    table.add_column("Destination", style="magenta")

    table.add_row("Agents", str(len(agents)), str(target_path / ".agents" / "agents"))
    table.add_row("Rules", str(len(rules)), str(target_path / ".agents" / "rules"))
    table.add_row("Skills", str(len(skills)), str(target_path / ".agents" / "skills"))
    return table
```

```python
# directive-cli/ui/prompts.py
from pathlib import Path
from typing import List, Optional
import questionary
from directive_cli.core.models import AgentItem, RuleItem, SkillItem, SkillGroup
from directive_cli.ui.console import console


def prompt_main_menu() -> str:
    choices = [
        "1. Scaffold .agents directory",
        "2. Add a new Git Submodule",
        "3. Manually Sync Submodules",
        "4. Exit",
    ]
    return questionary.select("What would you like to do?", choices=choices).ask()


def prompt_target_directory(default_path: Path) -> Path:
    target_str = questionary.text(
        "Target output directory:",
        default=str(default_path),
    ).ask()
    if not target_str:
        return default_path
    return Path(target_str.strip())


def prompt_select_agents(agents: List[AgentItem]) -> List[AgentItem]:
    if not agents:
        console.print("[dim]No agents found in instructions/agents.[/dim]")
        return []

    create = questionary.confirm("Do you want to configure Agents?", default=True).ask()
    if not create:
        return []

    choices = [
        questionary.Choice(
            title=f"{a.name} ({a.description[:50]})" if a.description else a.name,
            value=a,
            checked=True,
        )
        for a in agents
    ]
    selected = questionary.checkbox("Select Agents to include:", choices=choices).ask()
    return selected or []


def prompt_select_rules(rules: List[RuleItem]) -> List[RuleItem]:
    if not rules:
        console.print("[dim]No rules found in instructions/rules.[/dim]")
        return []

    create = questionary.confirm("Do you want to configure Rules?", default=True).ask()
    if not create:
        return []

    choices = [questionary.Choice(title=r.name, value=r, checked=True) for r in rules]
    selected = questionary.checkbox("Select Rules to include:", choices=choices).ask()
    return selected or []


def prompt_select_skills(skill_groups: List[SkillGroup]) -> List[SkillItem]:
    if not skill_groups:
        console.print("[dim]No skills found.[/dim]")
        return []

    create = questionary.confirm("Do you want to configure Skills?", default=True).ask()
    if not create:
        return []

    selected_skills: List[SkillItem] = []

    while True:
        # 1. Level 1: Choose Groups or Drill-down
        group_choices = []
        for g in skill_groups:
            group_choices.append(
                questionary.Choice(
                    title=f"{g.name} ({len(g.skills)} skills)",
                    value=g,
                    checked=g.is_active,
                )
            )
        group_choices.append(questionary.Separator())
        group_choices.append(questionary.Choice(title="[Drill-down] Select specific individual skills within a group...", value="__DRILL_DOWN__"))

        selected_groups = questionary.checkbox(
            "Select Skill Groups (or choose Drill-down):",
            choices=group_choices,
        ).ask()

        if not selected_groups:
            return []

        if "__DRILL_DOWN__" in selected_groups:
            # Handle Drill-down
            target_group_name = questionary.select(
                "Choose group to inspect and select individual skills:",
                choices=[g.name for g in skill_groups],
            ).ask()
            group_obj = next(g for g in skill_groups if g.name == target_group_name)

            skill_choices = [
                questionary.Choice(title=s.name, value=s, checked=True)
                for s in group_obj.skills
            ]
            picked = questionary.checkbox(
                f"Select skills from {group_obj.name}:",
                choices=skill_choices,
            ).ask()
            if picked:
                selected_skills.extend(picked)

            more = questionary.confirm("Do you want to select from other groups?", default=False).ask()
            if not more:
                break
        else:
            for g in selected_groups:
                if isinstance(g, SkillGroup):
                    selected_skills.extend(g.skills)
            break

    # Deduplicate selected skills by object
    unique_skills = []
    seen = set()
    for s in selected_skills:
        key = (s.source_group, s.name)
        if key not in seen:
            seen.add(key)
            unique_skills.append(s)

    return unique_skills
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest directive-cli/tests/test_ui.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add directive-cli/ui/ directive-cli/tests/test_ui.py
git commit -m "feat(directive-cli): implement interactive TUI and prompts layer"
```

---

### Task 6: CLI Entry Point & Orchestration (`main.py`)

**Files:**
- Create: `directive-cli/main.py`
- Test: `directive-cli/tests/test_cli_smoke.py`

**Interfaces:**
- Consumes:
  - `directive_cli.config`
  - `directive_cli.core.{scanner, exporter, git_manager}`
  - `directive_cli.ui.{console, display, prompts}`
- Produces:
  - CLI executable entry point (`python -m directive_cli.main`)

- [ ] **Step 1: Write smoke test for CLI invocation**

```python
# directive-cli/tests/test_cli_smoke.py
import subprocess
import sys


def test_cli_help_flag():
    result = subprocess.run(
        [sys.executable, "-m", "directive_cli.main", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "directive-cli" in result.stdout.lower() or "usage" in result.stdout.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest directive-cli/tests/test_cli_smoke.py -v`  
Expected: FAIL (No module named directive_cli.main)

- [ ] **Step 3: Implement `main.py`**

```python
# directive-cli/main.py
import argparse
import sys
from pathlib import Path
import questionary

from directive_cli import config
from directive_cli.core import scanner, exporter, git_manager
from directive_cli.ui import console, display, prompts


def parse_args():
    parser = argparse.ArgumentParser(
        prog="directive-cli",
        description="Scaffolding tool for agents, rules, and skills into .agents/",
    )
    parser.add_argument(
        "--skip-sync",
        action="store_true",
        help="Skip automatic Git submodule sync during startup",
    )
    parser.add_argument(
        "--target",
        type=str,
        default=None,
        help="Default target directory for scaffolding (default: directive-cli/output/)",
    )
    return parser.parse_args()


def run_scaffold_flow(root: Path, target_base: Path):
    target_path = prompts.prompt_target_directory(target_base)

    # 1. Scan and prompt Agents
    agents_all = scanner.scan_agents(config.DEFAULT_AGENTS_SOURCE)
    selected_agents = prompts.prompt_select_agents(agents_all)

    # 2. Scan and prompt Rules
    rules_all = scanner.scan_rules(config.DEFAULT_RULES_SOURCE)
    selected_rules = prompts.prompt_select_rules(rules_all)

    # 3. Scan and prompt Skills
    skill_groups_all = scanner.scan_skills(config.DEFAULT_SKILLS_ACTIVE, config.DEFAULT_SKILLS_EXTERNAL)
    selected_skills = prompts.prompt_select_skills(skill_groups_all)

    if not (selected_agents or selected_rules or selected_skills):
        console.console.print("[yellow]No items selected. Aborting scaffold.[/yellow]")
        return

    # Review table
    table = display.build_summary_table(selected_agents, selected_rules, selected_skills, target_path)
    console.console.print(table)

    confirm = questionary.confirm("Proceed with export?", default=True).ask()
    if confirm:
        with console.console.status("[bold green]Exporting scaffold...[/bold green]"):
            counts = exporter.export_scaffold(
                target_dir=target_path,
                agents=selected_agents,
                rules=selected_rules,
                skills=selected_skills,
            )
        display.print_status(
            f"Successfully exported: {counts['agents']} agents, {counts['rules']} rules, {counts['skills']} skills to {target_path / '.agents'}"
        )


def run_add_submodule_flow(root: Path):
    url = questionary.text("Git repository URL:").ask()
    if not url:
        return
    name = questionary.text("Submodule name (leave empty for auto-detect):").ask()
    with console.console.status("[bold cyan]Adding Git submodule...[/bold cyan]"):
        success, msg = git_manager.add_submodule(root, url, name if name else None)
    display.print_status(msg, is_warning=not success)


def main():
    args = parse_args()
    display.print_banner()

    root = config.REPO_ROOT
    target_base = Path(args.target) if args.target else config.DEFAULT_OUTPUT_DIR

    # Auto sync submodules on startup
    if not args.skip_sync and git_manager.is_git_repo(root):
        with console.console.status("[bold cyan]Syncing latest Git submodules...[/bold cyan]"):
            success, msg = git_manager.sync_submodules(root, timeout_seconds=config.SUBMODULE_TIMEOUT_SECONDS)
        if not success:
            display.print_status(f"Offline mode: {msg}", is_warning=True)
        else:
            display.print_status(msg)

    while True:
        choice = prompts.prompt_main_menu()
        if not choice or "4. Exit" in choice:
            console.console.print("[dim]Goodbye![/dim]")
            break
        elif "1. Scaffold" in choice:
            run_scaffold_flow(root, target_base)
        elif "2. Add a new Git Submodule" in choice:
            run_add_submodule_flow(root)
        elif "3. Manually Sync Submodules" in choice:
            with console.console.status("[bold cyan]Syncing Git submodules...[/bold cyan]"):
                success, msg = git_manager.sync_submodules(root, timeout_seconds=config.SUBMODULE_TIMEOUT_SECONDS)
            display.print_status(msg, is_warning=not success)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest directive-cli/tests/test_cli_smoke.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add directive-cli/main.py directive-cli/tests/test_cli_smoke.py
git commit -m "feat(directive-cli): implement CLI entry point and interactive lifecycle orchestration"
```

---

### Task 7: Documentation & End-to-End Verification

**Files:**
- Create: `directive-cli/README.md`
- Test: Full test suite execution

**Interfaces:**
- Complete user manual with installation, flags, and workflow examples.

- [ ] **Step 1: Write `directive-cli/README.md`**

Document:
- Installation: `pip install -r requirements.txt`
- Interactive Launch: `python -m directive_cli.main`
- CLI Flags: `--skip-sync`, `--target <path>`
- How default output `directive-cli/output/.agents/` works vs custom target path.
- Explanation of submodule auto-sync and offline fallback.

- [ ] **Step 2: Run complete pytest test suite**

Run: `python -m pytest directive-cli/tests/ -v`  
Expected: ALL PASS

- [ ] **Step 3: Commit**

```bash
git add directive-cli/README.md
git commit -m "docs(directive-cli): add comprehensive documentation and usage guide"
```
