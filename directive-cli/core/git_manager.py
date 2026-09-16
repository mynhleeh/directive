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
