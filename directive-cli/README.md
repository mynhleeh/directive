# Directive CLI

An interactive command-line interface for scaffolding modular AI agent workspaces (`.agents/`), managing rules, selecting skills, and maintaining external Git submodules.

---

## Overview

`directive-cli` streamlines the configuration of AI agent environments (such as Antigravity, Gemini CLI, Claude Code, and compatible tooling). It replaces manual copying and ad-hoc scripts with a guided, interactive terminal workflow.

With `directive-cli`, you can:
- Interactively select which **Agents**, **Rules**, and **Skills** to include in your project workspace.
- Choose entire skill groups at once or drill down to select individual skills.
- Automatically resolve skill name collisions using deterministic namespace prefixing.
- Add and sync external Git skill repositories as submodules with timeout safeguards and offline fallback.
- Export clean, ready-to-use `.agents/` scaffolds directly into any target directory.

> **Note:** The legacy script `instructions/scripts/extract_skills.py` remains completely intact and unmodified for backwards compatibility.

---

## Requirements & Installation

- **Python**: 3.8 or higher (Python 3.10+ recommended)
- **Git**: Installed and available on `PATH`

Install dependencies:

```bash
pip install -r directive-cli/requirements.txt
```

Dependencies include:
- [`rich`](https://github.com/Textualize/rich) (>=13.0.0): Terminal formatting, status spinners, and tables.
- [`questionary`](https://github.com/tmbo/questionary) (>=2.0.0): Interactive multi-select checklists and prompts.
- [`pytest`](https://github.com/pytest-dev/pytest) (>=7.0.0): Automated test suite.

---

## How to Run

You can launch `directive-cli` using either of the following commands from the repository root:

```bash
python -m directive_cli.main
```

or directly:

```bash
python directive-cli/main.py
```

### CLI Options

| Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--target <path>` | String / Path | `directive-cli/output/` | Set the base destination directory for scaffolding. The tool guarantees output inside `<path>/.agents/`. |
| `--skip-sync` | Flag | `False` | Skip automatic Git submodule synchronization on startup (useful in offline environments or for faster startup). |
| `-h`, `--help` | Flag | - | Show help message and exit. |

Example running with options:

```bash
# Export directly towards another project without startup submodule sync
python -m directive_cli.main --target "C:/Projects/my-new-app" --skip-sync
```

---

## Workflows

Upon launch, `directive-cli` checks for submodules (unless `--skip-sync` is passed) and presents the main menu:

```text
What would you like to do?
  1. Scaffold .agents directory
  2. Add a new Git Submodule
  3. Manually Sync Submodules
  4. Exit
```

### 1. Scaffolding `.agents/`

The scaffolding wizard walks you through 5 intuitive steps:

1. **Target Directory**: Confirm or adjust the target export location (defaults to `--target` or `directive-cli/output/`). If the target path does not end with `.agents`, `.agents` is automatically appended.
2. **Configure Agents**: Choose which custom agents from `instructions/agents/` to include. Agent descriptions are parsed from markdown frontmatter to assist selection.
3. **Configure Rules**: Choose which guidelines and operational rules from `instructions/rules/` to bundle.
4. **Configure Skills (2-Level Hierarchy)**:
   - **Level 1 (Group Selection)**: Select entire collections (e.g., active repository skills, or external submodule collections like `superpowers`, `AI-Research-SKILLs`). Active skills are pre-selected by default.
   - **Drill-Down Mode**: Select `[Drill-down]` to open a sub-menu, choose a specific group, and pick fine-grained individual skills from that group.
5. **Review & Export**: A rich summary table displays the final selection counts, item names, and destination paths. Confirming writes the files safely to disk.

### 2. Adding a New Git Submodule

Allows you to easily expand the collection of external skills:
1. Enter the Git repository URL (e.g., `https://github.com/example/skills.git`).
2. Enter an optional submodule folder name (defaults automatically to repository basename).
3. The tool executes `git submodule add <url> instructions/skills/external/<name>` and verifies the destination.

### 3. Manually Syncing Submodules

Triggers `git submodule update --init --recursive --remote` with a 30-second timeout. If network access is unavailable, the tool logs a warning and gracefully falls back without blocking your session.

---

## Conflict Resolution & Prefixing

When assembling skills from both `active` (`instructions/skills/active/`) and multiple external submodule folders (`instructions/skills/external/*/skills/`), duplicate skill names can occur (e.g., both collections provide a `commit` skill).

`directive-cli` resolves name collisions automatically at export time:

- **No Collision**: If a skill name is unique among selected skills, its original name is preserved (e.g., `python-dataviz-guide`).
- **Colliding Active Skills**: Active skills receive the `own-` prefix (e.g., `own-commit`).
- **Colliding Submodule Skills**: External skills receive a prefix derived from their submodule folder name:
  - **Single-word folder**: First 3 letters in lowercase (e.g., `superpowers` $\rightarrow$ `sup-commit`).
  - **Multi-word / hyphenated / underscored folder**: Acronym of initial letters (e.g., `AI-Research-SKILLs` $\rightarrow$ `ars-commit`, `ui-ux-pro-max-skill` $\rightarrow$ `uupms-commit`).

This matches the behavior of the legacy script while keeping output clean and predictable.

---

## Architecture & Codebase Map

```text
directive-cli/
├── __init__.py           # Package marker
├── config.py             # Global constants, default paths, and timeouts
├── main.py               # Application entry point and CLI command loop
├── requirements.txt      # Runtime and development dependencies
├── core/
│   ├── __init__.py
│   ├── models.py         # Dataclasses: AgentItem, RuleItem, SkillItem, SkillGroup
│   ├── scanner.py        # Filesystem scanner for agents, rules, and skills
│   ├── git_manager.py    # Submodule discovery, sync, and addition
│   └── exporter.py       # Safe recursive file copy, conflict resolution, export
├── ui/
│   ├── __init__.py
│   ├── console.py        # Centralized Rich console instance
│   ├── display.py        # ASCII banners, status indicators, summary tables
│   └── prompts.py        # Questionary prompts (menus, checkboxes, drill-down)
└── tests/
    ├── conftest.py           # Test fixtures and path configurations
    ├── test_cli_smoke.py     # End-to-end CLI arguments and workflow tests
    ├── test_exporter.py      # Export logic, directory resolution, prefixing tests
    ├── test_git_manager.py   # Submodule sync, name derivation, and addition tests
    ├── test_models.py        # Data model integrity and default paths
    ├── test_scanner.py       # Discovery logic and edge-case scanning
    └── test_ui.py            # Rich display and Questionary prompt mocks
```

---

## Running Tests

Run the full automated test suite using `pytest`:

```bash
python -m pytest directive-cli/tests/ -v
```

All tests mock interactive inputs and filesystem boundaries, guaranteeing zero side-effects on your working repository during test execution.
