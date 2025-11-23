"""
Unit tests for configuration loader.
"""

import pytest
from pathlib import Path
import tempfile
import yaml

from nixtla_search_to_slack.config_loader import ConfigLoader


class TestConfigLoader:
    """Test configuration loading functionality."""

    def test_load_valid_sources_config(self, tmp_path, sample_sources_config):
        """Test loading valid sources configuration."""
        # Create temp config file
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        sources_file = config_dir / "sources.yaml"

        with open(sources_file, "w") as f:
            yaml.dump(sample_sources_config, f)

        # Load configuration
        loader = ConfigLoader(config_dir)
        config = loader.load_sources()

        assert "sources" in config
        assert "web" in config["sources"]
        assert "github" in config["sources"]
        assert config["sources"]["web"]["max_results"] == 5

    def test_load_valid_topics_config(self, tmp_path, sample_sources_config, sample_topics_config):
        """Test loading valid topics configuration."""
        # Create temp config files
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        sources_file = config_dir / "sources.yaml"
        with open(sources_file, "w") as f:
            yaml.dump(sample_sources_config, f)

        topics_file = config_dir / "topics.yaml"
        with open(topics_file, "w") as f:
            yaml.dump(sample_topics_config, f)

        # Load configuration
        loader = ConfigLoader(config_dir)
        config = loader.load_topics()

        assert "topics" in config
        assert "test-topic" in config["topics"]
        assert config["topics"]["test-topic"]["name"] == "Test Topic"
        assert len(config["topics"]["test-topic"]["keywords"]) == 2

    def test_missing_config_directory(self):
        """Test error when config directory doesn't exist."""
        with pytest.raises(FileNotFoundError, match="Configuration directory not found"):
            ConfigLoader(Path("/nonexistent/directory"))

    def test_missing_config_file(self, tmp_path):
        """Test error when config file doesn't exist."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        loader = ConfigLoader(config_dir)
        with pytest.raises(FileNotFoundError, match="Configuration file not found"):
            loader.load_yaml("nonexistent.yaml")

    def test_invalid_yaml(self, tmp_path):
        """Test error with invalid YAML syntax."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        bad_yaml = config_dir / "bad.yaml"
        with open(bad_yaml, "w") as f:
            f.write("invalid: yaml: syntax: ][")

        loader = ConfigLoader(config_dir)
        with pytest.raises(ValueError, match="Invalid YAML"):
            loader.load_yaml("bad.yaml")

    def test_missing_required_source_fields(self, tmp_path):
        """Test error when sources config is missing required fields."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        sources_file = config_dir / "sources.yaml"
        bad_config = {
            "sources": {
                "web": {
                    "provider": "serpapi"
                    # Missing max_results and time_range
                }
            }
        }
        with open(sources_file, "w") as f:
            yaml.dump(bad_config, f)

        loader = ConfigLoader(config_dir)
        with pytest.raises(ValueError, match="missing required field"):
            loader.load_sources()

    def test_missing_required_topic_fields(self, tmp_path, sample_sources_config):
        """Test error when topics config is missing required fields."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        # Create valid sources config
        sources_file = config_dir / "sources.yaml"
        with open(sources_file, "w") as f:
            yaml.dump(sample_sources_config, f)

        # Create invalid topics config
        topics_file = config_dir / "topics.yaml"
        bad_config = {
            "topics": {
                "bad-topic": {
                    "name": "Bad Topic"
                    # Missing keywords and sources
                }
            }
        }
        with open(topics_file, "w") as f:
            yaml.dump(bad_config, f)

        loader = ConfigLoader(config_dir)
        with pytest.raises(ValueError, match="missing required field"):
            loader.load_topics()

    def test_topic_references_unknown_source(self, tmp_path, sample_sources_config):
        """Test error when topic references unknown source."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        # Create sources config
        sources_file = config_dir / "sources.yaml"
        with open(sources_file, "w") as f:
            yaml.dump(sample_sources_config, f)

        # Create topics config with unknown source
        topics_file = config_dir / "topics.yaml"
        bad_config = {
            "topics": {
                "test-topic": {
                    "name": "Test Topic",
                    "keywords": ["test"],
                    "sources": ["web", "unknown_source"]  # unknown_source doesn't exist
                }
            }
        }
        with open(topics_file, "w") as f:
            yaml.dump(bad_config, f)

        loader = ConfigLoader(config_dir)
        with pytest.raises(ValueError, match="references unknown source"):
            loader.load_topics()

    def test_validate_config_success(self, tmp_path, sample_sources_config, sample_topics_config):
        """Test successful validation of all configs."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        sources_file = config_dir / "sources.yaml"
        with open(sources_file, "w") as f:
            yaml.dump(sample_sources_config, f)

        topics_file = config_dir / "topics.yaml"
        with open(topics_file, "w") as f:
            yaml.dump(sample_topics_config, f)

        loader = ConfigLoader(config_dir)
        assert loader.validate_config() is True