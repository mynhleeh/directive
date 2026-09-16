# Design Specification: directive-cli

**Author:** Antigravity  
**Date:** 2026-09-16  
**Status:** Approved  
**Branch:** `cli-tool`  
**Target:** `directive-cli/` at repository root  

---

## 1. Executive Summary & Objectives

`directive-cli` is an interactive Terminal User Interface (TUI) and Command-Line Interface (CLI) tool designed to manage, discover, select, and scaffold agent configurations, rules, and skills into a targeted `.agents/` structure.

The tool replaces manual extraction scripts while keeping the legacy script `instructions/scripts/extract_skills.py` intact. It provides a guided terminal workflow powered by `questionary` and `rich`, with robust offline resilience, automatic Git submodule synchronization, and seamless submodule management.

### Key Objectives
1. **Interactive Scaffolding**: Guide the user step-by-step to scaffold `.agents/` containing selected `agents`, `rules`, and `skills`.
2. **Dynamic Listing & Discovery**: Dynamically scan and list all available agents (`instructions/agents`), rules (`instructions/rules`), and skills (`instructions/skills/active` and `instructions/skills/external/*`).
3. **Hierarchical Skill Selection**: Support selecting skills either as entire groups (`active/own`, or specific submodules) or by drilling down to individual skills.
4. **Git Submodule Automation**: Automatically synchronize submodules at startup with non-blocking offline fallback, and allow adding new Git submodules interactively.
5. **Conflict Resolution**: Inherit and enforce skill prefixing rules (`own-<name>`, `<submodule_prefix>-<name>`) to resolve duplicate skill names across multiple sources.
6. **Isolation**: Reside in `directive-cli/` at the repository root without altering existing scripts or core instruction files.

---

## 2. System Architecture & Folder Layout

```text
directive/
├── directive-cli/
│   ├── __init__.py
│   ├── main.py                  # Entry point, CLI flags (--skip-sync, --target), lifecycle
│   ├── config.py                # Constant paths, timeout values, styling constants
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py            # Data classes: AgentItem, RuleItem, SkillItem, SkillGroup
│   │   ├── scanner.py           # Filesystem discovery for agents, rules, and skills
│   │   ├── git_manager.py       # Submodule auto-sync, add submodule, offline detection
│   │   └── exporter.py          # Name conflict resolution, directory cleaning, file copying
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── console.py           # Rich console initialization and styling themes
│   │   ├── display.py           # Banners, spinners, summary tables, status messages
│   │   └── prompts.py           # Questionary interactive menus and checkbox prompts
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_scanner.py      # Unit tests for scanner functionality
│   │   ├── test_exporter.py     # Unit tests for prefix and copy logic
│   │   └── test_git_manager.py  # Unit tests for git sync and add logic
│   ├── requirements.txt         # Dependencies (questionary, rich, pytest)
│   └── README.md                # Usage guide and CLI documentation
├── instructions/
│   ├── agents/                  # Source agents
│   ├── rules/                   # Source rules
│   ├── skills/                  # Source skills (active/ & external/*)
│   └── scripts/
│       └── extract_skills.py    # Unmodified legacy script
└── .agents/                     # Default output target directory
    ├── agents/
    ├── rules/
    └── skills/
```

---

## 3. Component Breakdown & Data Models

### 3.1 Data Models (`core/models.py`)

```python
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

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
    source_group: str          # "active" or submodule directory name
    name: str                  # Original folder/skill name
    source_path: Path          # Path to directory containing SKILL.md
    export_name: str = ""      # Resolved destination name (with prefix if duplicate)

@dataclass
class SkillGroup:
    name: str                  # "active (own)" or submodule name
    raw_name: str              # "active" or directory name in instructions/skills/external
    is_active: bool            # True if active/own, False if external submodule
    skills: List[SkillItem] = field(default_factory=list)
```

### 3.2 Core Components

#### `core/scanner.py`
- `scan_agents(base_dir: Path) -> List[AgentItem]`:
  Scans subdirectories in `instructions/agents`. Extracts optional description from `agent.md` frontmatter or header.
