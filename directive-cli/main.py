import argparse
import sys
from pathlib import Path
import importlib.util
import questionary

if "directive_cli" not in sys.modules:
    cli_dir = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location(
        "directive_cli",
        cli_dir / "__init__.py",
        submodule_search_locations=[str(cli_dir)],
    )
    if spec and spec.loader:
        mod = importlib.util.module_from_spec(spec)
        sys.modules["directive_cli"] = mod
        spec.loader.exec_module(mod)

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
    if target_path is None:
        return

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
        dest_display = target_path if target_path.name == ".agents" else target_path / ".agents"
        display.print_status(
            f"Successfully exported: {counts['agents']} agents, {counts['rules']} rules, {counts['skills']} skills to {dest_display}"
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
