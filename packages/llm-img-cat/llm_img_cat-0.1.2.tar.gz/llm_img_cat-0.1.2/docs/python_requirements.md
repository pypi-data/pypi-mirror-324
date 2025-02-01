# Python Version Requirements

## Supported Python Versions

The LLM Image Categorization package supports the following Python versions:

- Python 3.8 (minimum)
- Python 3.9
- Python 3.10
- Python 3.11

## Version-Specific Features

### Python 3.8
- Base functionality
- Type hints support
- Async/await support

### Python 3.9+
- Improved type hints
- Dictionary union operators
- More flexible decorators

### Python 3.10+
- Pattern matching
- Better error messages
- Improved type unions

### Python 3.11+
- Enhanced error messages
- Faster runtime
- Better typing support

## Dependencies Version Matrix

| Dependency | Python 3.8 | Python 3.9 | Python 3.10 | Python 3.11 |
|------------|------------|------------|-------------|-------------|
| openai     | >=1.0.0   | >=1.0.0    | >=1.0.0     | >=1.0.0    |
| anthropic  | >=0.5.0   | >=0.5.0    | >=0.5.0     | >=0.5.0    |
| dashscope  | >=1.10.0  | >=1.10.0   | >=1.10.0    | >=1.10.0   |
| pillow     | >=10.0.0  | >=10.0.0   | >=10.0.0    | >=10.0.0   |

## Installation Requirements

### System Requirements
- Python 3.8 or higher
- pip 20.0 or higher
- venv module (usually included with Python)

### Virtual Environment
It's recommended to use a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### Verifying Python Version
```bash
# Check Python version
python --version

# Check pip version
pip --version
```

## Common Issues

### Python Version Too Old
```
Error: Python 3.8 or higher is required (found 3.7.x)
Solution: Install Python 3.8 or higher
```

### Missing venv Module
```
Error: No module named 'venv'
Solution: Install python3-venv package (Linux) or full Python installation (Windows)
```

### Dependency Conflicts
```
Error: ... has requirement Python>=3.8, but you'll have Python 3.7
Solution: Upgrade Python or use a supported version
```

## Best Practices

1. **Version Management**
   - Use pyenv for managing multiple Python versions
   - Keep Python up to date with security patches
   - Test against all supported versions

2. **Virtual Environments**
   - Always use virtual environments
   - Create separate environments for different projects
   - Document environment setup steps

3. **Dependency Management**
   - Pin dependency versions
   - Use requirements.txt for reproducible builds
   - Regularly update dependencies

4. **Version Checking**
   ```python
   import sys
   
   if sys.version_info < (3, 8):
       raise RuntimeError("Python 3.8 or higher is required")
   ```

## Development Setup

### For Contributors
```bash
# Clone repository
git clone https://github.com/yourusername/llm-image-categorizator.git
cd llm-image-categorizator

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt
```

### For Testing Multiple Versions
```bash
# Using tox for testing multiple Python versions
pip install tox
tox

# Manual testing with different versions
python3.8 -m pytest tests/
python3.9 -m pytest tests/
python3.10 -m pytest tests/
python3.11 -m pytest tests/
```

## Upgrading Python

### Linux/macOS
```bash
# Using pyenv
pyenv install 3.11.0
pyenv global 3.11.0

# System package manager (Ubuntu/Debian)
sudo apt update
sudo apt install python3.11
```

### Windows
1. Download installer from python.org
2. Run installer with "Add Python to PATH" option
3. Verify installation: `python --version` 