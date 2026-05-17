"""Full coverage tests for coding_agent/command_line/config_commands.py."""

import json
from unittest.mock import MagicMock, mock_open, patch


class TestGetCommandsHelp:
    def test_lazy_import(self):
        from coding_agent.command_line.config_commands import get_commands_help

        with patch(
            "coding_agent.command_line.command_handler.get_commands_help",
            return_value="help text",
        ):
            assert get_commands_help() == "help text"


class TestHandleShowCommand:
    def _show_patches(self, effective_temp=0.7, global_temp=0.7, yolo=True):
        """Return a context manager patching all lazy imports in handle_show_command."""
        mock_agent = MagicMock()
        mock_agent.display_name = "Test Agent"
        return [
            patch("coding_agent.agents.get_current_agent", return_value=mock_agent),
            patch(
                "coding_agent.command_line.model_picker_completion.get_active_model",
                return_value="gpt-5",
            ),
            patch("coding_agent.config.get_assistant_name", return_value="Pup"),
            patch("coding_agent.config.get_owner_name", return_value="Owner"),
            patch("coding_agent.config.get_yolo_mode", return_value=yolo),
            patch("coding_agent.config.get_auto_save_session", return_value=True),
            patch("coding_agent.config.get_protected_token_count", return_value=50000),
            patch("coding_agent.config.get_compaction_threshold", return_value=0.85),
            patch(
                "coding_agent.config.get_compaction_strategy", return_value="truncation"
            ),
            patch("coding_agent.config.get_temperature", return_value=global_temp),
            patch(
                "coding_agent.config.get_effective_temperature",
                return_value=effective_temp,
            ),
            patch("coding_agent.config.get_default_agent", return_value="coding-agent"),
            patch("coding_agent.config.get_resume_message_count", return_value=50),
            patch(
                "coding_agent.config.get_openai_reasoning_effort", return_value="medium"
            ),
            patch("coding_agent.config.get_openai_verbosity", return_value="medium"),
            patch(
                "coding_agent.keymap.get_cancel_agent_display_name", return_value="ctrl+c"
            ),
            patch("coding_agent.messaging.emit_info"),
        ]

    def test_show_command(self):
        from coding_agent.command_line.config_commands import handle_show_command

        patches = self._show_patches()
        with (
            patches[0],
            patches[1],
            patches[2],
            patches[3],
            patches[4],
            patches[5],
            patches[6],
            patches[7],
            patches[8],
            patches[9],
            patches[10],
            patches[11],
            patches[12],
            patches[13],
            patches[14],
            patches[15],
            patches[16],
        ):
            assert handle_show_command("/show") is True

    def test_show_effective_temp_none(self):
        from coding_agent.command_line.config_commands import handle_show_command

        patches = self._show_patches(effective_temp=None, global_temp=None)
        with (
            patches[0],
            patches[1],
            patches[2],
            patches[3],
            patches[4],
            patches[5],
            patches[6],
            patches[7],
            patches[8],
            patches[9],
            patches[10],
            patches[11],
            patches[12],
            patches[13],
            patches[14],
            patches[15],
            patches[16],
        ):
            assert handle_show_command("/show") is True


class TestHandleReasoningCommand:
    def test_no_args(self):
        from coding_agent.command_line.config_commands import handle_reasoning_command

        with patch("coding_agent.messaging.emit_warning") as warn:
            assert handle_reasoning_command("/reasoning") is True
            warn.assert_called_once()

    def test_valid(self):
        from coding_agent.command_line.config_commands import handle_reasoning_command

        mock_agent = MagicMock()
        with (
            patch("coding_agent.config.set_openai_reasoning_effort"),
            patch("coding_agent.config.get_openai_reasoning_effort", return_value="high"),
            patch(
                "coding_agent.agents.agent_manager.get_current_agent",
                return_value=mock_agent,
            ),
            patch("coding_agent.messaging.emit_success"),
        ):
            assert handle_reasoning_command("/reasoning high") is True

    def test_invalid(self):
        from coding_agent.command_line.config_commands import handle_reasoning_command

        with (
            patch(
                "coding_agent.config.set_openai_reasoning_effort",
                side_effect=ValueError("bad"),
            ),
            patch("coding_agent.messaging.emit_error") as err,
        ):
            assert handle_reasoning_command("/reasoning bad") is True
            err.assert_called_once()


