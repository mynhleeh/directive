import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

ACTIVE_PATH = Path("instructions/skills/active")
EXTERNAL_PATH = Path("instructions/skills/external")
TARGET_PATH = Path(".agents/skills")


def make_prefix(name: str) -> str:
    if name == "active":
        return "own"
    parts = [p for p in re.split(r"[-_]+", name) if p]
    if len(parts) == 1:
        return parts[0][:3].lower()
    return "".join(p[0].lower() for p in parts)


def find_active_skills(dir_path: Path) -> List[Tuple[str, str, Path]]:
    skills = []
    if not dir_path.is_dir():
        return skills
    for child in dir_path.iterdir():
        if child.is_dir() and (child / "SKILL.md").exists():
            skills.append(("active", child.name, child))
    return skills


def find_submodule_skills(sub_dir: Path) -> List[Tuple[str, str, Path]]:
    skills = []
    seen = set()
    if not sub_dir.is_dir():
        return skills
    for root, dirs, files in os.walk(sub_dir):
        if "SKILL.md" in files:
            current = Path(root)
            skill_name = sub_dir.name if current == sub_dir else current.name
            if skill_name in seen:
                continue
            seen.add(skill_name)
            skills.append((sub_dir.name, skill_name, current))
    return skills


def find_all_skills(active_dir: Path, external_dir: Path) -> List[Tuple[str, str, Path]]:
    skills = []
    skills.extend(find_active_skills(active_dir))
    if external_dir.is_dir():
        for sub in sorted(external_dir.iterdir()):
            if sub.is_dir():
                skills.extend(find_submodule_skills(sub))
    return skills


def count_names(skills: List[Tuple[str, str, Path]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for _, name, _ in skills:
        counts[name] = counts.get(name, 0) + 1
    return counts


def build_skill_name(source: str, name: str, is_duplicate: bool) -> str:
    if not is_duplicate:
        return name
    return f"{make_prefix(source)}-{name}"


def build_export_map(skills: List[Tuple[str, str, Path]]) -> Dict[str, Path]:
    counts = count_names(skills)
    export_map: Dict[str, Path] = {}
    for source, name, path in skills:
        dest_name = build_skill_name(source, name, counts[name] > 1)
        export_map[dest_name] = path
    return export_map


def clear_directory(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_skill(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def export_skills(skills_map: Dict[str, Path], target_dir: Path) -> None:
    clear_directory(target_dir)
    for name, path in skills_map.items():
        copy_skill(path, target_dir / name)


def main() -> None:
    skills = find_all_skills(ACTIVE_PATH, EXTERNAL_PATH)
    skills_map = build_export_map(skills)
    export_skills(skills_map, TARGET_PATH)
    print(f"Exported {len(skills_map)} skills to {TARGET_PATH}")


if __name__ == "__main__":
    main()