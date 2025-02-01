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

class ImageCategorizer:
    """Main class for image categorization using LLM."""
    
    def __init__(self, api_key: str = None, api_base: str = None, model: str = None):
        """Initialize the categorizer.
        
        Args:
            api_key (str, optional): DASHSCOPE_API_KEY. If None, will be read from env
            api_base (str, optional): API base URL. If None, will use default
            model (str, optional): Model to use. If None, will be read from env
        """
        # Load environment variables from main .env file only
        env_path = Path(".env")
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=True)
        
        self.api_key = api_key or os.getenv('DASHSCOPE_API_KEY')
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY not found in environment or constructor!")
            
        self.model = model or os.getenv('DEFAULT_MODEL')
        if not self.model:
            raise ValueError("Model name not provided and DEFAULT_MODEL not set in environment!")
            
        self.api_base = api_base or os.getenv('QWEN_API_BASE_URL', DEFAULT_API_BASE)
        
        # Initialize OpenAI client
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_base
        )

    def analyze_image(self, image_path: str, category: str) -> Tuple[bool, str, float]:
        """
        Analyze if an image belongs to a specific category.
        
        Args:
            image_path (str): Path to the image file
            category (str): Category to check (e.g., "book_cover")
            
        Returns:
            Tuple[bool, str, float]: (is_category, reasoning, confidence)
        """
        # Check if image exists
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Encode image
        base64_image = encode_image_to_base64(image_path)
        
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
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                response_format={ "type": "json_object" }
            )
            
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

    def categorize_image(self, image_path: str, category: str = "book_cover") -> Dict:
        """
        Main method to categorize images.
        
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
            is_category, reasoning, confidence = self.analyze_image(image_path, category)
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