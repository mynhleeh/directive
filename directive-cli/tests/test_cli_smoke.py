import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from directive_cli.main import parse_args, run_scaffold_flow, run_add_submodule_flow


def test_cli_help_flag():
    main_file = Path(__file__).resolve().parent.parent / "main.py"
    result = subprocess.run(
        [sys.executable, "-m", "directive_cli.main", "--help"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 and "No module named 'directive_cli'" in result.stderr:
        result = subprocess.run(
            [sys.executable, str(main_file), "--help"],
            capture_output=True,
            text=True,
        )
    assert result.returncode == 0
    assert "directive-cli" in result.stdout.lower() or "usage" in result.stdout.lower()


def test_parse_args_defaults():
    with patch("sys.argv", ["directive-cli"]):
        args = parse_args()
        assert args.skip_sync is False
        assert args.target is None


def test_parse_args_custom():
    with patch("sys.argv", ["directive-cli", "--skip-sync", "--target", "/my/custom/path"]):
        args = parse_args()
        assert args.skip_sync is True
        assert args.target == "/my/custom/path"


@patch("directive_cli.ui.prompts.prompt_target_directory")
@patch("directive_cli.core.scanner.scan_agents")
@patch("directive_cli.ui.prompts.prompt_select_agents")
@patch("directive_cli.core.scanner.scan_rules")
@patch("directive_cli.ui.prompts.prompt_select_rules")
@patch("directive_cli.core.scanner.scan_skills")
@patch("directive_cli.ui.prompts.prompt_select_skills")
@patch("questionary.confirm")
@patch("directive_cli.core.exporter.export_scaffold")
def test_run_scaffold_flow(
    mock_export,
    mock_confirm,
    mock_select_skills,
    mock_scan_skills,
    mock_select_rules,
    mock_scan_rules,
    mock_select_agents,
    mock_scan_agents,
    mock_target_prompt,
    tmp_path,
):
    mock_target_prompt.return_value = tmp_path / "output"
    mock_scan_agents.return_value = []
    mock_select_agents.return_value = ["agent1"]
    mock_scan_rules.return_value = []
    mock_select_rules.return_value = ["rule1"]
    mock_scan_skills.return_value = []
    mock_select_skills.return_value = ["skill1"]
    mock_confirm.return_value.ask.return_value = True
    mock_export.return_value = {"agents": 1, "rules": 1, "skills": 1}

    run_scaffold_flow(tmp_path, tmp_path / "output")
    assert mock_export.called


@patch("questionary.text")
@patch("directive_cli.core.git_manager.add_submodule")
def test_run_add_submodule_flow(mock_add, mock_text, tmp_path):
    mock_text.return_value.ask.side_effect = ["https://github.com/org/repo.git", "repo"]
    mock_add.return_value = (True, "Added")

    run_add_submodule_flow(tmp_path)
    assert mock_add.called
