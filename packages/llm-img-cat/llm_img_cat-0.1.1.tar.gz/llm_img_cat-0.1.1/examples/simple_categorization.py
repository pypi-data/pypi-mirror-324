"""Simple example of using the LLM Image Categorization API."""
import asyncio
from pathlib import Path

from llm_image_categorizator import llm_img_cat, llm_img_cat_sync

async def async_example():
    """Example of async usage."""
    # Get path to example image
    image_path = Path("tests/data/images/book_covers/manual/example_book.jpg")
    
    # Define category to check
    category = "book cover"
    
    try:
        # Classify image
        result = await llm_img_cat(image_path, category)
        
        # Print results
        print(f"\nResults for {image_path.name}:")
        print(f"Is {category}? {'Yes' if result['is_match'] else 'No'}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Reasoning: {result['reasoning']}")
        print(f"Model used: {result['model_used']}")
        print(f"Processing time: {result['processing_time']:.2f}s")
        
    except Exception as e:
        print(f"Error: {e}")

def sync_example():
    """Example of synchronous usage."""
    image_path = Path("tests/data/images/book_covers/manual/example_book.jpg")
    category = "book cover"
    
    try:
        result = llm_img_cat_sync(image_path, category)
        
        print(f"\nResults for {image_path.name}:")
        print(f"Is {category}? {'Yes' if result['is_match'] else 'No'}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Reasoning: {result['reasoning']}")
        print(f"Model used: {result['model_used']}")
        print(f"Processing time: {result['processing_time']:.2f}s")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Running async example...")
    asyncio.run(async_example())
    
    print("\nRunning sync example...")
    sync_example() 