- `scan_rules(base_dir: Path) -> List[RuleItem]`:
  Scans `instructions/rules` for `*.rule.md` files.
- `scan_skills(active_dir: Path, external_dir: Path) -> List[SkillGroup]`:
  - Scans `instructions/skills/active` for child folders containing `SKILL.md` (group: `active (own)`).
  - Scans each subdirectory under `instructions/skills/external/` using `os.walk` to find folders containing `SKILL.md` (one group per submodule).
  - Deduplicates skills within each submodule.

#### `core/git_manager.py`
- `is_git_repo(root: Path) -> bool`:
  Verifies that current project is a Git repository.
- `sync_submodules(root: Path, timeout_seconds: int = 15) -> Tuple[bool, str]`:
  Executes `git submodule update --init --recursive`.
  - Catches `TimeoutExpired`, network disconnection, and Git errors.
  - Returns `(True, "OK")` on success, or `(False, error_message)` on failure/timeout without crashing.
- `add_submodule(root: Path, repo_url: str, custom_name: Optional[str] = None) -> Tuple[bool, str]`:
  - Derives submodule name from repo URL if not supplied.
  - Validates destination `instructions/skills/external/<name>` does not already exist.
  - Executes `git submodule add <repo_url> instructions/skills/external/<name>`.
  - Initializes the newly added submodule.

#### `core/exporter.py`
- `make_prefix(name: str) -> str`:
  Ported directly from `extract_skills.py`:
  - If `name == "active"`: returns `"own"`
  - Otherwise splits by `[-_]+` and returns lowercase initial letters or first 3 letters.
- `resolve_skill_names(skills: List[SkillItem]) -> List[SkillItem]`:
  Counts occurrences of `name`. If count > 1, sets `export_name = f"{make_prefix(skill.source_group)}-{skill.name}"`, else `export_name = skill.name`.
- `export_scaffold(target_dir: Path, agents: List[AgentItem], rules: List[RuleItem], skills: List[SkillItem]) -> Dict[str, int]`:
  - Prepares directories under `target_dir`: `.agents/agents`, `.agents/rules`, `.agents/skills`.
  - Clears only the subdirectories that are being updated (or leaves untouched if user opted out).
  - Copies agent directories into `target_dir / "agents" / agent.name`.
  - Copies rule files into `target_dir / "rules" / rule.filename`.
  - Copies skill directories into `target_dir / "skills" / skill.export_name`.
  - Returns count statistics: `{"agents": X, "rules": Y, "skills": Z}`.

---

## 4. User Interaction & TUI Workflows (`ui/`)

### 4.1 Startup Sequence
1. Displays application banner:
   ```text
   ╭──────────────────────────────────────────────────╮
   │                 DIRECTIVE CLI                    │
   │       Agent, Rule & Skill Scaffolding Tool       │
   ╰──────────────────────────────────────────────────╯
   ```
2. Checks `--skip-sync` flag:
   - If not skipped: runs `sync_submodules()` with a Rich spinner: `[bold cyan]Syncing latest Git submodules...[/bold cyan]`.
   - On network error or timeout: prints warning banner: `[yellow]⚠️  Offline mode: Could not reach remote, using cached submodules.[/yellow]`.

### 4.2 Main Menu
Prompt with choices:
- `1. Scaffold .agents directory`
- `2. Add a new Git Submodule`
- `3. Manually Sync Submodules`
- `4. Exit`

### 4.3 Scaffolding Workflow (`Scaffold .agents`)
1. **Target Confirmation**:
   - Prompts for target directory (default: `./.agents`). User can press Enter to keep default or type a custom path.
2. **Agents Selection**:
   - Prompt: *"Do you want to configure Agents?"* `[Y/n]`
   - If Yes:
     - Displays Rich table of found agents (`cv-architect`, `directive`, `omni`).
     - Checkbox selection: allows selecting all or specific agents.
3. **Rules Selection**:
   - Prompt: *"Do you want to configure Rules?"* `[Y/n]`
   - If Yes:
     - Displays Rich table of found rules (`file-folder-organization.rule.md`).
     - Checkbox selection: allows selecting all or specific rules.
