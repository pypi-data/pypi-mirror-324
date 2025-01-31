"""Qwen VL model for image classification."""
import base64
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from openai import OpenAI
import os
from dotenv import load_dotenv

from .base import BaseClassifier, CategoryResult

logger = logging.getLogger(__name__)

class QwenClassifier(BaseClassifier):
    """Image classifier using Qwen VL model."""
    
    def __init__(self, model_name: str = None, confidence_threshold: float = 0.8):
        # Use model name from environment
        if model_name is None:
            model_name = os.getenv("DEFAULT_MODEL")
            if not model_name:
                raise ValueError("DEFAULT_MODEL environment variable must be set")
        super().__init__(model_name, confidence_threshold)
        self.client = None
        self.base_url = os.getenv("QWEN_API_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY environment variable not set")
    
    async def setup(self):
        """Initialize the OpenAI client for Qwen."""
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def get_prompt(self) -> str:
        """Get the classification prompt."""
        return """Analyze this book cover image and determine its category. The categories are:
- russian (Russian language book)
- chinese (Chinese language book)
- manual (Manual/instruction book)
- other (Any other type)

Respond in JSON format with category and confidence level (0-1):
{
    "category": "category_name",
    "confidence": confidence_score,
    "explanation": "brief explanation"
}"""
    
    async def classify(self, image_path: Path) -> CategoryResult:
        """Classify a book cover image using Qwen VL."""
        start_time = datetime.now()
        
        try:
            # Convert image to base64
            with open(image_path, "rb") as image_file:
                image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Prepare API request
            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": self.get_prompt()},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]
            }]
            
            # Make API request
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            
            try:
                # Parse response
                result = json.loads(response.choices[0].message.content)
                
                return CategoryResult(
                    category=result["category"],
                    confidence=float(result["confidence"]),
                    metadata={"explanation": result["explanation"]},
                    model_used=self.model_name,
                    processing_time=(datetime.now() - start_time).total_seconds()
                )
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Failed to parse Qwen response: {e}")
                return CategoryResult(
                    category="error",
                    confidence=0.0,
                    metadata={"error": str(e), "raw_response": response.choices[0].message.content},
                    model_used=self.model_name,
                    processing_time=(datetime.now() - start_time).total_seconds()
                )
                
        except Exception as e:
            logger.error(f"Qwen classification failed: {e}")
            return CategoryResult(
                category="error",
                confidence=0.0,
                metadata={"error": str(e)},
                model_used=self.model_name,
                processing_time=(datetime.now() - start_time).total_seconds()
            )
    
    async def batch_classify(self, image_paths: List[Path]) -> List[CategoryResult]:
        """Classify multiple book cover images."""
        results = []
        for path in image_paths:
            try:
                result = await self.classify(path)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to classify {path}: {e}")
                results.append(CategoryResult(
                    category="error",
                    confidence=0.0,
                    metadata={"error": str(e)},
                    model_used=self.model_name
                ))
        return results 