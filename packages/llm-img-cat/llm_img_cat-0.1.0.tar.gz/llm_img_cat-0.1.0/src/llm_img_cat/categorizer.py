"""Image categorization using Qwen VL model."""
import os
import json
import base64
from pathlib import Path
from typing import Dict, Tuple
from openai import OpenAI
from dotenv import load_dotenv

# Default values from QwenClassifier
DEFAULT_API_BASE = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

def encode_image_to_base64(image_path: str) -> str:
    """Convert image to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(image_path: str, category: str) -> Tuple[bool, str, float]:
    """
    Analyze if an image belongs to a specific category.
    
    Args:
        image_path (str): Path to the image file
        category (str): Category to check (e.g., "book_cover")
        
    Returns:
        Tuple[bool, str, float]: (is_category, reasoning, confidence)
    """
    print("Starting image analysis...")
    
    # Load environment variables from main .env file only
    env_path = Path(".env")
    if not env_path.exists():
        raise ValueError("ERROR: .env file not found!")
    
    load_dotenv(dotenv_path=env_path, override=True)
    
    # Print all relevant environment variables for debugging
    print("\nEnvironment variables:")
    print("-" * 20)
    api_key = os.getenv('DASHSCOPE_API_KEY')
    print(f"DASHSCOPE_API_KEY: {'[SET]' if api_key else '[NOT SET]'}")
    if api_key:
        print(f"API Key length: {len(api_key)}")
        print(f"API Key preview: {api_key[:5]}...")
    
    model = os.getenv('DEFAULT_MODEL')
    if not model:
        raise ValueError("ERROR: DEFAULT_MODEL not set in environment!")
    print(f"DEFAULT_MODEL: {model}")
    
    api_base = os.getenv('QWEN_API_BASE_URL', DEFAULT_API_BASE)
    print(f"QWEN_API_BASE_URL: {api_base}")
    print("-" * 20)
    
    # Check if image exists
    if not Path(image_path).exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    # Encode image
    base64_image = encode_image_to_base64(image_path)
    
    # Initialize OpenAI client
    client = OpenAI(
        api_key=api_key,
        base_url=api_base
    )
    
    # Create the analysis prompt
    prompt = f"""Analyze this image and determine if it is a {category}.
Please provide your response in the following JSON format:
{{
    "is_{category}": true/false,
    "similarity_score": <number 0-100>,
    "reasoning": "EXACTLY 5 WORDS"
}}

Guidelines:
- is_{category}: boolean, your final decision
- similarity_score: How much does this image match a {category}?
  * 100 = perfect match, definitely a {category}
  * 80-99 = has most {category} characteristics
  * 60-79 = has some {category} characteristics
  * 40-59 = ambiguous or unclear
  * 20-39 = few {category} characteristics
  * 0-19 = almost no {category} characteristics
  * 0 = absolutely nothing like a {category}
- reasoning: EXACTLY 5 words explaining your decision
"""
    
    # Create the message with image
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
    
    try:
        # Get the response
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=500,
            response_format={ "type": "json_object" }
        )
        
        # Print raw JSON for debugging
        print("\nRaw API Response:")
        print("-" * 20)
        print(json.dumps(json.loads(response.choices[0].message.content), indent=2))
        print("-" * 20)
        
        # Parse response using json
        result = json.loads(response.choices[0].message.content)
        
        # Get similarity score (backward compatible with old confidence)
        similarity = result.get("similarity_score", result.get("confidence_in_percentage", result.get("confidence", 0)))
        
        return (
            result[f"is_{category}"],
            result["reasoning"],
            similarity
        )
        
    except Exception as e:
        raise RuntimeError(f"Error during image analysis: {str(e)}")

def llm_img_cat(image_path: str, category: str = "book_cover") -> Dict:
    """
    CLI-friendly function to categorize images.
    
    Args:
        image_path (str): Path to the image file
        category (str): Category to check (default: "book_cover")
        
    Returns:
        Dict: {
            "is_category": bool,
            "confidence": float,
            "reasoning": str
        }
    """
    try:
        is_category, reasoning, confidence = analyze_image(image_path, category)
        return {
            "is_category": is_category,
            "confidence": confidence,
            "reasoning": reasoning
        }
    except Exception as e:
        return {
            "error": str(e),
            "is_category": False,
            "confidence": 0.0,
            "reasoning": f"Error during analysis: {str(e)}"
        } 