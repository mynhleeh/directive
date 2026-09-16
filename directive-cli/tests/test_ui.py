from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from directive_cli.core.models import AgentItem, RuleItem, SkillItem, SkillGroup
from directive_cli.ui.display import print_banner, print_status, build_summary_table
from directive_cli.ui.prompts import (
    prompt_main_menu,
    prompt_target_directory,
    prompt_select_agents,
    prompt_select_rules,
    prompt_select_skills,
)


def test_build_summary_table():
    agents = [AgentItem(name="omni", source_path=Path("."))]
    rules = [RuleItem(name="rule", source_path=Path("."), filename="rule.md")]
    skills = [SkillItem(source_group="active", name="s1", source_path=Path("."))]

    # Path not ending with .agents
    table = build_summary_table(agents, rules, skills, Path("directive-cli/output"))
    assert table.title == "Export Summary"
    assert table.row_count == 3

    # Path already ending with .agents
    table_dot_agents = build_summary_table(agents, rules, skills, Path("custom/.agents"))
    assert table_dot_agents.title == "Export Summary"
    assert table_dot_agents.row_count == 3


def test_print_banner():
    with patch("directive_cli.ui.display.console.print") as mock_print:
        print_banner()
        mock_print.assert_called_once()
        panel = mock_print.call_args[0][0]
        assert "DIRECTIVE CLI" in panel.renderable


def test_print_status():
    with patch("directive_cli.ui.display.console.print") as mock_print:
        print_status("All good", is_warning=False)
        assert "All good" in mock_print.call_args[0][0]
        assert "✓" in mock_print.call_args[0][0]

        print_status("Watch out", is_warning=True)
        assert "Watch out" in mock_print.call_args[0][0]
        assert "⚠️" in mock_print.call_args[0][0]


