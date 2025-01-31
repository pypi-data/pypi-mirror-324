"""Main API for LLM Image Categorization."""
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Union, Dict, Any

from .classifiers import create_classifier, CategoryResult
from .classifiers.image_validators import validate_image_path

async def llm_img_cat(path_to_image: Union[str, Path], category: str) -> Dict[str, Any]:
    """
    Determine if an image matches a given category using LLM-based image analysis.
    
    Args:
        path_to_image: Path to the image file (supports jpg, jpeg, png formats)
        category: Text description of the category to check (e.g., "book cover")
    
    Returns:
        dict: A dictionary containing:
            - is_match (bool): Whether the image matches the category
            - confidence (float): Confidence score between 0 and 1
            - reasoning (str): Explanation of the decision
            - model_used (str): Name of the LLM model used
            - processing_time (float): Time taken in seconds
    
    Raises:
        FileNotFoundError: If the image file doesn't exist
        ValueError: If the image format is invalid or category is empty
        RuntimeError: If classification fails
    """
    # Convert string path to Path object
    image_path = Path(path_to_image)
    
    # Validate inputs
    if not category.strip():
        raise ValueError("Category description cannot be empty")
    
    # Validate image path and format
    validate_image_path(image_path)
    
    # Record start time
    start_time = datetime.now()
    
    try:
        # Create and setup classifier
        classifier = create_classifier()
        await classifier.setup()
        
        # Perform classification
        result: CategoryResult = await classifier.classify(image_path)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Prepare response
        response = {
            "is_match": result.confidence >= classifier.confidence_threshold,
            "confidence": result.confidence,
            "reasoning": result.metadata.get("reasoning", "No reasoning provided"),
            "model_used": result.model_used,
            "processing_time": processing_time
        }
        
        return response
        
    except Exception as e:
        raise RuntimeError(f"Classification failed: {str(e)}") from e

def llm_img_cat_sync(path_to_image: Union[str, Path], category: str) -> Dict[str, Any]:
    """
    Synchronous version of llm_img_cat.
    
    This is a convenience wrapper for environments where async/await cannot be used.
    """
    return asyncio.run(llm_img_cat(path_to_image, category))

# Example usage
if __name__ == "__main__":
    # Async usage
    async def main():
        result = await llm_img_cat("path/to/image.jpg", "book cover")
        print(json.dumps(result, indent=2))
    
    # Sync usage
    # result = llm_img_cat_sync("path/to/image.jpg", "book cover")
    # print(json.dumps(result, indent=2))
    
    asyncio.run(main()) 