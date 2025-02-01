"""Base classes for image categorization."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

@dataclass
class CategoryResult:
    """Result of image categorization."""
    category: str
    confidence: float
    metadata: Dict[str, Any]
    model_used: str
    processing_time: Optional[float] = None

class BaseClassifier(ABC):
    """Abstract base class for image classifiers."""
    
    def __init__(self, model_name: str, confidence_threshold: float = 0.8):
        self.model_name = model_name
        self.confidence_threshold = confidence_threshold
    
    @abstractmethod
    async def setup(self):
        """Setup the classifier (load models, initialize clients, etc.)."""
        pass
    
    @abstractmethod
    async def classify(self, image_path: Path) -> CategoryResult:
        """Classify a single image."""
        pass
    
    @abstractmethod
    async def batch_classify(self, image_paths: List[Path]) -> List[CategoryResult]:
        """Classify multiple images."""
        pass
    
    @abstractmethod
    def get_prompt(self) -> str:
        """Get the classification prompt."""
        pass

class CascadeClassifier(BaseClassifier):
    """Classifier that tries multiple models in sequence."""
    
    def __init__(self, classifiers: List[BaseClassifier]):
        super().__init__("cascade")
        self.classifiers = classifiers
    
    async def setup(self):
        """Setup all classifiers in the cascade."""
        for classifier in self.classifiers:
            await classifier.setup()
    
    async def classify(self, image_path: Path) -> CategoryResult:
        """Try each classifier until one succeeds with high confidence."""
        start_time = datetime.now()
        
        for classifier in self.classifiers:
            try:
                result = await classifier.classify(image_path)
                if result.confidence >= classifier.confidence_threshold:
                    result.processing_time = (datetime.now() - start_time).total_seconds()
                    return result
            except Exception as e:
                continue
        
        # If no classifier succeeded with high confidence, return the last result
        if 'result' in locals():
            result.processing_time = (datetime.now() - start_time).total_seconds()
            return result
            
        raise ValueError("All classifiers failed to process the image")
    
    async def batch_classify(self, image_paths: List[Path]) -> List[CategoryResult]:
        """Classify multiple images using the cascade."""
        results = []
        for path in image_paths:
            try:
                result = await self.classify(path)
                results.append(result)
            except Exception as e:
                results.append(CategoryResult(
                    category="error",
                    confidence=0.0,
                    metadata={"error": str(e)},
                    model_used=self.model_name
                ))
        return results
    
    def get_prompt(self) -> str:
        """Get the prompt from the first classifier."""
        return self.classifiers[0].get_prompt() 