class TestHandleVerbosityCommand:
    def test_no_args(self):
        from coding_agent.command_line.config_commands import handle_verbosity_command

        with patch("coding_agent.messaging.emit_warning"):
            assert handle_verbosity_command("/verbosity") is True

    def test_valid(self):
        from coding_agent.command_line.config_commands import handle_verbosity_command

        mock_agent = MagicMock()
        with (
            patch("coding_agent.config.set_openai_verbosity"),
            patch("coding_agent.config.get_openai_verbosity", return_value="low"),
            patch(
                "coding_agent.agents.agent_manager.get_current_agent",
                return_value=mock_agent,
            ),
            patch("coding_agent.messaging.emit_success"),
        ):
            assert handle_verbosity_command("/verbosity low") is True

    def test_invalid(self):
        from coding_agent.command_line.config_commands import handle_verbosity_command

        with (
            patch(
                "coding_agent.config.set_openai_verbosity", side_effect=ValueError("bad")
            ),
            patch("coding_agent.messaging.emit_error"),
        ):
            assert handle_verbosity_command("/verbosity bad") is True


class TestHandleSetCommand:
    def test_no_args_shows_help(self):
        from coding_agent.command_line.config_commands import handle_set_command

        with patch("coding_agent.messaging.emit_warning"):
            assert handle_set_command("/set") is True

    def test_equals_syntax(self):
        from coding_agent.command_line.config_commands import handle_set_command

        mock_agent = MagicMock()
        with (
            patch("coding_agent.config.set_config_value"),
            patch("coding_agent.messaging.emit_success"),
            patch("coding_agent.messaging.emit_info"),
            patch("coding_agent.agents.get_current_agent", return_value=mock_agent),
        ):
            assert handle_set_command("/set key=value") is True

    def test_space_syntax(self):
        from coding_agent.command_line.config_commands import handle_set_command

        mock_agent = MagicMock()
        with (
            patch("coding_agent.config.set_config_value"),
            patch("coding_agent.messaging.emit_success"),
            patch("coding_agent.messaging.emit_info"),
            patch("coding_agent.agents.get_current_agent", return_value=mock_agent),
        ):
            assert handle_set_command("/set key value") is True

    def test_key_only(self):
        from coding_agent.command_line.config_commands import handle_set_command

        mock_agent = MagicMock()
        with (
            patch("coding_agent.config.set_config_value"),
            patch("coding_agent.messaging.emit_success"),
            patch("coding_agent.messaging.emit_info"),
            patch("coding_agent.agents.get_current_agent", return_value=mock_agent),
        ):
            assert handle_set_command("/set key") is True

    def test_enable_dbos(self):
        from coding_agent.command_line.config_commands import handle_set_command

        mock_agent = MagicMock()
        with (
            patch("coding_agent.config.set_config_value"),
            patch("coding_agent.messaging.emit_success"),
            patch("coding_agent.messaging.emit_info"),
            patch("coding_agent.agents.get_current_agent", return_value=mock_agent),
        ):
            assert handle_set_command("/set enable_dbos true") is True

    def test_cancel_agent_key_valid(self):
        from coding_agent.command_line.config_commands import handle_set_command

        mock_agent = MagicMock()
        with (
            patch("coding_agent.config.set_config_value"),
            patch("coding_agent.messaging.emit_success"),
            patch("coding_agent.messaging.emit_info"),
            patch(
                "coding_agent.keymap.VALID_CANCEL_KEYS", {"ctrl+c", "ctrl+k", "ctrl+q"}
            ),
            patch("coding_agent.agents.get_current_agent", return_value=mock_agent),
        ):
            assert handle_set_command("/set cancel_agent_key ctrl+c") is True

    def test_cancel_agent_key_invalid(self):
        from coding_agent.command_line.config_commands import handle_set_command

        with (
            patch(
                "coding_agent.keymap.VALID_CANCEL_KEYS", {"ctrl+c", "ctrl+k", "ctrl+q"}
            ),
            patch("coding_agent.messaging.emit_error") as err,
        ):
            assert handle_set_command("/set cancel_agent_key bad_key") is True
            err.assert_called_once()

    def test_agent_reload_failure(self):
        from coding_agent.command_line.config_commands import handle_set_command

        mock_agent = MagicMock()
        mock_agent.reload_code_generation_agent.side_effect = Exception("boom")
        with (
            patch("coding_agent.config.set_config_value"),
            patch("coding_agent.messaging.emit_success"),
            patch("coding_agent.messaging.emit_info"),
            patch("coding_agent.messaging.emit_warning") as warn,
            patch("coding_agent.agents.get_current_agent", return_value=mock_agent),
        ):
            assert handle_set_command("/set key value") is True
            warn.assert_called_once()


