# LLM Image Categorization API Reference

## Quick Start

```python
from llm_image_categorizator import llm_img_cat, llm_img_cat_sync

# Async usage
async def check_image():
    result = await llm_img_cat("path/to/image.jpg", "book cover")
    print(f"Is book cover: {result['is_match']}")

# Sync usage
result = llm_img_cat_sync("path/to/image.jpg", "book cover")
print(f"Is book cover: {result['is_match']}")
```

## Core Functions

### `llm_img_cat`

```python
async def llm_img_cat(
    path_to_image: Union[str, Path],
    category: str
) -> Dict[str, Any]
```

Asynchronously determines if an image matches a given category using LLM-based image analysis.

#### Parameters:
- `path_to_image` (str | Path): Path to the image file
  - Supported formats: JPG, JPEG, PNG
  - Can be string or Path object
  - File must exist and be readable
  
- `category` (str): Category description to check against
  - Must be non-empty string
  - Can be simple (e.g., "book cover") or detailed (e.g., "vintage science fiction book cover")
  - Language: English recommended for best results

#### Returns:
Dictionary containing:
```python
{
    "is_match": bool,        # True if image matches category
    "confidence": float,     # 0.0 to 1.0 confidence score
    "reasoning": str,        # Explanation of the decision
    "model_used": str,       # Name of LLM model used
    "processing_time": float # Time taken in seconds
}
```

#### Raises:
- `FileNotFoundError`: Image file doesn't exist
- `ValueError`: Invalid image format or empty category
- `RuntimeError`: Classification failed (with details)

#### Example:
```python
async def example():
    result = await llm_img_cat(
        "book.jpg",
        "science fiction book cover"
    )
    
    if result["is_match"]:
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Reasoning: {result['reasoning']}")
```

### `llm_img_cat_sync`

```python
def llm_img_cat_sync(
    path_to_image: Union[str, Path],
    category: str
) -> Dict[str, Any]
```

Synchronous wrapper for `llm_img_cat`. Identical functionality but can be used in non-async contexts.

#### Example:
```python
result = llm_img_cat_sync("cover.jpg", "book cover")
print(f"Is book cover: {result['is_match']}")
```

## Configuration

### Environment Variables

Required:
- `DASHSCOPE_API_KEY`: API key for Qwen/Gwen (primary model)

Optional:
- `OPENAI_API_KEY`: For GPT-4V support
- `GEMINI_API_KEY`: For Google Gemini support
- `DEFAULT_MODEL`: Override default model choice

### Performance Considerations

1. **First Run**:
   - Initial call may take longer (model loading)
   - Subsequent calls are faster

2. **Image Size**:
   - Large images are automatically resized
   - Optimal size: 1024x1024 pixels or smaller
   - Supported aspect ratios: Any

3. **Response Time**:
   - Typical: 2-4 seconds
   - Maximum: 5 seconds
   - Network dependent

## Best Practices

1. **Category Descriptions**:
   ```python
   # Good - Clear and specific
   "book cover"
   "hardcover science fiction book"
   
   # Bad - Too vague or complex
   ""  # Empty
   "maybe some kind of book or magazine cover"
   ```

2. **Error Handling**:
   ```python
   try:
       result = await llm_img_cat(image_path, category)
   except FileNotFoundError:
       print("Image file not found")
   except ValueError as e:
       print(f"Invalid input: {e}")
   except RuntimeError as e:
       print(f"Classification failed: {e}")
   ```

3. **Performance Optimization**:
   ```python
   # Reuse classifier for multiple images
   async def batch_process(image_paths):
       results = []
       for path in image_paths:
           result = await llm_img_cat(path, "book cover")
           results.append(result)
       return results
   ```

## Common Issues

1. **Authentication Errors**:
   - Check API key environment variables
   - Verify API key validity
   - Ensure network connectivity

2. **Performance Issues**:
   - Check image size
   - Monitor network speed
   - Consider caching for repeated queries

3. **Accuracy Issues**:
   - Use specific category descriptions
   - Ensure image quality
   - Try alternative model if available

## Model Selection

The package automatically selects the best available model:

1. **Qwen** (Primary):
   - Best overall performance
   - Fastest response time
   - Most cost-effective

2. **Gemini** (Fallback):
   - Good alternative
   - Different strengths
   - May require separate API key

3. **GPT-4V** (Optional):
   - Highest accuracy
   - Slower response time
   - Higher cost

## Advanced Usage

### Custom Category Validation:
```python
from llm_image_categorizator.validators import validate_category

# Custom validation before processing
if validate_category(my_category):
    result = await llm_img_cat(image_path, my_category)
```

### Batch Processing:
```python
async def process_directory(dir_path: Path, category: str):
    tasks = []
    for image_path in dir_path.glob("*.jpg"):
        tasks.append(llm_img_cat(image_path, category))
    return await asyncio.gather(*tasks)
``` 