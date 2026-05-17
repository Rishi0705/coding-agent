"""Tests for load_agent_rules() in coding_agent.agents._builder.

Covers the .coding_agent/ directory feature (PUP-34):
- Loading from .coding_agent/AGENTS.md (preferred)
- Precedence: .coding_agent/ over project root
- Backwards compatibility with root AGENTS.md
- Combining global + project rules
- Edge cases (dir is file, empty dir, etc.)
"""

from unittest.mock import patch

import pytest


class TestLoadPuppyRulesCodingAgentDir:
    """Tests for .coding_agent/ directory support in load_agent_rules()."""

    @pytest.fixture
    def temp_project(self, tmp_path, monkeypatch):
        """Set up a temporary project directory and cd into it."""
        monkeypatch.chdir(tmp_path)
        return tmp_path

    @pytest.fixture
    def mock_config_dir(self, tmp_path):
        """Create a mock global config directory."""
        config_dir = tmp_path / "global_config"
        config_dir.mkdir()
        return config_dir

    def test_load_from_coding_agent_dir(self, temp_project, mock_config_dir):
        """Load AGENTS.md from .coding_agent/ directory."""
        from coding_agent.agents._builder import load_agent_rules

        # Create .coding_agent/AGENTS.md
        coding_agent_dir = temp_project / ".coding_agent"
        coding_agent_dir.mkdir()
        agents_file = coding_agent_dir / "AGENTS.md"
        agents_file.write_text("# Rules from .coding_agent dir")

        with patch("coding_agent.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        assert result == "# Rules from .coding_agent dir"

    def test_precedence_coding_agent_over_root(self, temp_project, mock_config_dir):
        """Files in .coding_agent/ take precedence over project root."""
        from coding_agent.agents._builder import load_agent_rules

        # Create both locations
        coding_agent_dir = temp_project / ".coding_agent"
        coding_agent_dir.mkdir()
        (coding_agent_dir / "AGENTS.md").write_text("# Preferred rules")
        (temp_project / "AGENTS.md").write_text("# Root rules")

        with patch("coding_agent.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        # Should use .coding_agent/ version, NOT root
        assert result == "# Preferred rules"
        assert "Root rules" not in (result or "")

    def test_fallback_to_root(self, temp_project, mock_config_dir):
        """Fall back to root AGENTS.md if .coding_agent/ doesn't exist."""
        from coding_agent.agents._builder import load_agent_rules

        # Only create root AGENTS.md
        (temp_project / "AGENTS.md").write_text("# Root rules")

        with patch("coding_agent.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        assert result == "# Root rules"

    def test_global_and_coding_agent_combined(self, temp_project, mock_config_dir):
        """Global rules and .coding_agent rules are combined."""
        from coding_agent.agents._builder import load_agent_rules

        # Create global rules
        (mock_config_dir / "AGENTS.md").write_text("# Global rules")

        # Create .coding_agent rules
        coding_agent_dir = temp_project / ".coding_agent"
        coding_agent_dir.mkdir()
        (coding_agent_dir / "AGENTS.md").write_text("# Project rules")

        with patch("coding_agent.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        # Both should be present, global first
        assert "# Global rules" in result
        assert "# Project rules" in result
        assert result.index("# Global rules") < result.index("# Project rules")

    def test_global_and_root_combined(self, temp_project, mock_config_dir):
        """Global rules + root rules work together."""
        from coding_agent.agents._builder import load_agent_rules

        # Create global rules
        (mock_config_dir / "AGENTS.md").write_text("# Global rules")

        # Create root rules
        (temp_project / "AGENTS.md").write_text("# Root rules")

        with patch("coding_agent.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        # Both should be combined
        assert "# Global rules" in result
        assert "# Root rules" in result

    def test_coding_agent_is_file_not_dir(self, temp_project, mock_config_dir):
        """If .coding_agent is a file (not directory), fall back to root."""
        from coding_agent.agents._builder import load_agent_rules

        # Create .coding_agent as a FILE, not directory
        (temp_project / ".coding_agent").write_text("I'm a file, not a dir!")

        # Create root AGENTS.md as fallback
        (temp_project / "AGENTS.md").write_text("# Root fallback")

        with patch("coding_agent.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        # Should use root fallback
        assert result == "# Root fallback"

    def test_coding_agent_dir_exists_but_empty(self, temp_project, mock_config_dir):
        """Empty .coding_agent/ dir falls back to root AGENTS.md."""
        from coding_agent.agents._builder import load_agent_rules

        # Create empty .coding_agent directory
        (temp_project / ".coding_agent").mkdir()

        # Create root AGENTS.md as fallback
        (temp_project / "AGENTS.md").write_text("# Root fallback")

        with patch("coding_agent.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        # Should use root fallback
        assert result == "# Root fallback"

    def test_no_agents_files_anywhere(self, temp_project, mock_config_dir):
        """Returns None if no AGENTS.md files exist anywhere."""
        from coding_agent.agents._builder import load_agent_rules

        with patch("coding_agent.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        assert result is None

    def test_agent_md_variant_in_coding_agent_dir(self, temp_project, mock_config_dir):
        """Also supports AGENT.md (singular) in .coding_agent/."""
        from coding_agent.agents._builder import load_agent_rules

        coding_agent_dir = temp_project / ".coding_agent"
        coding_agent_dir.mkdir()
        # Use singular AGENT.md instead of AGENTS.md
        (coding_agent_dir / "AGENT.md").write_text("# Singular agent rules")

        with patch("coding_agent.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        assert result == "# Singular agent rules"

    def test_agents_md_takes_precedence_over_agent_md(
        self, temp_project, mock_config_dir
    ):
        """AGENTS.md (plural) takes precedence over AGENT.md (singular)."""
        from coding_agent.agents._builder import load_agent_rules

        coding_agent_dir = temp_project / ".coding_agent"
        coding_agent_dir.mkdir()
        (coding_agent_dir / "AGENTS.md").write_text("# Plural wins")
        (coding_agent_dir / "AGENT.md").write_text("# Singular loses")

        with patch("coding_agent.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        assert result == "# Plural wins"

    def test_only_global_rules(self, temp_project, mock_config_dir):
        """Only global rules loaded when no project rules exist."""
        from coding_agent.agents._builder import load_agent_rules

        # Create only global rules
        (mock_config_dir / "AGENTS.md").write_text("# Global only")

        with patch("coding_agent.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        assert result == "# Global only"
