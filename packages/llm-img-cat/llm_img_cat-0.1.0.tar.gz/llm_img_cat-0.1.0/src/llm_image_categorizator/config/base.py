"""Base configuration management for the LLM Image Categorization package."""
from typing import Dict, Any, Optional
from pathlib import Path
import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class BaseConfig:
    """Base configuration class for LLM Image Categorization."""
    
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    dashscope_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    
    # Model Settings
    default_model: str = "qwen-vl-plus"
    fallback_models: list = None
    max_retries: int = 3
    timeout: int = 30
    
    # Paths
    data_dir: Path = Path("data")
    cache_dir: Path = Path("cache")
    results_dir: Path = Path("results")
    
    @classmethod
    def from_env(cls, env_file: Optional[str] = None) -> 'BaseConfig':
        """Create configuration from environment variables."""
        if env_file:
            load_dotenv(env_file)
        
        config = cls()
        
        # Load API keys from environment
        config.openai_api_key = os.getenv("OPENAI_API_KEY")
        config.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        config.dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
        config.google_api_key = os.getenv("GOOGLE_API_KEY")
        
        # Load other settings
        if os.getenv("DEFAULT_MODEL"):
            config.default_model = os.getenv("DEFAULT_MODEL")
        
        if os.getenv("FALLBACK_MODELS"):
            config.fallback_models = os.getenv("FALLBACK_MODELS").split(",")
        
        if os.getenv("MAX_RETRIES"):
            config.max_retries = int(os.getenv("MAX_RETRIES"))
        
        if os.getenv("TIMEOUT"):
            config.timeout = int(os.getenv("TIMEOUT"))
        
        return config
    
    def validate(self) -> Dict[str, Any]:
        """Validate the configuration and return any issues found."""
        issues = {}
        
        # Check required API keys based on default model
        if self.default_model.startswith("gpt"):
            if not self.openai_api_key:
                issues["openai_api_key"] = "OpenAI API key required for GPT models"
        elif self.default_model.startswith("qwen"):
            if not self.dashscope_api_key:
                issues["dashscope_api_key"] = "DashScope API key required for Qwen models"
        elif self.default_model.startswith("gemini"):
            if not self.google_api_key:
                issues["google_api_key"] = "Google API key required for Gemini models"
        
        # Validate paths
        for path_name, path in [
            ("data_dir", self.data_dir),
            ("cache_dir", self.cache_dir),
            ("results_dir", self.results_dir)
        ]:
            if not path.exists():
                try:
                    path.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    issues[path_name] = f"Failed to create directory: {str(e)}"
        
        # Validate other settings
        if self.max_retries < 0:
            issues["max_retries"] = "max_retries must be non-negative"
        
        if self.timeout < 0:
            issues["timeout"] = "timeout must be non-negative"
        
        return issues
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary, excluding sensitive data."""
        return {
            "default_model": self.default_model,
            "fallback_models": self.fallback_models,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "data_dir": str(self.data_dir),
            "cache_dir": str(self.cache_dir),
            "results_dir": str(self.results_dir),
            # Exclude API keys for security
        } 