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


def prompt_target_directory(default_path: Path) -> Optional[Path]:
    target_str = questionary.text(
        "Target output directory:",
        default=str(default_path),
    ).ask()
    if target_str is None:
        return None
    if not target_str.strip():
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
        # Level 1: Choose Groups or Drill-down
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
        group_choices.append(
            questionary.Choice(
                title="[Drill-down] Select specific individual skills within a group...",
                value="__DRILL_DOWN__",
            )
        )

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
            if not target_group_name:
                break
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

    # Deduplicate selected skills
    unique_skills = []
    seen = set()
    for s in selected_skills:
        key = (s.source_group, s.name)
        if key not in seen:
            seen.add(key)
            unique_skills.append(s)

    return unique_skills
