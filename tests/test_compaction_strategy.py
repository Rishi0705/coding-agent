import configparser
import os
import tempfile
from unittest.mock import patch

from coco_codes.config import (
    DEFAULT_SECTION,
    get_compaction_strategy,
)


def test_default_compaction_strategy():
    """Test that the default compaction strategy is truncation"""
    with patch("coco_codes.config.get_value") as mock_get_value:
        mock_get_value.return_value = None
        strategy = get_compaction_strategy()
        assert strategy == "truncation"


def test_set_compaction_strategy_truncation():
    """Test that we can set the compaction strategy to truncation"""
    import coco_codes.config

    original_config_dir = coco_codes.config.CONFIG_DIR
    original_config_file = coco_codes.config.CONFIG_FILE

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            coco_codes.config.CONFIG_DIR = temp_dir
            coco_codes.config.CONFIG_FILE = os.path.join(temp_dir, "coco.cfg")

            config = configparser.ConfigParser()
            config[DEFAULT_SECTION] = {}
            config[DEFAULT_SECTION]["compaction_strategy"] = "truncation"

            with open(coco_codes.config.CONFIG_FILE, "w") as f:
                config.write(f)

            strategy = get_compaction_strategy()
            assert strategy == "truncation"
        finally:
            coco_codes.config.CONFIG_DIR = original_config_dir
            coco_codes.config.CONFIG_FILE = original_config_file


def test_set_compaction_strategy_summarization():
    """Test that we can set the compaction strategy to summarization"""
    import coco_codes.config

    original_config_dir = coco_codes.config.CONFIG_DIR
    original_config_file = coco_codes.config.CONFIG_FILE

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            coco_codes.config.CONFIG_DIR = temp_dir
            coco_codes.config.CONFIG_FILE = os.path.join(temp_dir, "coco.cfg")

            config = configparser.ConfigParser()
            config[DEFAULT_SECTION] = {}
            config[DEFAULT_SECTION]["compaction_strategy"] = "summarization"

            with open(coco_codes.config.CONFIG_FILE, "w") as f:
                config.write(f)

            strategy = get_compaction_strategy()
            assert strategy == "summarization"
        finally:
            coco_codes.config.CONFIG_DIR = original_config_dir
            coco_codes.config.CONFIG_FILE = original_config_file


def test_set_compaction_strategy_invalid():
    """Test that an invalid compaction strategy defaults to truncation"""
    import coco_codes.config

    original_config_dir = coco_codes.config.CONFIG_DIR
    original_config_file = coco_codes.config.CONFIG_FILE

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            coco_codes.config.CONFIG_DIR = temp_dir
            coco_codes.config.CONFIG_FILE = os.path.join(temp_dir, "coco.cfg")

            config = configparser.ConfigParser()
            config[DEFAULT_SECTION] = {}
            config[DEFAULT_SECTION]["compaction_strategy"] = "invalid_strategy"

            with open(coco_codes.config.CONFIG_FILE, "w") as f:
                config.write(f)

            strategy = get_compaction_strategy()
            assert strategy == "truncation"
        finally:
            coco_codes.config.CONFIG_DIR = original_config_dir
            coco_codes.config.CONFIG_FILE = original_config_file
