"""
Configuration loader for Nixtla Search-to-Slack plugin.
Handles YAML configuration files with validation.
"""

import logging
from pathlib import Path
from typing import Dict, Any

import yaml

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Load and validate configuration from YAML files."""

    def __init__(self, config_dir: Path = None):
        """
        Initialize the configuration loader.

        Args:
            config_dir: Path to configuration directory
        """
        if config_dir is None:
            # Default to config/ relative to this file
            module_path = Path(__file__).parent
            self.config_dir = module_path.parent.parent / "config"
        else:
            self.config_dir = Path(config_dir)

        if not self.config_dir.exists():
            raise FileNotFoundError(f"Configuration directory not found: {self.config_dir}")

    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """
        Load a YAML configuration file.

        Args:
            filename: Name of the YAML file to load

        Returns:
            Parsed YAML content as dictionary
        """
        filepath = self.config_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Configuration file not found: {filepath}")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                logger.debug(f"Loaded configuration from {filepath}")
                return data or {}
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML file {filepath}: {e}")
            raise ValueError(f"Invalid YAML in {filename}: {e}")

    def load_sources(self) -> Dict[str, Any]:
        """
        Load and validate sources configuration.

        Returns:
            Sources configuration dictionary
        """
        config = self.load_yaml("sources.yaml")

        # Validate required fields
        if "sources" not in config:
            raise ValueError("sources.yaml must contain 'sources' section")

        # Validate each source
        for source_id, source_config in config["sources"].items():
            required_fields = ["max_results", "time_range"]
            for field in required_fields:
                if field not in source_config:
                    raise ValueError(
                        f"Source '{source_id}' missing required field: {field}"
                    )

            # Validate source-specific requirements
            if source_id == "web" and "provider" not in source_config:
                raise ValueError("Web source requires 'provider' field")
            elif source_id == "github":
                if not source_config.get("organizations") and not source_config.get("additional_repos"):
                    raise ValueError(
                        "GitHub source requires either 'organizations' or 'additional_repos'"
                    )

        logger.info(f"Loaded {len(config['sources'])} search sources")
        return config

    def load_topics(self) -> Dict[str, Any]:
        """
        Load and validate topics configuration.

        Returns:
            Topics configuration dictionary
        """
        config = self.load_yaml("topics.yaml")

        # Validate required fields
        if "topics" not in config:
            raise ValueError("topics.yaml must contain 'topics' section")

        # Validate each topic
        for topic_id, topic_config in config["topics"].items():
            required_fields = ["name", "keywords", "sources"]
            for field in required_fields:
                if field not in topic_config:
                    raise ValueError(
                        f"Topic '{topic_id}' missing required field: {field}"
                    )

            # Validate keywords is a list
            if not isinstance(topic_config["keywords"], list):
                raise ValueError(f"Topic '{topic_id}' keywords must be a list")

            # Validate sources is a list
            if not isinstance(topic_config["sources"], list):
                raise ValueError(f"Topic '{topic_id}' sources must be a list")

            # Validate sources exist
            available_sources = self.load_sources()["sources"].keys()
            for source in topic_config["sources"]:
                if source not in available_sources:
                    raise ValueError(
                        f"Topic '{topic_id}' references unknown source: {source}"
                    )

        logger.info(f"Loaded {len(config['topics'])} topics")
        return config

    def validate_config(self) -> bool:
        """
        Validate all configuration files.

        Returns:
            True if all configurations are valid

        Raises:
            Various exceptions if configuration is invalid
        """
        try:
            self.load_sources()
            self.load_topics()
            logger.info("All configuration files validated successfully")
            return True
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            raise