class TestGetJsonAgentsPinnedToModel:
    def test_returns_pinned(self, tmp_path):
        from coding_agent.command_line.config_commands import (
            _get_json_agents_pinned_to_model,
        )

        agent_file = tmp_path / "agent.json"
        agent_file.write_text(json.dumps({"model": "gpt-5"}))
        with patch(
            "coding_agent.agents.json_agent.discover_json_agents",
            return_value={"test": str(agent_file)},
        ):
            result = _get_json_agents_pinned_to_model("gpt-5")
            assert "test" in result

    def test_skips_errors(self, tmp_path):
        from coding_agent.command_line.config_commands import (
            _get_json_agents_pinned_to_model,
        )

        with patch(
            "coding_agent.agents.json_agent.discover_json_agents",
            return_value={"bad": "/nonexistent/path.json"},
        ):
            result = _get_json_agents_pinned_to_model("gpt-5")
            assert result == []


class TestHandlePinModelCommand:
    def _make_patches(self, **overrides):
        defaults = {
            "discover_json_agents": {},
            "load_model_names": ["gpt-5", "claude"],
            "get_agent_descriptions": {"coding-agent": "Default agent"},
        }
        defaults.update(overrides)
        return [
            patch(
                "coding_agent.agents.json_agent.discover_json_agents",
                return_value=defaults["discover_json_agents"],
            ),
            patch(
                "coding_agent.command_line.model_picker_completion.load_model_names",
                return_value=defaults["load_model_names"],
            ),
            patch(
                "coding_agent.agents.agent_manager.get_agent_descriptions",
                return_value=defaults["get_agent_descriptions"],
            ),
        ]

    def test_no_args_shows_help(self):
        from coding_agent.command_line.config_commands import handle_pin_model_command

        patches = self._make_patches()
        with (
            patches[0],
            patches[1],
            patches[2],
            patch("coding_agent.messaging.emit_warning"),
            patch("coding_agent.messaging.emit_info"),
        ):
            assert handle_pin_model_command("/pin_model") is True

    def test_unpin_delegation(self):
        from coding_agent.command_line.config_commands import handle_pin_model_command

        patches = self._make_patches()
        with (
            patches[0],
            patches[1],
            patches[2],
            patch(
                "coding_agent.command_line.config_commands.handle_unpin_command",
                return_value=True,
            ) as unpin,
        ):
            assert handle_pin_model_command("/pin_model agent (unpin)") is True
            unpin.assert_called_once()

    def test_model_not_found(self):
        from coding_agent.command_line.config_commands import handle_pin_model_command

        patches = self._make_patches()
        with (
            patches[0],
            patches[1],
            patches[2],
            patch("coding_agent.messaging.emit_error"),
            patch("coding_agent.messaging.emit_warning"),
        ):
            assert handle_pin_model_command("/pin_model agent nonexistent") is True

    def test_agent_not_found(self):
        from coding_agent.command_line.config_commands import handle_pin_model_command

        patches = self._make_patches()
        with (
            patches[0],
            patches[1],
            patches[2],
            patch("coding_agent.messaging.emit_error"),
            patch("coding_agent.messaging.emit_info"),
        ):
            assert handle_pin_model_command("/pin_model unknown gpt-5") is True

    def test_pin_builtin_agent(self):
        from coding_agent.command_line.config_commands import handle_pin_model_command

        mock_agent = MagicMock()
        mock_agent.name = "coding-agent"
        patches = self._make_patches()
        with (
            patches[0],
            patches[1],
            patches[2],
            patch("coding_agent.config.set_agent_pinned_model"),
            patch("coding_agent.messaging.emit_success"),
            patch("coding_agent.messaging.emit_info"),
            patch("coding_agent.agents.get_current_agent", return_value=mock_agent),
        ):
            assert handle_pin_model_command("/pin_model coding-agent gpt-5") is True

    def test_pin_json_agent(self, tmp_path):
        from coding_agent.command_line.config_commands import handle_pin_model_command

        agent_file = tmp_path / "agent.json"
        agent_file.write_text(json.dumps({"name": "test"}))
        mock_agent = MagicMock()
        mock_agent.name = "other"
        patches = self._make_patches(discover_json_agents={"test": str(agent_file)})
        with (
            patches[0],
            patches[1],
            patches[2],
            patch("coding_agent.messaging.emit_success"),
            patch("coding_agent.messaging.emit_info"),
            patch("coding_agent.agents.get_current_agent", return_value=mock_agent),
        ):
            assert handle_pin_model_command("/pin_model test gpt-5") is True
            data = json.loads(agent_file.read_text())
            assert data["model"] == "gpt-5"

    def test_pin_current_json_agent_reloads(self, tmp_path):
        from coding_agent.command_line.config_commands import handle_pin_model_command

        agent_file = tmp_path / "agent.json"
        agent_file.write_text(json.dumps({"name": "test"}))
        mock_agent = MagicMock()
        mock_agent.name = "test"
        mock_agent.refresh_config = MagicMock()
        patches = self._make_patches(discover_json_agents={"test": str(agent_file)})
        with (
            patches[0],
            patches[1],
            patches[2],
            patch("coding_agent.messaging.emit_success"),
            patch("coding_agent.messaging.emit_info"),
            patch("coding_agent.agents.get_current_agent", return_value=mock_agent),
        ):
            assert handle_pin_model_command("/pin_model test gpt-5") is True
            mock_agent.refresh_config.assert_called_once()

    def test_pin_exception(self, tmp_path):
        from coding_agent.command_line.config_commands import handle_pin_model_command

        patches = self._make_patches(discover_json_agents={"test": "/bad/path.json"})
        with (
            patches[0],
            patches[1],
            patches[2],
            patch("coding_agent.messaging.emit_error"),
        ):
            assert handle_pin_model_command("/pin_model test gpt-5") is True


