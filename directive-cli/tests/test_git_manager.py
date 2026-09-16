from pathlib import Path
from unittest.mock import patch, MagicMock
import subprocess
from directive_cli.core.git_manager import (
    derive_submodule_name,
    sync_submodules,
    add_submodule,
    is_git_repo,
)


def test_derive_submodule_name():
    assert derive_submodule_name("https://github.com/org/my-skills.git") == "my-skills"
    assert derive_submodule_name("https://github.com/org/awesome-agent") == "awesome-agent"
    assert derive_submodule_name("git@github.com:org/tool.git") == "tool"


def test_is_git_repo(tmp_path):
    assert is_git_repo(tmp_path) is False
    (tmp_path / ".git").mkdir()
    assert is_git_repo(tmp_path) is True


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
def test_sync_submodules_failure(mock_run, tmp_path):
    mock_run.return_value = MagicMock(returncode=128, stdout="", stderr="fatal: unable to access network")
    success, msg = sync_submodules(tmp_path, timeout_seconds=5)
    assert success is False
    assert "Git error" in msg


@patch("subprocess.run")
def test_add_submodule_success(mock_run, tmp_path):
    mock_run.return_value = MagicMock(returncode=0, stdout="Added", stderr="")
    success, msg = add_submodule(tmp_path, "https://github.com/org/new-pack.git", custom_name="new-pack")
    assert success is True
    assert "new-pack" in msg


def test_add_submodule_destination_exists(tmp_path):
    dest = tmp_path / "instructions" / "skills" / "external" / "existing-pack"
    dest.mkdir(parents=True)
    success, msg = add_submodule(tmp_path, "https://github.com/org/existing-pack.git")
    assert success is False
    assert "already exists" in msg.lower()
