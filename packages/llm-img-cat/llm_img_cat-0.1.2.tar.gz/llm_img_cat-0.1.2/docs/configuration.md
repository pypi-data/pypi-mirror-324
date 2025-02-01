# Configuration Guide

## Overview

The LLM Image Categorization package uses a flexible configuration system that supports:
- Environment variables
- YAML configuration files
- Runtime configuration
- Model-specific settings

## Configuration Sources

### 1. Environment Variables

Create a `.env` file in your project root:

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DASHSCOPE_API_KEY=your_dashscope_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Model Settings
DEFAULT_MODEL=qwen-vl-plus
FALLBACK_MODELS=gemini-pro-vision,gpt-4-vision-preview

# API Settings
MAX_RETRIES=3
TIMEOUT=30

# Paths
DATA_DIR=data
CACHE_DIR=cache
RESULTS_DIR=results
```

### 2. YAML Configuration

Create a `config.yaml` file:

```yaml
# Model Settings
default_model: "qwen-vl-plus"
fallback_models:
  - "gemini-pro-vision"
  - "gpt-4-vision-preview"

# API Settings
max_retries: 3
timeout: 30

# Paths
data_dir: "data"
cache_dir: "cache"
results_dir: "results"

# Model-specific settings
model_settings:
  qwen-vl-plus:
    max_tokens: 2048
    temperature: 0.7
  gemini-pro-vision:
    max_tokens: 2048
    temperature: 0.7
```

## Loading Configuration

### From Environment

```python
from llm_image_categorizator.config import BaseConfig

# Load from default .env file
config = BaseConfig.from_env()

# Load from specific .env file
config = BaseConfig.from_env(".env.production")
```

### From YAML

```python
from llm_image_categorizator.config import ConfigLoader

# Load from YAML only
config = ConfigLoader.load_config(yaml_path="config.yaml")

# Load from both YAML and environment
config = ConfigLoader.load_config(
    yaml_path="config.yaml",
    env_file=".env"
)
```

### Runtime Configuration

```python
from llm_image_categorizator.config import BaseConfig

config = BaseConfig(
    default_model="qwen-vl-plus",
    max_retries=5,
    timeout=60
)
```

## Configuration Options

### Required Settings

| Setting | Type | Description | Default |
|---------|------|-------------|---------|
| `default_model` | str | Primary model to use | "qwen-vl-plus" |
| `max_retries` | int | Maximum retry attempts | 3 |
| `timeout` | int | Request timeout in seconds | 30 |

### Optional Settings

| Setting | Type | Description | Default |
|---------|------|-------------|---------|
| `fallback_models` | List[str] | Models to try if primary fails | None |
| `data_dir` | Path | Directory for data files | "./data" |
| `cache_dir` | Path | Directory for cache files | "./cache" |
| `results_dir` | Path | Directory for results | "./results" |

### Model-Specific Settings

```python
config.model_settings = {
    "qwen-vl-plus": {
        "max_tokens": 2048,
        "temperature": 0.7,
        "confidence_threshold": 0.8
    }
}
```

## Configuration Validation

The package automatically validates configuration:

```python
from llm_image_categorizator.config import ConfigValidator

# Validate model name
ConfigValidator.validate_model("qwen-vl-plus")

# Validate API keys
ConfigValidator.validate_api_keys(config.to_dict(), "qwen-vl-plus")

# Validate paths
ConfigValidator.validate_paths({
    "data_dir": config.data_dir,
    "cache_dir": config.cache_dir
})
```

## Environment Variables

### Required Variables

- `DASHSCOPE_API_KEY`: For Qwen models
- `OPENAI_API_KEY`: For GPT models
- `GOOGLE_API_KEY`: For Gemini models

### Optional Variables

- `DEFAULT_MODEL`: Override default model
- `MAX_RETRIES`: Override retry attempts
- `TIMEOUT`: Override timeout
- `DATA_DIR`: Override data directory
- `CACHE_DIR`: Override cache directory
- `RESULTS_DIR`: Override results directory

## Best Practices

1. **Security**
   - Never commit `.env` files
   - Use environment variables for sensitive data
   - Rotate API keys regularly

2. **Organization**
   - Use different config files for different environments
   - Keep model-specific settings separate
   - Document all configuration changes

3. **Validation**
   - Always validate configuration before use
   - Set appropriate confidence thresholds
   - Monitor API usage and limits

4. **Performance**
   - Enable caching for repeated operations
   - Use appropriate timeout values
   - Configure retry strategies

## Troubleshooting

### Common Issues

1. **Missing API Keys**
   ```python
   # Check if keys are loaded
   print(config.dashscope_api_key)  # Should not be None
   ```

2. **Invalid Model Names**
   ```python
   # Validate model name
   ConfigValidator.validate_model("invalid-model")
   # Raises: "Unsupported model: invalid-model"
   ```

3. **Path Issues**
   ```python
   # Ensure directories exist
   config.data_dir.mkdir(parents=True, exist_ok=True)
   ```

### Getting Help

- Check error messages from validation
- Review configuration files
- Consult API documentation
- Contact support team 