def test_prompt_main_menu():
    with patch("questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "1. Scaffold .agents directory"
        result = prompt_main_menu()
        assert result == "1. Scaffold .agents directory"
        mock_select.assert_called_once()


def test_prompt_target_directory():
    default_p = Path("directive-cli/output")

    # Custom input provided
    with patch("questionary.text") as mock_text:
        mock_text.return_value.ask.return_value = "custom/target/dir"
        res = prompt_target_directory(default_p)
        assert res == Path("custom/target/dir")

    # Empty input defaults to default_path
    with patch("questionary.text") as mock_text:
        mock_text.return_value.ask.return_value = ""
        res = prompt_target_directory(default_p)
        assert res == default_p

    # Whitespace trimmed
    with patch("questionary.text") as mock_text:
        mock_text.return_value.ask.return_value = "  spaced/dir  "
        res = prompt_target_directory(default_p)
        assert res == Path("spaced/dir")


def test_prompt_select_agents():
    # Empty list
    with patch("directive_cli.ui.prompts.console.print") as mock_print:
        res = prompt_select_agents([])
        assert res == []
        mock_print.assert_called_once()

    agent1 = AgentItem(name="omni", source_path=Path("instructions/agents/omni"), description="Omni agent description")
    agent2 = AgentItem(name="coder", source_path=Path("instructions/agents/coder"))

    # User declines confirmation
    with patch("questionary.confirm") as mock_confirm:
        mock_confirm.return_value.ask.return_value = False
        res = prompt_select_agents([agent1, agent2])
        assert res == []

    # User confirms and selects agents
    with patch("questionary.confirm") as mock_confirm, patch("questionary.checkbox") as mock_checkbox:
        mock_confirm.return_value.ask.return_value = True
        mock_checkbox.return_value.ask.return_value = [agent1]
        res = prompt_select_agents([agent1, agent2])
        assert res == [agent1]

    # User confirms but selects none (returns empty list)
    with patch("questionary.confirm") as mock_confirm, patch("questionary.checkbox") as mock_checkbox:
        mock_confirm.return_value.ask.return_value = True
        mock_checkbox.return_value.ask.return_value = None
        res = prompt_select_agents([agent1, agent2])
        assert res == []


def test_prompt_select_rules():
    # Empty list
    with patch("directive_cli.ui.prompts.console.print") as mock_print:
        res = prompt_select_rules([])
        assert res == []
        mock_print.assert_called_once()

    rule1 = RuleItem(name="r1", source_path=Path("r1.md"), filename="r1.md")
    rule2 = RuleItem(name="r2", source_path=Path("r2.md"), filename="r2.md")

    # User declines confirmation
    with patch("questionary.confirm") as mock_confirm:
        mock_confirm.return_value.ask.return_value = False
        res = prompt_select_rules([rule1, rule2])
        assert res == []

    # User confirms and selects rules
    with patch("questionary.confirm") as mock_confirm, patch("questionary.checkbox") as mock_checkbox:
        mock_confirm.return_value.ask.return_value = True
        mock_checkbox.return_value.ask.return_value = [rule1, rule2]
        res = prompt_select_rules([rule1, rule2])
        assert res == [rule1, rule2]

    # User confirms but returns None
    with patch("questionary.confirm") as mock_confirm, patch("questionary.checkbox") as mock_checkbox:
        mock_confirm.return_value.ask.return_value = True
        mock_checkbox.return_value.ask.return_value = None
        res = prompt_select_rules([rule1, rule2])
        assert res == []


def test_prompt_select_skills():
    # Empty skill groups
    with patch("directive_cli.ui.prompts.console.print") as mock_print:
        res = prompt_select_skills([])
        assert res == []
        mock_print.assert_called_once()

    s1 = SkillItem(source_group="active", name="s1", source_path=Path("s1"))
    s2 = SkillItem(source_group="active", name="s2", source_path=Path("s2"))
    group1 = SkillGroup(name="active", raw_name="active", is_active=True, skills=[s1, s2])

    s3 = SkillItem(source_group="ext", name="s3", source_path=Path("s3"))
    group2 = SkillGroup(name="ext", raw_name="ext", is_active=False, skills=[s3])

    # User declines confirmation
    with patch("questionary.confirm") as mock_confirm:
        mock_confirm.return_value.ask.return_value = False
        res = prompt_select_skills([group1, group2])
        assert res == []

    # User selects groups directly (no drill down)
    with patch("questionary.confirm") as mock_confirm, patch("questionary.checkbox") as mock_checkbox:
        mock_confirm.return_value.ask.return_value = True
        mock_checkbox.return_value.ask.return_value = [group1]
        res = prompt_select_skills([group1, group2])
        assert res == [s1, s2]

    # User cancels / selects empty groups
    with patch("questionary.confirm") as mock_confirm, patch("questionary.checkbox") as mock_checkbox:
        mock_confirm.return_value.ask.return_value = True
        mock_checkbox.return_value.ask.return_value = []
        res = prompt_select_skills([group1, group2])
        assert res == []

    # User uses drill-down
    with patch("questionary.confirm") as mock_confirm, \
         patch("questionary.checkbox") as mock_checkbox, \
         patch("questionary.select") as mock_select:
        # 1. confirm configure skills -> True
        # 2. confirm more groups -> False
        mock_confirm.return_value.ask.side_effect = [True, False]
        # 1. checkbox for groups -> selects drill down
        # 2. checkbox for skills in chosen group -> selects s1
        mock_checkbox.return_value.ask.side_effect = [["__DRILL_DOWN__"], [s1]]
        mock_select.return_value.ask.return_value = "active"

        res = prompt_select_skills([group1, group2])
        assert res == [s1]

    # User cancels drill-down (target_group_name is None or empty)
    with patch("questionary.confirm") as mock_confirm, \
         patch("questionary.checkbox") as mock_checkbox, \
         patch("questionary.select") as mock_select:
        mock_confirm.return_value.ask.return_value = True
        mock_checkbox.return_value.ask.return_value = ["__DRILL_DOWN__"]
        mock_select.return_value.ask.return_value = None

        res = prompt_select_skills([group1, group2])
        assert res == []