class TestHandleUnpinCommand:
    def test_no_args(self):
        from coding_agent.command_line.config_commands import handle_unpin_command

        with (
            patch("coding_agent.agents.json_agent.discover_json_agents", return_value={}),
            patch(
                "coding_agent.agents.agent_manager.get_agent_descriptions",
                return_value={"a": "desc"},
            ),
            patch("coding_agent.config.get_agent_pinned_model", return_value=None),
            patch("coding_agent.messaging.emit_warning"),
            patch("coding_agent.messaging.emit_info"),
        ):
            assert handle_unpin_command("/unpin") is True

    def test_no_args_with_pinned(self):
        from coding_agent.command_line.config_commands import handle_unpin_command

        agent_file_content = json.dumps({"model": "gpt-5"})
        with (
            patch(
                "coding_agent.agents.json_agent.discover_json_agents",
                return_value={"j": "/f.json"},
            ),
            patch(
                "coding_agent.agents.agent_manager.get_agent_descriptions",
                return_value={"a": "desc"},
            ),
            patch("coding_agent.config.get_agent_pinned_model", return_value="gpt-5"),
            patch("builtins.open", mock_open(read_data=agent_file_content)),
            patch("coding_agent.messaging.emit_warning"),
            patch("coding_agent.messaging.emit_info"),
        ):
            assert handle_unpin_command("/unpin") is True

    def test_agent_not_found(self):
        from coding_agent.command_line.config_commands import handle_unpin_command

        with (
            patch("coding_agent.agents.json_agent.discover_json_agents", return_value={}),
            patch(
                "coding_agent.agents.agent_manager.get_agent_descriptions",
                return_value={},
            ),
            patch("coding_agent.messaging.emit_error"),
        ):
            assert handle_unpin_command("/unpin unknown") is True

    def test_unpin_builtin(self):
        from coding_agent.command_line.config_commands import handle_unpin_command

        mock_agent = MagicMock()
        mock_agent.name = "coding-agent"
        with (
            patch("coding_agent.agents.json_agent.discover_json_agents", return_value={}),
            patch(
                "coding_agent.agents.agent_manager.get_agent_descriptions",
                return_value={"coding-agent": "desc"},
            ),
            patch("coding_agent.config.clear_agent_pinned_model"),
            patch("coding_agent.messaging.emit_success"),
            patch("coding_agent.agents.get_current_agent", return_value=mock_agent),
            patch("coding_agent.messaging.emit_info"),
        ):
            assert handle_unpin_command("/unpin coding-agent") is True

    def test_unpin_json_agent(self, tmp_path):
        from coding_agent.command_line.config_commands import handle_unpin_command

        agent_file = tmp_path / "agent.json"
        agent_file.write_text(json.dumps({"name": "test", "model": "gpt-5"}))
        mock_agent = MagicMock()
        mock_agent.name = "other"
        with (
            patch(
                "coding_agent.agents.json_agent.discover_json_agents",
                return_value={"test": str(agent_file)},
            ),
            patch(
                "coding_agent.agents.agent_manager.get_agent_descriptions",
                return_value={},
            ),
            patch("coding_agent.messaging.emit_success"),
            patch("coding_agent.agents.get_current_agent", return_value=mock_agent),
        ):
            assert handle_unpin_command("/unpin test") is True
            data = json.loads(agent_file.read_text())
            assert "model" not in data

    def test_unpin_exception(self):
        from coding_agent.command_line.config_commands import handle_unpin_command

        with (
            patch(
                "coding_agent.agents.json_agent.discover_json_agents",
                return_value={"test": "/bad.json"},
            ),
            patch(
                "coding_agent.agents.agent_manager.get_agent_descriptions",
                return_value={},
            ),
            patch("coding_agent.messaging.emit_error"),
        ):
            assert handle_unpin_command("/unpin test") is True

    def test_unpin_current_agent_reload_failure(self, tmp_path):
        from coding_agent.command_line.config_commands import handle_unpin_command

        agent_file = tmp_path / "agent.json"
        agent_file.write_text(json.dumps({"name": "test", "model": "gpt-5"}))
        mock_agent = MagicMock()
        mock_agent.name = "test"
        mock_agent.reload_code_generation_agent.side_effect = Exception("boom")
        with (
            patch(
                "coding_agent.agents.json_agent.discover_json_agents",
                return_value={"test": str(agent_file)},
            ),
            patch(
                "coding_agent.agents.agent_manager.get_agent_descriptions",
                return_value={},
            ),
            patch("coding_agent.messaging.emit_success"),
            patch("coding_agent.messaging.emit_warning"),
            patch("coding_agent.agents.get_current_agent", return_value=mock_agent),
        ):
            assert handle_unpin_command("/unpin test") is True


