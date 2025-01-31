"""Unit tests for configuration management."""
import os
import pytest
from pathlib import Path
from typing import Dict

from llm_image_categorizator.config import BaseConfig, ConfigLoader, ConfigValidator

def test_base_config_defaults():
    """Test BaseConfig default values."""
    config = BaseConfig()
    assert config.default_model == "qwen-vl-plus"
    assert config.max_retries == 3
    assert config.timeout == 30
    assert isinstance(config.data_dir, Path)

def test_config_from_env(test_env, monkeypatch):
    """Test loading configuration from environment variables."""
    # Set environment variables
    for key, value in test_env.items():
        monkeypatch.setenv(key, value)
    
    config = BaseConfig.from_env()
    
    assert config.openai_api_key == test_env["OPENAI_API_KEY"]
    assert config.dashscope_api_key == test_env["DASHSCOPE_API_KEY"]
    assert config.default_model == test_env["DEFAULT_MODEL"]
    assert config.max_retries == int(test_env["MAX_RETRIES"])

def test_config_validation():
    """Test configuration validation."""
    config = BaseConfig()
    config.max_retries = -1  # Invalid value
    
    issues = config.validate()
    assert "max_retries" in issues
    assert "must be non-negative" in issues["max_retries"]

def test_config_loader(mock_config_path, test_env, monkeypatch):
    """Test ConfigLoader with both YAML and environment variables."""
    # Set environment variables
    for key, value in test_env.items():
        monkeypatch.setenv(key, value)
    
    config = ConfigLoader.load_config(
        yaml_path=mock_config_path,
        validate=True
    )
    
    assert config.default_model == "qwen-vl-plus"
    assert config.max_retries == 3
    assert config.timeout == 30

def test_config_validator():
    """Test ConfigValidator functionality."""
    # Test model validation
    assert ConfigValidator.validate_model("qwen-vl-plus") is None
    assert "Unsupported model" in ConfigValidator.validate_model("invalid-model")
    
    # Test API key validation
    issues = ConfigValidator.validate_api_keys(
        {"dashscope_api_key": None},
        "qwen-vl-plus"
    )
    assert len(issues) == 1
    assert "DashScope API key required" in issues[0]
    
    # Test settings validation
    issues = ConfigValidator.validate_settings({
        "max_retries": -1,
        "timeout": 0
    })
    assert "max_retries" in issues
    assert "timeout" in issues

def test_path_validation(tmp_path):
    """Test path validation and creation."""
    test_paths = {
        "data": tmp_path / "data",
        "cache": tmp_path / "cache"
    }
    
    issues = ConfigValidator.validate_paths(test_paths)
    assert not issues  # No issues, directories should be created
    
    for path in test_paths.values():
        assert path.exists()

@pytest.mark.parametrize("model,required_key", [
    ("qwen-vl-plus", "dashscope_api_key"),
    ("gpt-4-vision-preview", "openai_api_key"),
    ("gemini-pro-vision", "google_api_key")
])
def test_model_specific_api_keys(model: str, required_key: str):
    """Test API key requirements for different models."""
    config = {key: None for key in ["dashscope_api_key", "openai_api_key", "google_api_key"]}
    issues = ConfigValidator.validate_api_keys(config, model)
    assert len(issues) == 1
    assert required_key in issues[0].lower() 