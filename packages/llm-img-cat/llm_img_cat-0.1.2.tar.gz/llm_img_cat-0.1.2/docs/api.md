# API Documentation

## Book Cover Detection API

The package provides a simple and powerful API for detecting book covers in images.

### Main Function

```python
def llm_img_cat(image_path: str, category: str = "book_cover") -> Dict:
    """
    Analyze if an image is a book cover.
    
    Args:
        image_path (str): Path to the image file
        category (str): Currently only supports "book_cover"
        
    Returns:
        Dict: {
            "is_category": bool,      # True if image is a book cover
            "confidence": float,      # Similarity score (0-100%)
            "reasoning": str          # 5-word explanation
        }
    """
```

### Response Format

The function returns a dictionary with the following structure:

```python
{
    "is_category": True,             # Boolean: is it a book cover?
    "confidence": 90.0,              # Float: similarity score 0-100%
    "reasoning": "Classic book cover with title"  # String: 5-word explanation
}
```

In case of errors:
```python
{
    "error": "Error message here",   # String: error description
    "is_category": False,            # Boolean: defaults to False
    "confidence": 0.0,               # Float: defaults to 0%
    "reasoning": "Error during analysis: ..."  # String: error explanation
}
```

### Raw API Response

The raw API response from Qwen is in JSON format:
```json
{
    "is_book_cover": true,
    "similarity_score": 90,
    "reasoning": "Text and design typical of books"
}
```

### Environment Variables

Required variables in `.env`:
```bash
DASHSCOPE_API_KEY=your_api_key_here
DEFAULT_MODEL=qwen2.5-vl-3b-instruct
QWEN_API_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
```

### Error Handling

The API handles several types of errors:
1. File not found
2. Invalid API key
3. Network errors
4. Invalid image format
5. API response parsing errors

### Example Usage

```python
from llm_img_cat.categorizer import llm_img_cat

try:
    # Analyze a book cover
    result = llm_img_cat("path/to/image.jpg")
    
    if result["is_category"]:
        print(f"This is a book cover! ({result['confidence']}% sure)")
        print(f"Reason: {result['reasoning']}")
    else:
        print(f"This is not a book cover. ({result['confidence']}% similarity)")
        print(f"Reason: {result['reasoning']}")
        
except Exception as e:
    print(f"Error: {str(e)}")
```

### CLI Interface

The package includes a CLI tool for easy testing:
```bash
python scripts/llm_img_cat_cli.py path/to/image.jpg
```

The CLI provides a rich, colorful output with:
- Detection result (Yes/No)
- Similarity score (0-100%)
- Concise reasoning
- Raw API response 