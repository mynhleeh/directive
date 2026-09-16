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
    dest_path = target_path if target_path.name == ".agents" else target_path / ".agents"
    table = Table(title="Export Summary", border_style="blue")
    table.add_column("Category", style="cyan", no_wrap=True)
    table.add_column("Selected Count", justify="right", style="green")
    table.add_column("Destination", style="magenta")

    table.add_row("Agents", str(len(agents)), str(dest_path / "agents"))
    table.add_row("Rules", str(len(rules)), str(dest_path / "rules"))
    table.add_row("Skills", str(len(skills)), str(dest_path / "skills"))
    return table
