import os
import shutil
from pathlib import Path
from typing import Union, List, Dict

SOURCE: Union[List[str], str] = ["instructions/skills"]
EXCLUDE: Union[List[str], str] = []
DESTINATION: str = ".agents"

def to_paths(paths: Union[List[str], str]) -> List[Path]:
    if isinstance(paths, str): return [Path(paths).resolve()]
    return [Path(p).resolve() for p in paths]


def is_excluded(path: Path, excludes: List[Path]) -> bool:
    return any(path == ex or ex in path.parents for ex in excludes)


def find_skills(sources: List[Path], excludes: List[Path]) -> Dict[str, Path]:
    skills: Dict[str, Path] = {}

    for src in sources:
        if not src.is_dir(): continue

        for root, dirs, files in os.walk(src, topdown=True):
            current = Path(root)

            if is_excluded(current, excludes):
                dirs.clear()
                continue

            if "SKILL.md" in files:
                skill_name = current.name
                
                if skill_name in skills:
                    if current.stat().st_mtime > skills[skill_name].stat().st_mtime:
                        skills[skill_name] = current
                else:
                    skills[skill_name] = current
                
                dirs.clear()
    return skills


def extract_skills(source: Union[List[str], str], exclude: Union[List[str], str], destination: str) -> None:
    sources = to_paths(source)
    excludes = to_paths(exclude) if exclude else []
    target = Path(destination).resolve() / "skills"
    
    skills = find_skills(sources, excludes)
    if not skills:
        print("No skills found")
        return
        
    target.mkdir(parents=True, exist_ok=True)

    for name, path in skills.items():
        dest = target / name

        if dest.exists(): shutil.rmtree(dest)
        shutil.copytree(path, dest)

    print(f"Extracted {len(skills)} skills to {target}")

if __name__ == "__main__":
    extract_skills(SOURCE, EXCLUDE, DESTINATION)