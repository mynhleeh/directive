from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class AgentItem:
    name: str
    source_path: Path
    description: str = ""


@dataclass
class RuleItem:
    name: str
    source_path: Path
    filename: str


@dataclass
class SkillItem:
    source_group: str
    name: str
    source_path: Path
    export_name: str = ""


@dataclass
class SkillGroup:
    name: str
    raw_name: str
    is_active: bool
    skills: List[SkillItem] = field(default_factory=list)
