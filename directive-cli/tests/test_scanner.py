from pathlib import Path
import pytest
from directive_cli.core.scanner import scan_agents, scan_rules, scan_skills


@pytest.fixture
def mock_instructions(tmp_path):
    # Setup agents
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()
    agent_a = agents_dir / "agent-a"
    agent_a.mkdir()
    (agent_a / "agent.md").write_text("# Agent A\nDescription for A", encoding="utf-8")

    # Setup rules
    rules_dir = tmp_path / "rules"
    rules_dir.mkdir()
    (rules_dir / "format.rule.md").write_text("# Formatting rule", encoding="utf-8")

    # Setup skills active
    skills_active = tmp_path / "skills" / "active"
    skills_active.mkdir(parents=True)
    my_skill = skills_active / "my-skill"
    my_skill.mkdir()
    (my_skill / "SKILL.md").write_text("---\nname: my-skill\n---", encoding="utf-8")

    # Setup skills external submodule
    skills_ext = tmp_path / "skills" / "external"
    sub1 = skills_ext / "sub1"
    sub1.mkdir(parents=True)
    sub1_skill = sub1 / "nested" / "ext-skill"
    sub1_skill.mkdir(parents=True)
    (sub1_skill / "SKILL.md").write_text("---\nname: ext-skill\n---", encoding="utf-8")

    return agents_dir, rules_dir, skills_active, skills_ext


def test_scanner_functions(mock_instructions):
    agents_dir, rules_dir, skills_active, skills_ext = mock_instructions

    # Test scan_agents
    agents = scan_agents(agents_dir)
    assert len(agents) == 1
    assert agents[0].name == "agent-a"
    assert "Description for A" in agents[0].description

    # Test scan_rules
    rules = scan_rules(rules_dir)
    assert len(rules) == 1
    assert rules[0].filename == "format.rule.md"
    assert rules[0].name == "format"

    # Test scan_skills
    groups = scan_skills(skills_active, skills_ext)
    assert len(groups) == 2

    # Group 1: active
    active_group = next(g for g in groups if g.is_active)
    assert active_group.raw_name == "active"
    assert len(active_group.skills) == 1
    assert active_group.skills[0].name == "my-skill"

    # Group 2: sub1
    sub1_group = next(g for g in groups if not g.is_active)
    assert sub1_group.raw_name == "sub1"
    assert len(sub1_group.skills) == 1
    assert sub1_group.skills[0].name == "ext-skill"


def test_scanner_edge_cases(tmp_path):
    # Non-existent directories
    assert scan_agents(tmp_path / "does_not_exist") == []
    assert scan_rules(tmp_path / "does_not_exist") == []
    assert scan_skills(tmp_path / "none1", tmp_path / "none2") == []

    # Agent without agent.md
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()
    empty_agent = agents_dir / "agent-empty"
    empty_agent.mkdir()
    agents = scan_agents(agents_dir)
    assert len(agents) == 1
    assert agents[0].name == "agent-empty"
    assert agents[0].description == ""

    # Frontmatter description in agent.md
    frontmatter_agent = agents_dir / "agent-frontmatter"
    frontmatter_agent.mkdir()
    (frontmatter_agent / "agent.md").write_text(
        "---\ndescription: \"An expert in coding\"\n---\n# Agent\nBody",
        encoding="utf-8",
    )
    agents = scan_agents(agents_dir)
    fm_item = next(a for a in agents if a.name == "agent-frontmatter")
    assert fm_item.description == "An expert in coding"

    # Rules with standard .md extension as well as .rule.md
    rules_dir = tmp_path / "rules"
    rules_dir.mkdir()
    (rules_dir / "plain.md").write_text("# Plain rule", encoding="utf-8")
    (rules_dir / "non_rule.txt").write_text("ignore me", encoding="utf-8")
    rules = scan_rules(rules_dir)
    assert len(rules) == 1
    assert rules[0].name == "plain"
    assert rules[0].filename == "plain.md"
