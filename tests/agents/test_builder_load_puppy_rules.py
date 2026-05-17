"""Tests for load_agent_rules() in coco_codes.agents._builder.

Covers the .coco_codes/ directory feature (PUP-34):
- Loading from .coco_codes/AGENTS.md (preferred)
- Precedence: .coco_codes/ over project root
- Backwards compatibility with root AGENTS.md
- Combining global + project rules
- Edge cases (dir is file, empty dir, etc.)
"""

from unittest.mock import patch

import pytest


class TestLoadPuppyRulesCocoCodesDir:
    """Tests for .coco_codes/ directory support in load_agent_rules()."""

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

    def test_load_from_coco_codes_dir(self, temp_project, mock_config_dir):
        """Load AGENTS.md from .coco_codes/ directory."""
        from coco_codes.agents._builder import load_agent_rules

        # Create .coco_codes/AGENTS.md
        coco_codes_dir = temp_project / ".coco_codes"
        coco_codes_dir.mkdir()
        agents_file = coco_codes_dir / "AGENTS.md"
        agents_file.write_text("# Rules from .coco_codes dir")

        with patch("coco_codes.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        assert result == "# Rules from .coco_codes dir"

    def test_precedence_coco_codes_over_root(self, temp_project, mock_config_dir):
        """Files in .coco_codes/ take precedence over project root."""
        from coco_codes.agents._builder import load_agent_rules

        # Create both locations
        coco_codes_dir = temp_project / ".coco_codes"
        coco_codes_dir.mkdir()
        (coco_codes_dir / "AGENTS.md").write_text("# Preferred rules")
        (temp_project / "AGENTS.md").write_text("# Root rules")

        with patch("coco_codes.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        # Should use .coco_codes/ version, NOT root
        assert result == "# Preferred rules"
        assert "Root rules" not in (result or "")

    def test_fallback_to_root(self, temp_project, mock_config_dir):
        """Fall back to root AGENTS.md if .coco_codes/ doesn't exist."""
        from coco_codes.agents._builder import load_agent_rules

        # Only create root AGENTS.md
        (temp_project / "AGENTS.md").write_text("# Root rules")

        with patch("coco_codes.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        assert result == "# Root rules"

    def test_global_and_coco_codes_combined(self, temp_project, mock_config_dir):
        """Global rules and .coco_codes rules are combined."""
        from coco_codes.agents._builder import load_agent_rules

        # Create global rules
        (mock_config_dir / "AGENTS.md").write_text("# Global rules")

        # Create .coco_codes rules
        coco_codes_dir = temp_project / ".coco_codes"
        coco_codes_dir.mkdir()
        (coco_codes_dir / "AGENTS.md").write_text("# Project rules")

        with patch("coco_codes.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        # Both should be present, global first
        assert "# Global rules" in result
        assert "# Project rules" in result
        assert result.index("# Global rules") < result.index("# Project rules")

    def test_global_and_root_combined(self, temp_project, mock_config_dir):
        """Global rules + root rules work together."""
        from coco_codes.agents._builder import load_agent_rules

        # Create global rules
        (mock_config_dir / "AGENTS.md").write_text("# Global rules")

        # Create root rules
        (temp_project / "AGENTS.md").write_text("# Root rules")

        with patch("coco_codes.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        # Both should be combined
        assert "# Global rules" in result
        assert "# Root rules" in result

    def test_coco_codes_is_file_not_dir(self, temp_project, mock_config_dir):
        """If .coco_codes is a file (not directory), fall back to root."""
        from coco_codes.agents._builder import load_agent_rules

        # Create .coco_codes as a FILE, not directory
        (temp_project / ".coco_codes").write_text("I'm a file, not a dir!")

        # Create root AGENTS.md as fallback
        (temp_project / "AGENTS.md").write_text("# Root fallback")

        with patch("coco_codes.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        # Should use root fallback
        assert result == "# Root fallback"

    def test_coco_codes_dir_exists_but_empty(self, temp_project, mock_config_dir):
        """Empty .coco_codes/ dir falls back to root AGENTS.md."""
        from coco_codes.agents._builder import load_agent_rules

        # Create empty .coco_codes directory
        (temp_project / ".coco_codes").mkdir()

        # Create root AGENTS.md as fallback
        (temp_project / "AGENTS.md").write_text("# Root fallback")

        with patch("coco_codes.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        # Should use root fallback
        assert result == "# Root fallback"

    def test_no_agents_files_anywhere(self, temp_project, mock_config_dir):
        """Returns None if no AGENTS.md files exist anywhere."""
        from coco_codes.agents._builder import load_agent_rules

        with patch("coco_codes.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        assert result is None

    def test_agent_md_variant_in_coco_codes_dir(self, temp_project, mock_config_dir):
        """Also supports AGENT.md (singular) in .coco_codes/."""
        from coco_codes.agents._builder import load_agent_rules

        coco_codes_dir = temp_project / ".coco_codes"
        coco_codes_dir.mkdir()
        # Use singular AGENT.md instead of AGENTS.md
        (coco_codes_dir / "AGENT.md").write_text("# Singular agent rules")

        with patch("coco_codes.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        assert result == "# Singular agent rules"

    def test_agents_md_takes_precedence_over_agent_md(
        self, temp_project, mock_config_dir
    ):
        """AGENTS.md (plural) takes precedence over AGENT.md (singular)."""
        from coco_codes.agents._builder import load_agent_rules

        coco_codes_dir = temp_project / ".coco_codes"
        coco_codes_dir.mkdir()
        (coco_codes_dir / "AGENTS.md").write_text("# Plural wins")
        (coco_codes_dir / "AGENT.md").write_text("# Singular loses")

        with patch("coco_codes.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        assert result == "# Plural wins"

    def test_only_global_rules(self, temp_project, mock_config_dir):
        """Only global rules loaded when no project rules exist."""
        from coco_codes.agents._builder import load_agent_rules

        # Create only global rules
        (mock_config_dir / "AGENTS.md").write_text("# Global only")

        with patch("coco_codes.agents._builder.CONFIG_DIR", str(mock_config_dir)):
            result = load_agent_rules()

        assert result == "# Global only"
