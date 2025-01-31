"""Configuration loader for LLM Image Categorization."""
from typing import Dict, Any, Optional
from pathlib import Path
import yaml
from .base import BaseConfig
from .validator import ConfigValidator

class ConfigLoader:
    """Configuration loader that handles both YAML and environment variables."""
    
    @staticmethod
    def load_yaml(config_path: Path) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise ValueError(f"Failed to load config from {config_path}: {str(e)}")
    
    @staticmethod
    def load_config(
        yaml_path: Optional[Path] = None,
        env_file: Optional[str] = None,
        validate: bool = True
    ) -> BaseConfig:
        """
        Load configuration from YAML and/or environment variables.
        
        Args:
            yaml_path: Path to YAML configuration file
            env_file: Path to .env file
            validate: Whether to validate the configuration
            
        Returns:
            BaseConfig: Loaded and validated configuration
        """
        # Start with base config
        config = BaseConfig()
        
        # Load from YAML if provided
        if yaml_path:
            yaml_config = ConfigLoader.load_yaml(yaml_path)
            
            # Update config with YAML values
            for key, value in yaml_config.items():
                if hasattr(config, key):
                    setattr(config, key, value)
        
        # Load from environment variables (overrides YAML)
        if env_file:
            env_config = BaseConfig.from_env(env_file)
            
            # Update non-None values from environment
            for key, value in env_config.to_dict().items():
                if value is not None:
                    setattr(config, key, value)
        
        # Validate if requested
        if validate:
            issues = {}
            
            # Validate model
            model_issue = ConfigValidator.validate_model(config.default_model)
            if model_issue:
                issues["default_model"] = model_issue
            
            # Validate API keys
            api_key_issues = ConfigValidator.validate_api_keys(
                config.to_dict(),
                config.default_model
            )
            if api_key_issues:
                issues["api_keys"] = api_key_issues
            
            # Validate paths
            path_issues = ConfigValidator.validate_paths({
                "data_dir": config.data_dir,
                "cache_dir": config.cache_dir,
                "results_dir": config.results_dir
            })
            if path_issues:
                issues["paths"] = path_issues
            
            # Validate other settings
            setting_issues = ConfigValidator.validate_settings(config.to_dict())
            if setting_issues:
                issues["settings"] = setting_issues
            
            if issues:
                raise ValueError(f"Configuration validation failed: {issues}")
        
        return config 