class TestHandleDiffCommand:
    def _pool_mock(self, result):
        mock_pool = MagicMock()
        mock_future = MagicMock()
        mock_future.result.return_value = result
        mock_pool.__enter__ = MagicMock(return_value=mock_pool)
        mock_pool.__exit__ = MagicMock(return_value=False)
        mock_pool.submit.return_value = mock_future
        return mock_pool

    def test_with_result(self):
        from coding_agent.command_line.config_commands import handle_diff_command

        pool = self._pool_mock({"add_color": "green", "del_color": "red"})
        with (
            patch("concurrent.futures.ThreadPoolExecutor", return_value=pool),
            patch("coding_agent.config.set_diff_addition_color"),
            patch("coding_agent.config.set_diff_deletion_color"),
        ):
            assert handle_diff_command("/diff") is True

    def test_no_result(self):
        from coding_agent.command_line.config_commands import handle_diff_command

        pool = self._pool_mock(None)
        with patch("concurrent.futures.ThreadPoolExecutor", return_value=pool):
            assert handle_diff_command("/diff") is True

    def test_error_applying(self):
        from coding_agent.command_line.config_commands import handle_diff_command

        pool = self._pool_mock({"add_color": "g", "del_color": "r"})
        with (
            patch("concurrent.futures.ThreadPoolExecutor", return_value=pool),
            patch(
                "coding_agent.config.set_diff_addition_color",
                side_effect=Exception("fail"),
            ),
            patch("coding_agent.messaging.emit_error"),
        ):
            assert handle_diff_command("/diff") is True


