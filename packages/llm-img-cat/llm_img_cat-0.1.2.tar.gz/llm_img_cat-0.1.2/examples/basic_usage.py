"""
Basic Usage Example for llm_img_cat Package
=========================================

This example demonstrates how to use the llm_img_cat package for image categorization.
Before running this example, make sure to:

1. Install the package:
   pip install llm_img_cat==0.1.2

2. Set up your API key:
   export DASHSCOPE_API_KEY="your_api_key_here"
"""

import os
from llm_img_cat import ImageCategorizer

def main():
    # Check for API key
    if 'DASHSCOPE_API_KEY' not in os.environ:
        print("⚠️ Please set your DASHSCOPE_API_KEY environment variable!")
        print("Example: export DASHSCOPE_API_KEY='your_api_key_here'")
        return

    try:
        # Initialize the categorizer
        print("🚀 Initializing ImageCategorizer...")
        categorizer = ImageCategorizer()

        # Example with a remote image URL
        print("\n📚 Testing with a book cover image...")
        test_url = "https://raw.githubusercontent.com/almazkun/llm_img_cat/main/tests/data/test_image.jpg"
        result = categorizer.categorize_image(test_url)

        # Print results
        print("\n🔍 Results:")
        print(f"Is book cover: {result['is_category']}")
        print(f"Confidence: {result['confidence']}%")
        print(f"Reasoning: {result['reasoning']}")

        # Example with error handling
        print("\n⚠️ Testing error handling with invalid URL...")
        invalid_result = categorizer.categorize_image("invalid_url")
        print(f"Error handling: {invalid_result.get('error', 'No error')}")

    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        print("\n💡 Troubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Verify your API key is correct")
        print("3. Ensure the image URL is accessible")

if __name__ == "__main__":
    main() 