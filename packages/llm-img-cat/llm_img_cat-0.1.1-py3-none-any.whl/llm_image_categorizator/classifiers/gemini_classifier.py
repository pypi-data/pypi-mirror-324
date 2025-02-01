"""Gemini Pro Vision model for image classification."""
import base64
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List
import google.generativeai as genai
import os
from dotenv import load_dotenv

from .base import BaseClassifier, CategoryResult

logger = logging.getLogger(__name__)

class GeminiClassifier(BaseClassifier):
    """Image classifier using Gemini Pro Vision model."""
    
    def __init__(self, model_name: str = None, confidence_threshold: float = 0.85):
        # Use model name from environment
        if model_name is None:
            model_name = os.getenv("DEFAULT_MODEL")
            if not model_name:
                raise ValueError("DEFAULT_MODEL environment variable must be set")
        super().__init__(model_name, confidence_threshold)
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    async def setup(self):
        """Initialize the Gemini client."""
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
    
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
        """Classify a book cover image using Gemini Pro Vision."""
        start_time = datetime.now()
        
        try:
            # Read image
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
            
            # Generate response
            response = self.model.generate_content([
                self.get_prompt(),
                {"mime_type": "image/jpeg", "data": image_data}
            ])
            
            try:
                # Parse response
                result = json.loads(response.text)
                
                return CategoryResult(
                    category=result["category"],
                    confidence=float(result["confidence"]),
                    metadata={"explanation": result["explanation"]},
                    model_used=self.model_name,
                    processing_time=(datetime.now() - start_time).total_seconds()
                )
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Failed to parse Gemini response: {e}")
                return CategoryResult(
                    category="error",
                    confidence=0.0,
                    metadata={"error": str(e), "raw_response": response.text},
                    model_used=self.model_name,
                    processing_time=(datetime.now() - start_time).total_seconds()
                )
                
        except Exception as e:
            logger.error(f"Gemini classification failed: {e}")
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