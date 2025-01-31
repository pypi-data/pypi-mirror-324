"""Configuration validation for LLM Image Categorization."""
from typing import Dict, Any, List, Optional
from pathlib import Path

class ConfigValidator:
    """Configuration validator for LLM Image Categorization."""
    
    SUPPORTED_MODELS = {
        "qwen": ["qwen-vl-plus", "qwen2.5-vl-3b-instruct"],
        "gpt": ["gpt-4-vision-preview"],
        "gemini": ["gemini-pro-vision"],
    }
    
    @staticmethod
    def validate_model(model: str) -> Optional[str]:
        """Validate model name."""
        for model_family, models in ConfigValidator.SUPPORTED_MODELS.items():
            if any(model.startswith(m) for m in models):
                return None
        return f"Unsupported model: {model}. Supported models: {ConfigValidator.SUPPORTED_MODELS}"
    
    @staticmethod
    def validate_api_keys(config: Dict[str, Any], model: str) -> List[str]:
        """Validate required API keys for given model."""
        issues = []
        
        if model.startswith("qwen") and not config.get("dashscope_api_key"):
            issues.append("DashScope API key required for Qwen models")
        elif model.startswith("gpt") and not config.get("openai_api_key"):
            issues.append("OpenAI API key required for GPT models")
        elif model.startswith("gemini") and not config.get("google_api_key"):
            issues.append("Google API key required for Gemini models")
            
        return issues
    
    @staticmethod
    def validate_paths(paths: Dict[str, Path]) -> Dict[str, str]:
        """Validate paths exist or can be created."""
        issues = {}
        
        for name, path in paths.items():
            if not path.exists():
                try:
                    path.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    issues[name] = f"Failed to create directory {path}: {str(e)}"
                    
        return issues
    
    @staticmethod
    def validate_settings(settings: Dict[str, Any]) -> Dict[str, str]:
        """Validate general settings."""
        issues = {}
        
        # Validate max_retries
        max_retries = settings.get("max_retries")
        if max_retries is not None:
            if not isinstance(max_retries, int) or max_retries < 0:
                issues["max_retries"] = "max_retries must be a non-negative integer"
                
        # Validate timeout
        timeout = settings.get("timeout")
        if timeout is not None:
            if not isinstance(timeout, (int, float)) or timeout <= 0:
                issues["timeout"] = "timeout must be a positive number"
                
        # Validate fallback models
        fallback_models = settings.get("fallback_models")
        if fallback_models is not None:
            if not isinstance(fallback_models, list):
                issues["fallback_models"] = "fallback_models must be a list"
            else:
                for model in fallback_models:
                    model_issue = ConfigValidator.validate_model(model)
                    if model_issue:
                        issues.setdefault("fallback_models", []).append(model_issue)
                        
        return issues 