class TestHandleColorsCommand:
    def _pool_mock(self, result):
        mock_pool = MagicMock()
        mock_future = MagicMock()
        mock_future.result.return_value = result
        mock_pool.__enter__ = MagicMock(return_value=mock_pool)
        mock_pool.__exit__ = MagicMock(return_value=False)
        mock_pool.submit.return_value = mock_future
        return mock_pool

    def test_with_result(self):
        from coding_agent.command_line.config_commands import handle_colors_command

        pool = self._pool_mock({"thinking": "red"})
        with (
            patch("concurrent.futures.ThreadPoolExecutor", return_value=pool),
            patch("coding_agent.config.set_banner_color"),
            patch("coding_agent.messaging.emit_success"),
        ):
            assert handle_colors_command("/colors") is True

    def test_no_result(self):
        from coding_agent.command_line.config_commands import handle_colors_command

        pool = self._pool_mock(None)
        with patch("concurrent.futures.ThreadPoolExecutor", return_value=pool):
            assert handle_colors_command("/colors") is True

    def test_error_applying(self):
        from coding_agent.command_line.config_commands import handle_colors_command

        pool = self._pool_mock({"thinking": "red"})
        with (
            patch("concurrent.futures.ThreadPoolExecutor", return_value=pool),
            patch("coding_agent.config.set_banner_color", side_effect=Exception("fail")),
            patch("coding_agent.messaging.emit_error"),
        ):
            assert handle_colors_command("/colors") is True


class TestShowColorOptions:
    def test_additions(self):
        from coding_agent.command_line.config_commands import _show_color_options

        with patch("coding_agent.messaging.emit_info"):
            _show_color_options("additions")

    def test_deletions(self):
        from coding_agent.command_line.config_commands import _show_color_options

        with patch("coding_agent.messaging.emit_info"):
            _show_color_options("deletions")

    def test_other(self):
        from coding_agent.command_line.config_commands import _show_color_options

        with patch("coding_agent.messaging.emit_info"):
            _show_color_options("other")
