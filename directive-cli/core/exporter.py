import re
import shutil
from collections import Counter
from pathlib import Path
from typing import Dict, List
from directive_cli.core.models import AgentItem, RuleItem, SkillItem


def make_prefix(name: str) -> str:
    """Generate source group prefix identical to legacy extract_skills.py."""
    if name == "active":
        return "own"
    parts = [p for p in re.split(r"[-_]+", name) if p]
    if len(parts) == 1:
        return parts[0][:3].lower()
    return "".join(p[0].lower() for p in parts)


def resolve_skill_names(skills: List[SkillItem]) -> List[SkillItem]:
    """Attach export_name with prefix if duplicate skill names exist."""
    name_counts = Counter(s.name for s in skills)
    resolved: List[SkillItem] = []

    for skill in skills:
        if name_counts[skill.name] > 1:
            skill.export_name = f"{make_prefix(skill.source_group)}-{skill.name}"
        else:
            skill.export_name = skill.name
        resolved.append(skill)
    return resolved


def resolve_target_directory(target_path: Path) -> Path:
    """Ensure target directory resolves to a .agents directory."""
    if target_path.name == ".agents":
        return target_path
    return target_path / ".agents"


def _copy_item(src: Path, dst: Path) -> None:
    """Copy file or directory recursively, replacing destination if exists."""
    if src.is_dir():
        if dst.is_dir():
            shutil.rmtree(dst)
        elif dst.is_file():
            dst.unlink()
        shutil.copytree(src, dst)
    elif src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def export_scaffold(
    target_dir: Path,
    agents: List[AgentItem],
    rules: List[RuleItem],
    skills: List[SkillItem],
) -> Dict[str, int]:
    """Export selected agents, rules, and skills into target .agents directory."""
    dest_agents_root = resolve_target_directory(target_dir)

    counts = {"agents": 0, "rules": 0, "skills": 0}

    # 1. Export agents if any selected
    if agents:
        agents_dest = dest_agents_root / "agents"
        agents_dest.mkdir(parents=True, exist_ok=True)
        for agent in agents:
            _copy_item(agent.source_path, agents_dest / agent.name)
            counts["agents"] += 1

    # 2. Export rules if any selected
    if rules:
        rules_dest = dest_agents_root / "rules"
        rules_dest.mkdir(parents=True, exist_ok=True)
        for rule in rules:
            _copy_item(rule.source_path, rules_dest / rule.filename)
            counts["rules"] += 1

    # 3. Export skills if any selected
    if skills:
        skills_dest = dest_agents_root / "skills"
        skills_dest.mkdir(parents=True, exist_ok=True)
        resolved_skills = resolve_skill_names(skills)
        for skill in resolved_skills:
            _copy_item(skill.source_path, skills_dest / skill.export_name)
            counts["skills"] += 1

    return counts
