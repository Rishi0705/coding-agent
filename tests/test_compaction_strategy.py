import configparser
import os
import tempfile
from unittest.mock import patch

from coding_agent.config import (
    DEFAULT_SECTION,
    get_compaction_strategy,
)


def test_default_compaction_strategy():
    """Test that the default compaction strategy is truncation"""
    with patch("coding_agent.config.get_value") as mock_get_value:
        mock_get_value.return_value = None
        strategy = get_compaction_strategy()
        assert strategy == "truncation"


def test_set_compaction_strategy_truncation():
    """Test that we can set the compaction strategy to truncation"""
    import coding_agent.config

    original_config_dir = coding_agent.config.CONFIG_DIR
    original_config_file = coding_agent.config.CONFIG_FILE

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            coding_agent.config.CONFIG_DIR = temp_dir
            coding_agent.config.CONFIG_FILE = os.path.join(temp_dir, "coding_agent.cfg")

            config = configparser.ConfigParser()
            config[DEFAULT_SECTION] = {}
            config[DEFAULT_SECTION]["compaction_strategy"] = "truncation"

            with open(coding_agent.config.CONFIG_FILE, "w") as f:
                config.write(f)

            strategy = get_compaction_strategy()
            assert strategy == "truncation"
        finally:
            coding_agent.config.CONFIG_DIR = original_config_dir
            coding_agent.config.CONFIG_FILE = original_config_file


def test_set_compaction_strategy_summarization():
    """Test that we can set the compaction strategy to summarization"""
    import coding_agent.config

    original_config_dir = coding_agent.config.CONFIG_DIR
    original_config_file = coding_agent.config.CONFIG_FILE

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            coding_agent.config.CONFIG_DIR = temp_dir
            coding_agent.config.CONFIG_FILE = os.path.join(temp_dir, "coding_agent.cfg")

            config = configparser.ConfigParser()
            config[DEFAULT_SECTION] = {}
            config[DEFAULT_SECTION]["compaction_strategy"] = "summarization"

            with open(coding_agent.config.CONFIG_FILE, "w") as f:
                config.write(f)

            strategy = get_compaction_strategy()
            assert strategy == "summarization"
        finally:
            coding_agent.config.CONFIG_DIR = original_config_dir
            coding_agent.config.CONFIG_FILE = original_config_file


def test_set_compaction_strategy_invalid():
    """Test that an invalid compaction strategy defaults to truncation"""
    import coding_agent.config

    original_config_dir = coding_agent.config.CONFIG_DIR
    original_config_file = coding_agent.config.CONFIG_FILE

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            coding_agent.config.CONFIG_DIR = temp_dir
            coding_agent.config.CONFIG_FILE = os.path.join(temp_dir, "coding_agent.cfg")

            config = configparser.ConfigParser()
            config[DEFAULT_SECTION] = {}
            config[DEFAULT_SECTION]["compaction_strategy"] = "invalid_strategy"

            with open(coding_agent.config.CONFIG_FILE, "w") as f:
                config.write(f)

            strategy = get_compaction_strategy()
            assert strategy == "truncation"
        finally:
            coding_agent.config.CONFIG_DIR = original_config_dir
            coding_agent.config.CONFIG_FILE = original_config_file
