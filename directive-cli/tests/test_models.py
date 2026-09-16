from pathlib import Path
from directive_cli.core.models import AgentItem, RuleItem, SkillItem, SkillGroup
from directive_cli import config


def test_models_instantiation():
    agent = AgentItem(name="omni", source_path=Path("instructions/agents/omni"), description="Omni agent")
    assert agent.name == "omni"
    assert agent.description == "Omni agent"

    rule = RuleItem(name="file-org", source_path=Path("instructions/rules/rule.md"), filename="rule.md")
    assert rule.name == "file-org"
    assert rule.filename == "rule.md"

    skill = SkillItem(source_group="active", name="git-workflow", source_path=Path("active/git-workflow"))
    assert skill.export_name == ""
    assert skill.source_group == "active"

    group = SkillGroup(name="active (own)", raw_name="active", is_active=True, skills=[skill])
    assert len(group.skills) == 1
    assert group.is_active is True


def test_config_paths_exist_as_paths():
    assert isinstance(config.DEFAULT_OUTPUT_DIR, Path)
    assert config.DEFAULT_OUTPUT_DIR.name == "output"
    assert isinstance(config.DEFAULT_AGENTS_SOURCE, Path)
    assert isinstance(config.DEFAULT_RULES_SOURCE, Path)
    assert isinstance(config.DEFAULT_SKILLS_ACTIVE, Path)
    assert isinstance(config.DEFAULT_SKILLS_EXTERNAL, Path)
