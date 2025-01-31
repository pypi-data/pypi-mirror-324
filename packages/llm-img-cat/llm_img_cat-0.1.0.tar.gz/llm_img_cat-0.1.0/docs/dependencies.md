# Dependencies Documentation

## Core Dependencies

### API Clients
- **openai**: Required for Qwen and OpenAI API integration
  - Used in: `src/categorization/gwen_book_classifier.py`
  - Version: >=1.0.0
  - Purpose: Making API calls to Qwen and OpenAI services

- **google-cloud-aiplatform**: Required for Gemini API integration
  - Used in: `src/categorization/gemini_book_classifier.py`
  - Version: >=1.25.0
  - Purpose: Making API calls to Google's Gemini service

### Image Processing
- **Pillow**: Core image processing library
  - Used in: Image validation and preprocessing
  - Version: >=10.0.0
  - Purpose: Loading and basic image processing

- **imagehash**: Image validation and comparison
  - Used in: Book cover validation
  - Version: >=4.3.1
  - Purpose: Detecting duplicate and invalid images

### Utilities
- **python-dotenv**: Environment variable management
  - Used in: Configuration loading
  - Version: >=1.0.0
  - Purpose: Loading API keys and configuration from .env files

- **rich**: Terminal output formatting
  - Used in: CLI tools and test output
  - Version: >=13.0.0
  - Purpose: Creating rich terminal user interfaces

- **httpx**: Async HTTP client
  - Used in: API clients
  - Version: >=0.24.0
  - Purpose: Making async HTTP requests

- **pyyaml**: YAML parsing
  - Used in: Configuration files
  - Version: >=6.0.0
  - Purpose: Loading YAML configuration files

## Development Dependencies

### Testing
- **pytest**: Testing framework
  - Version: >=7.0.0
  - Purpose: Running unit and integration tests

- **pytest-asyncio**: Async test support
  - Version: >=0.21.0
  - Purpose: Testing async functions

- **pytest-cov**: Test coverage
  - Version: >=4.1.0
  - Purpose: Measuring test coverage

### Code Quality
- **black**: Code formatting
  - Version: >=23.0.0
  - Purpose: Maintaining consistent code style

- **isort**: Import sorting
  - Version: >=5.12.0
  - Purpose: Organizing imports

- **flake8**: Code linting
  - Version: >=6.0.0
  - Purpose: Checking code quality

- **mypy**: Type checking
  - Version: >=1.5.0
  - Purpose: Static type checking

### Documentation
- **mkdocs**: Documentation generator
  - Version: >=1.5.0
  - Purpose: Building documentation site

- **mkdocs-material**: Documentation theme
  - Version: >=9.0.0
  - Purpose: Material theme for documentation

- **pdoc3**: API documentation
  - Version: >=0.10.0
  - Purpose: Generating API documentation

## Optional Dependencies

### Visualization
- **matplotlib**: Plotting library
  - Version: >=3.7.0
  - Purpose: Creating visualizations in examples

- **jupyter**: Notebook support
  - Version: >=1.0.0
  - Purpose: Running example notebooks

## System Requirements

- Python >= 3.9
- Virtual environment recommended
- Sufficient disk space for model caches
- Internet connection for API access

## API Keys Required

1. Qwen API Key
   - Environment variable: `QWEN_API_KEY`
   - Obtain from: Alibaba Cloud

2. OpenAI API Key (optional)
   - Environment variable: `OPENAI_API_KEY`
   - Obtain from: OpenAI

3. Gemini API Key (optional)
   - Environment variable: `GEMINI_API_KEY`
   - Obtain from: Google Cloud Console 