from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_AGENTS_SOURCE = REPO_ROOT / "instructions" / "agents"
DEFAULT_RULES_SOURCE = REPO_ROOT / "instructions" / "rules"
DEFAULT_SKILLS_ACTIVE = REPO_ROOT / "instructions" / "skills" / "active"
DEFAULT_SKILLS_EXTERNAL = REPO_ROOT / "instructions" / "skills" / "external"

DEFAULT_OUTPUT_DIR = REPO_ROOT / "directive-cli" / "output"
SUBMODULE_TIMEOUT_SECONDS = 15
