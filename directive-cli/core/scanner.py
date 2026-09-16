import os
import re
from pathlib import Path
from typing import List
from directive_cli.core.models import AgentItem, RuleItem, SkillItem, SkillGroup


def _extract_description_from_file(file_path: Path) -> str:
    """Extract first non-heading sentence or prompt excerpt."""
    if not file_path.is_file():
        return ""
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        lines = content.splitlines()

        # Check if file has YAML frontmatter
        if lines and lines[0].strip() == "---":
            for line in lines[1:]:
                line_clean = line.strip()
                if line_clean == "---":
                    break
                if line_clean.startswith("description:"):
                    return line_clean.replace("description:", "", 1).strip().strip('"\'')

        for line in lines:
            line_clean = line.strip()
            if not line_clean or line_clean.startswith("#") or line_clean.startswith("---"):
                continue
            if line_clean.startswith("description:"):
                return line_clean.replace("description:", "", 1).strip().strip('"\'')
            return line_clean[:100]
    except Exception:
        pass
    return ""


def scan_agents(base_dir: Path) -> List[AgentItem]:
    """Scan instructions/agents directory for agent packages."""
    agents: List[AgentItem] = []
    if not base_dir.is_dir():
        return agents

    for child in sorted(base_dir.iterdir()):
        if child.is_dir():
            agent_file = child / "agent.md"
            desc = _extract_description_from_file(agent_file) if agent_file.exists() else ""
            agents.append(AgentItem(name=child.name, source_path=child, description=desc))
    return agents


def scan_rules(base_dir: Path) -> List[RuleItem]:
    """Scan instructions/rules directory for *.rule.md or *.md files."""
    rules: List[RuleItem] = []
    if not base_dir.is_dir():
        return rules

    for child in sorted(base_dir.iterdir()):
        if child.is_file() and child.name.endswith(".md"):
            clean_name = re.sub(r"\.rule\.md$", "", child.name)
            clean_name = re.sub(r"\.md$", "", clean_name)
            rules.append(RuleItem(name=clean_name, source_path=child, filename=child.name))
    return rules


def _scan_submodule_skills(sub_dir: Path) -> List[SkillItem]:
    """Scan a single external submodule directory for folders containing SKILL.md."""
    skills: List[SkillItem] = []
    seen = set()
    if not sub_dir.is_dir():
        return skills

    for root, _, files in os.walk(sub_dir):
        if "SKILL.md" in files:
            current = Path(root)
            skill_name = sub_dir.name if current == sub_dir else current.name
            if skill_name in seen:
                continue
            seen.add(skill_name)
            skills.append(
                SkillItem(
                    source_group=sub_dir.name,
                    name=skill_name,
                    source_path=current,
                )
            )
    return skills


def scan_skills(active_dir: Path, external_dir: Path) -> List[SkillGroup]:
    """Scan active skills and external submodule skills."""
    groups: List[SkillGroup] = []

    # 1. Active skills
    if active_dir.is_dir():
        active_skills: List[SkillItem] = []
        for child in sorted(active_dir.iterdir()):
            if child.is_dir() and (child / "SKILL.md").exists():
                active_skills.append(
                    SkillItem(
                        source_group="active",
                        name=child.name,
                        source_path=child,
                    )
                )
        groups.append(
            SkillGroup(
                name="active (own)",
                raw_name="active",
                is_active=True,
                skills=active_skills,
            )
        )

    # 2. External submodules
    if external_dir.is_dir():
        for sub in sorted(external_dir.iterdir()):
            if sub.is_dir():
                sub_skills = _scan_submodule_skills(sub)
                groups.append(
                    SkillGroup(
                        name=sub.name,
                        raw_name=sub.name,
                        is_active=False,
                        skills=sub_skills,
                    )
                )

    return groups
