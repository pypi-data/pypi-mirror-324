# Development Environment Setup

This guide explains how to set up your development environment for the LLM Image Categorization project.

## Prerequisites

- Python 3.9 or higher
- Git
- pip (Python package installer)
- Virtual environment support (`python3-venv` package)

## Quick Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd llm_image_categorizator
```

2. Run the setup script:
```bash
./scripts/setup_env.sh
```

This script will:
- Check Python version
- Create a virtual environment
- Install dependencies
- Set up directory structure
- Create initial configuration

3. Validate the setup:
```bash
source venv/bin/activate
./scripts/validate_env.py
```

## Manual Setup

If you prefer to set up manually or if the automatic setup fails:

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -e ".[dev,docs,examples]"
```

3. Configure environment:
```bash
cp .env.template .env
# Edit .env with your API keys
```

4. Create necessary directories:
```bash
mkdir -p tests/data
mkdir -p tests/results
mkdir -p logs
```

## Environment Variables

Required environment variables:
- `QWEN_API_KEY`: Your Qwen API key (required)
- `OPENAI_API_KEY`: Your OpenAI API key (optional)
- `GEMINI_API_KEY`: Your Gemini API key (optional)

Optional environment variables:
- `LOG_LEVEL`: Logging level (default: INFO)
- `LOG_FILE`: Log file path (default: logs/app.log)

## Development Tools

The project includes several development tools:

- **Black**: Code formatting
  ```bash
  black src/ tests/
  ```

- **isort**: Import sorting
  ```bash
  isort src/ tests/
  ```

- **flake8**: Code linting
  ```bash
  flake8 src/ tests/
  ```

- **mypy**: Type checking
  ```bash
  mypy src/
  ```

- **pytest**: Testing
  ```bash
  pytest tests/
  ```

## IDE Setup

### VSCode

Recommended extensions:
- Python
- Pylance
- Python Test Explorer
- Python Docstring Generator
- YAML

Recommended settings (`settings.json`):
```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### PyCharm

Recommended settings:
- Enable Black formatter
- Enable Flake8 linting
- Set project interpreter to virtual environment
- Enable auto-import optimization

## Common Issues

1. **Virtual environment not activated**
   - Symptom: Import errors
   - Solution: Run `source venv/bin/activate`

2. **Missing dependencies**
   - Symptom: ModuleNotFoundError
   - Solution: Run `pip install -r requirements.txt`

3. **API keys not set**
   - Symptom: Authentication errors
   - Solution: Set up environment variables in `.env`

## Best Practices

1. Always activate virtual environment before development
2. Run tests before committing changes
3. Format code with Black before committing
4. Update requirements.txt when adding new dependencies
5. Keep documentation up to date 