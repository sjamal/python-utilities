"""Configuration loading utilities supporting YAML, JSON, and .env files."""

import os
import json
from pathlib import Path
from typing import Any, Dict, Optional, Union


class ConfigLoader:
    """Load and merge configuration from YAML, JSON, or .env files with env var overrides."""

    @staticmethod
    def load_yaml(filepath: Union[str, Path]) -> Dict[str, Any]:
        """
        Load configuration from YAML file.

        Args:
            filepath: Path to YAML file.

        Returns:
            Dict of configuration.

        Raises:
            ImportError: If PyYAML is not installed.
            FileNotFoundError: If file does not exist.
        """
        try:
            import yaml
        except ImportError:
            raise ImportError(
                "PyYAML is required for YAML support. Install with: pip install pyyaml"
            )

        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")

        with open(path, "r") as f:
            return yaml.safe_load(f) or {}

    @staticmethod
    def load_json(filepath: Union[str, Path]) -> Dict[str, Any]:
        """
        Load configuration from JSON file.

        Args:
            filepath: Path to JSON file.

        Returns:
            Dict of configuration.

        Raises:
            FileNotFoundError: If file does not exist.
            json.JSONDecodeError: If file is not valid JSON.
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")

        with open(path, "r") as f:
            return json.load(f)

    @staticmethod
    def load_env(filepath: Union[str, Path]) -> Dict[str, str]:
        """
        Load .env file (KEY=VALUE format, one per line).

        Args:
            filepath: Path to .env file.

        Returns:
            Dict of environment variables.

        Raises:
            FileNotFoundError: If file does not exist.
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f".env file not found: {filepath}")

        env_vars = {}
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "=" in line:
                        key, value = line.split("=", 1)
                        env_vars[key.strip()] = value.strip().strip('"\'')

        return env_vars

    @staticmethod
    def merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge override dict into base dict.

        Args:
            base: Base configuration.
            override: Configuration to merge on top.

        Returns:
            Merged configuration.
        """
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = ConfigLoader.merge(result[key], value)
            else:
                result[key] = value
        return result

    @staticmethod
    def load_with_env_override(
        filepath: Union[str, Path],
        env_prefix: str = "",
        required_keys: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Load config from file and override with environment variables.

        Args:
            filepath: Path to config file (.yaml, .json, or .env).
            env_prefix: Optional prefix for environment variables (e.g., 'APP_').
            required_keys: List of keys that must be present after loading.

        Returns:
            Merged configuration dict.

        Raises:
            ValueError: If required keys are missing.
            FileNotFoundError: If config file not found.
        """
        path = Path(filepath)
        ext = path.suffix.lower()

        # Load from file
        if ext == ".yaml" or ext == ".yml":
            config = ConfigLoader.load_yaml(path)
        elif ext == ".json":
            config = ConfigLoader.load_json(path)
        elif ext == ".env":
            config = ConfigLoader.load_env(path)
        else:
            raise ValueError(f"Unsupported config format: {ext}")

        # Apply environment variable overrides
        for key in config.keys():
            env_key = f"{env_prefix}{key}".upper() if env_prefix else key.upper()
            if env_key in os.environ:
                config[key] = os.environ[env_key]

        # Validate required keys
        if required_keys:
            missing = [k for k in required_keys if k not in config or not config[k]]
            if missing:
                raise ValueError(f"Missing required config keys: {', '.join(missing)}")

        return config