4. **Skills Selection**:
   - Prompt: *"Do you want to configure Skills?"* `[Y/n]`
   - If Yes:
     - Shows Hierarchical Group Menu:
       - `[x] Active (own) (2 skills)`
       - `[ ] anthropics (15 skills)`
       - `[ ] superpowers (18 skills)`
       - `...`
       - `[>] Drill-down: Select individual skills within a group...`
     - When drilling down, user picks a group, sees all skills within that group as a checkbox list, and ticks desired skills.
5. **Review & Confirmation Table**:
   - Displays a clean Rich Summary Table:
     | Resource | Selected Count | Destination |
     | :--- | :--- | :--- |
     | Agents | 2 | `./.agents/agents/` |
     | Rules | 1 | `./.agents/rules/` |
     | Skills | 35 | `./.agents/skills/` |
   - Prompt: *"Proceed with exporting to `./.agents`?"* `[Y/n]`
   - On confirmation, executes `export_scaffold()`, displays live progress, and prints success summary.

### 4.4 Add Submodule Workflow
1. Prompt: *"Enter Git Repository URL (e.g., https://github.com/org/repo.git):"*
2. Automatically derives default group name from URL (e.g. `repo`), allows user to customize.
3. Validates path `instructions/skills/external/<group_name>`.
4. Executes `git submodule add` with a Rich spinner.
5. Displays success notice and refreshes available skills in memory.

---

## 5. Error Handling & Edge Cases

| Scenario | Handling Mechanism |
| :--- | :--- |
| **Offline startup / Git network timeout** | Catch `TimeoutExpired` & `CalledProcessError`; print warning; continue seamlessly using local files. |
| **No Git repository found** | Warn user that Git submodule operations are disabled; allow local scaffolding without submodule commands. |
| **Duplicate Skill Names across submodules** | Count occurrences across selected skills; apply deterministic prefix (`own-` or abbreviation) so files are never overwritten silently. |
| **Submodule directory already exists on Add** | Check filesystem before running command; show friendly error prompt without executing broken Git state. |
| **Windows Path Separators** | Use `pathlib.Path` consistently across all scanners and exporters to guarantee cross-platform support. |
| **UTF-8 Encoding on Windows** | Force `encoding="utf-8"` when reading markdown or frontmatter files. |

---

## 6. Testing Strategy

1. **Unit Tests (`directive-cli/tests/`)**:
   - `test_scanner.py`:
     - Test scanning mock `instructions/agents` directory.
     - Test scanning mock `instructions/rules` directory.
     - Test scanning active skills and nested submodule skills with `SKILL.md`.
   - `test_exporter.py`:
     - Test `make_prefix` logic against various names (`active`, `AI-Research-SKILLs`, `ui-ux-pro-max-skill`).
     - Test name conflict resolution when two skills share identical names.
     - Test file copy and clean directory behavior.
   - `test_git_manager.py`:
     - Mock `subprocess.run` to test sync success, network failure, and timeout scenarios.
     - Test submodule URL extraction and name parsing.
2. **Smoke Test**:
   - Test `python -m directive-cli.main --skip-sync --help` execution without errors.
   - Verify non-interactive execution with default flags.

---

## 7. Implementation Roadmap & Subagent Work Plan

The implementation will be executed on branch `cli-tool` following subagent-driven development:
- **Task 1: Foundation & Project Scaffolding** (`config.py`, `models.py`, `requirements.txt`)
- **Task 2: Core Scanning & Exporter Engine** (`core/scanner.py`, `core/exporter.py` + tests)
- **Task 3: Git Submodule Manager** (`core/git_manager.py` + tests)
- **Task 4: Interactive TUI & Prompts Layer** (`ui/console.py`, `ui/display.py`, `ui/prompts.py`)
- **Task 5: CLI Entry Point & Orchestration** (`main.py` integrating all flows)
- **Task 6: Documentation & End-to-End Verification** (`directive-cli/README.md` + full verification run)
