# Usage Examples

## Basic Examples

### Simple Image Classification

```python
from llm_image_categorizator.categorization import QwenClassifier
from llm_image_categorizator.config import BaseConfig
import base64

# Initialize configuration
config = BaseConfig.from_env()

# Create classifier
classifier = QwenClassifier(config=config)

# Load and encode image
with open("book_cover.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

# Classify image
result = classifier.classify_image(image_data)

print(f"Is book cover: {result['is_book_cover']}")
print(f"Confidence: {result['confidence']:.2f}")
print(f"Model used: {result['model_name']}")
print(f"Processing time: {result['processing_time']:.2f}s")
```

### Using Multiple Models

```python
from llm_image_categorizator.categorization import (
    QwenClassifier,
    GeminiClassifier,
    GPTClassifier
)

# Create classifiers
classifiers = [
    QwenClassifier(config=config),
    GeminiClassifier(config=config),
    GPTClassifier(config=config)
]

# Classify with all models
results = []
for classifier in classifiers:
    result = classifier.classify_image(image_data)
    results.append(result)

# Compare results
for result in results:
    print(f"\nModel: {result['model_name']}")
    print(f"Is book cover: {result['is_book_cover']}")
    print(f"Confidence: {result['confidence']:.2f}")
```

## Advanced Examples

### Batch Processing

```python
import os
from pathlib import Path

# Get all images in a directory
image_dir = Path("test_images")
image_files = list(image_dir.glob("*.jpg"))

# Process all images
results = []
for image_file in image_files:
    with open(image_file, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()
    
    result = classifier.classify_image(image_data)
    results.append({
        "file": image_file.name,
        **result
    })

# Print results
for result in results:
    print(f"\nFile: {result['file']}")
    print(f"Is book cover: {result['is_book_cover']}")
    print(f"Confidence: {result['confidence']:.2f}")
```

### Using Fallback Chain

```python
from llm_image_categorizator.categorization import ClassifierChain

# Create fallback chain
chain = ClassifierChain([
    QwenClassifier(config=config),
    GeminiClassifier(config=config),
    GPTClassifier(config=config)
])

# Classify with fallback
try:
    result = chain.classify_image(image_data)
    print(f"Successfully classified using {result['model_name']}")
except Exception as e:
    print(f"All models failed: {e}")
```

### Custom Configuration

```python
# Create custom configuration
config = BaseConfig(
    default_model="qwen-vl-plus",
    fallback_models=["gemini-pro-vision"],
    max_retries=5,
    timeout=60
)

# Add model-specific settings
config.model_settings = {
    "qwen-vl-plus": {
        "max_tokens": 2048,
        "temperature": 0.7,
        "confidence_threshold": 0.8
    }
}

# Create classifier with custom config
classifier = QwenClassifier(config=config)
```

### Error Handling

```python
from llm_image_categorizator.exceptions import (
    InvalidImageError,
    ModelError,
    ConfigurationError
)

try:
    result = classifier.classify_image(image_data)
except InvalidImageError as e:
    print(f"Image validation failed: {e}")
except ModelError as e:
    print(f"Model error: {e}")
    # Try fallback model
    fallback_classifier = GeminiClassifier(config=config)
    result = fallback_classifier.classify_image(image_data)
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

### Using Caching

```python
from llm_image_categorizator.utils import enable_cache, disable_cache

# Enable caching
enable_cache()

# First call (API request)
result1 = classifier.classify_image(image_data)

# Second call (cache hit)
result2 = classifier.classify_image(image_data)

# Disable caching
disable_cache()
```

### Custom Image Validation

```python
from llm_image_categorizator.utils import validate_image
from PIL import Image
import io

def custom_validate(image_data: str) -> bool:
    """Custom image validation."""
    try:
        # Decode base64
        image_bytes = base64.b64decode(image_data)
        
        # Open image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Check size
        if image.size[0] < 300 or image.size[1] < 300:
            return False
        
        # Check format
        if image.format not in ["JPEG", "PNG"]:
            return False
        
        return True
    except Exception:
        return False

# Use custom validation
classifier.validate_image = custom_validate
```

### Async Processing

```python
import asyncio
from llm_image_categorizator.categorization import AsyncQwenClassifier

async def process_images(image_files):
    """Process multiple images asynchronously."""
    classifier = AsyncQwenClassifier(config=config)
    tasks = []
    
    for image_file in image_files:
        with open(image_file, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()
        task = classifier.classify_image(image_data)
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return results

# Run async processing
results = asyncio.run(process_images(image_files))
```

## Integration Examples

### Web API Integration

```python
from fastapi import FastAPI, File, UploadFile
import base64
import io

app = FastAPI()
classifier = QwenClassifier(config=config)

@app.post("/classify")
async def classify_image(file: UploadFile):
    """Classify uploaded image."""
    contents = await file.read()
    image_data = base64.b64encode(contents).decode()
    
    result = classifier.classify_image(image_data)
    return result
```

### CLI Tool

```python
import click

@click.command()
@click.argument("image_path")
@click.option("--model", default="qwen-vl-plus", help="Model to use")
def classify(image_path, model):
    """Classify an image from command line."""
    config = BaseConfig(default_model=model)
    classifier = QwenClassifier(config=config)
    
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()
    
    result = classifier.classify_image(image_data)
    click.echo(f"Is book cover: {result['is_book_cover']}")
    click.echo(f"Confidence: {result['confidence']:.2f}")

if __name__ == "__main__":
    classify()
```

## Best Practices

1. Always validate images before processing
2. Use appropriate confidence thresholds
3. Implement proper error handling
4. Enable caching for repeated operations
5. Use environment variables for API keys
6. Monitor API usage and limits
7. Implement fallback strategies
8. Keep configuration organized
9. Document custom implementations
10. Follow security guidelines 