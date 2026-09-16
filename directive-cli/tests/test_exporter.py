from pathlib import Path
from directive_cli.core.models import AgentItem, RuleItem, SkillItem
from directive_cli.core.exporter import (
    make_prefix,
    resolve_skill_names,
    resolve_target_directory,
    export_scaffold,
)


def test_make_prefix():
    assert make_prefix("active") == "own"
    assert make_prefix("superpowers") == "sup"
    assert make_prefix("AI-Research-SKILLs") == "ars"
    assert make_prefix("ui-ux-pro-max-skill") == "uupms"


def test_resolve_skill_names_conflict():
    skill1 = SkillItem(source_group="active", name="commit", source_path=Path("active/commit"))
    skill2 = SkillItem(source_group="superpowers", name="commit", source_path=Path("ext/superpowers/commit"))
    skill3 = SkillItem(source_group="anthropics", name="unique-skill", source_path=Path("ext/anth/unique"))

    resolved = resolve_skill_names([skill1, skill2, skill3])
    # Conflict skills get prefix
    assert resolved[0].export_name == "own-commit"
    assert resolved[1].export_name == "sup-commit"
    # Unique skill keeps original name
    assert resolved[2].export_name == "unique-skill"


def test_resolve_target_directory():
    # If path already ends in .agents, keep it
    p1 = Path("/tmp/myproject/.agents")
    assert resolve_target_directory(p1) == p1

    # If path is arbitrary folder, append .agents
    p2 = Path("/tmp/myproject")
    assert resolve_target_directory(p2) == p2 / ".agents"


def test_export_scaffold(tmp_path):
    source_dir = tmp_path / "source"
    source_dir.mkdir()

    # Agent fixture
    agent_dir = source_dir / "agent1"
    agent_dir.mkdir()
    (agent_dir / "agent.md").write_text("agent content")
    agent = AgentItem(name="agent1", source_path=agent_dir)

    # Rule fixture
    rule_file = source_dir / "my.rule.md"
    rule_file.write_text("rule content")
    rule = RuleItem(name="my", source_path=rule_file, filename="my.rule.md")

    # Skill fixture
    skill_dir = source_dir / "skill1"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("skill content")
    skill = SkillItem(source_group="active", name="skill1", source_path=skill_dir, export_name="skill1")

    target = tmp_path / "output_test"
    counts = export_scaffold(target, agents=[agent], rules=[rule], skills=[skill])

    assert counts["agents"] == 1
    assert counts["rules"] == 1
    assert counts["skills"] == 1

    resolved_target = target / ".agents"
    assert (resolved_target / "agents" / "agent1" / "agent.md").exists()
    assert (resolved_target / "rules" / "my.rule.md").exists()
    assert (resolved_target / "skills" / "skill1" / "SKILL.md").exists()


def test_export_scaffold_empty_and_overwrite(tmp_path):
    # Empty lists
    target = tmp_path / "empty_target"
    counts = export_scaffold(target, agents=[], rules=[], skills=[])
    assert counts == {"agents": 0, "rules": 0, "skills": 0}

    # Overwrite test
    source_dir = tmp_path / "source2"
    source_dir.mkdir()
    skill_dir = source_dir / "skill1"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("v1")
    skill = SkillItem(source_group="active", name="skill1", source_path=skill_dir)

    export_scaffold(target, agents=[], rules=[], skills=[skill])
    assert (target / ".agents" / "skills" / "skill1" / "SKILL.md").read_text() == "v1"

    # Overwrite with v2
    (skill_dir / "SKILL.md").write_text("v2")
    export_scaffold(target, agents=[], rules=[], skills=[skill])
    assert (target / ".agents" / "skills" / "skill1" / "SKILL.md").read_text() == "v2"


def test_export_scaffold_replace_file_with_dir(tmp_path):
    # Destination already has a file where a directory should be copied
    source_dir = tmp_path / "source3"
    source_dir.mkdir()
    skill_dir = source_dir / "dir_skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("dir content")
    skill = SkillItem(source_group="active", name="dir_skill", source_path=skill_dir)

    target = tmp_path / "target_file_conflict"
    dest_file = target / ".agents" / "skills" / "dir_skill"
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    dest_file.write_text("i am an unexpected file")

    export_scaffold(target, agents=[], rules=[], skills=[skill])
    assert dest_file.is_dir()
    assert (dest_file / "SKILL.md").read_text() == "dir content"

