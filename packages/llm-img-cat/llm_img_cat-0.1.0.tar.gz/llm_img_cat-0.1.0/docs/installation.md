# Installation Guide

## Requirements

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

## Quick Start

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install from PyPI
pip install llm-image-categorizator
```

## Development Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/llm-image-categorizator.git
cd llm-image-categorizator

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

## Configuration

1. Copy the environment template:
```bash
cp .env.template .env
```

2. Edit `.env` with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DASHSCOPE_API_KEY=your_dashscope_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

3. (Optional) Configure model settings in `config/default_config.yaml`

## Verify Installation

```bash
# Run tests
pytest tests/unit

# Try a simple classification
python examples/classify_image.py
```

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'llm_image_categorizator'**
   - Ensure you're in the virtual environment
   - Check if package is installed: `pip list | grep llm-image-categorizator`

2. **API Key Errors**
   - Verify `.env` file exists and contains valid keys
   - Check environment variables are loaded

3. **Model Loading Errors**
   - Ensure internet connection is stable
   - Verify API keys have sufficient permissions

### Getting Help

- Check the [Troubleshooting Guide](troubleshooting.md)
- Open an issue on GitHub
- Contact support at support@example.com

## Next Steps

- Read the [Quick Start Guide](quickstart.md)
- Check [API Documentation](api.md)
- Try [Example Scripts](examples.md) 