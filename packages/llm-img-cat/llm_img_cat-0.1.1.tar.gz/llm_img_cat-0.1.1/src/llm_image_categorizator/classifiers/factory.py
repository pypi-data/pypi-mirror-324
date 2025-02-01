"""Factory for creating image classifiers."""
import logging
import os
from pathlib import Path
from typing import Dict, Type, List
from dotenv import load_dotenv

from .base import BaseClassifier, CascadeClassifier, CategoryResult
from .image_validators import BookCoverValidator
from .qwen_classifier import QwenClassifier
from .gemini_classifier import GeminiClassifier
from .gpt_classifier import GPTClassifier

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Load model configurations from environment
MODEL_CONFIGS = {
    "qwen": {
        "class": QwenClassifier,
        "models": os.getenv("QWEN_MODELS", "").split(",") if os.getenv("QWEN_MODELS") else [],
        "api_key": "DASHSCOPE_API_KEY"
    },
    "gemini": {
        "class": GeminiClassifier,
        "models": os.getenv("GEMINI_MODELS", "").split(",") if os.getenv("GEMINI_MODELS") else [],
        "api_key": "GOOGLE_API_KEY"
    },
    "gpt": {
        "class": GPTClassifier,
        "models": os.getenv("GPT_MODELS", "").split(",") if os.getenv("GPT_MODELS") else [],
        "api_key": "OPENAI_API_KEY"
    }
}

def get_model_family(model_name: str) -> tuple[str, Type[BaseClassifier]]:
    """Get the model family and classifier class for a given model name."""
    for family, config in MODEL_CONFIGS.items():
        if any(model_name.startswith(model) for model in config["models"]):
            return family, config["class"]
    supported_models = [model for config in MODEL_CONFIGS.values() for model in config["models"]]
    raise ValueError(f"Unsupported model: {model_name}. Available models must be set in environment variables: QWEN_MODELS, GEMINI_MODELS, or GPT_MODELS")

def create_classifier(model_name: str = None, confidence_threshold: float = 0.8) -> BaseClassifier:
    """Create a classifier instance."""
    # Use default model if none specified
    if model_name is None:
        model_name = os.getenv("DEFAULT_MODEL")
        if not model_name:
            raise ValueError("DEFAULT_MODEL environment variable must be set")
        logger.info(f"Using model from environment: {model_name}")
    
    # Create classifier based on model family
    family, classifier_class = get_model_family(model_name)
    classifier = classifier_class(model_name=model_name, confidence_threshold=confidence_threshold)
    
    # Add validation wrapper
    validator = BookCoverValidator()
    return ValidatedClassifier(classifier, validator)

class ValidatedClassifier(BaseClassifier):
    """Wrapper that adds validation to any classifier."""
    
    def __init__(self, classifier: BaseClassifier, validator: BookCoverValidator):
        super().__init__(classifier.model_name, classifier.confidence_threshold)
        self.classifier = classifier
        self.validator = validator
    
    async def setup(self):
        """Setup wrapped classifier."""
        await self.classifier.setup()
    
    async def classify(self, image_path: Path) -> CategoryResult:
        """Validate and classify image."""
        # Validate first
        if not await self.validator.validate(image_path):
            return CategoryResult(
                category="invalid_image",
                confidence=1.0,
                metadata={"reason": "Failed validation"},
                model_used=self.model_name
            )
        
        # Then classify
        return await self.classifier.classify(image_path)
    
    async def batch_classify(self, image_paths: List[Path]) -> List[CategoryResult]:
        """Validate and classify batch of images."""
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
    
    def get_prompt(self) -> str:
        """Get prompt from wrapped classifier."""
        return self.classifier.get_prompt()

class ClassifierFactory:
    """Factory for creating image classifiers."""
    
    _classifiers: Dict[str, Type[BaseClassifier]] = {
        "qwen": QwenClassifier,
        "gemini": GeminiClassifier,
        "gpt": GPTClassifier,
    }
    
    @classmethod
    async def create(cls, classifier_type: str = "book_cover", **kwargs) -> BaseClassifier:
        """Create and setup a classifier instance."""
        if classifier_type == "book_cover":
            # Create cascade classifier with fallback chain
            classifiers = []
            cascade_config = [
                ("qwen", 0.8),    # Primary classifier
                ("gemini", 0.85), # Secondary classifier
                ("gpt", 0.9),     # Tertiary classifier
            ]
            
            # Initialize classifiers
            for model_type, threshold in cascade_config:
                try:
                    classifier = cls._classifiers[model_type](confidence_threshold=threshold)
                    await classifier.setup()
                    classifiers.append(classifier)
                    logger.info(f"Initialized {model_type} classifier with threshold {threshold}")
                except Exception as e:
                    logger.error(f"Failed to initialize {model_type} classifier: {e}")
            
            if not classifiers:
                raise ValueError("No classifiers could be initialized")
            
            # Create cascade with validation
            validator = BookCoverValidator()
            cascade = CascadeClassifier(classifiers)
            return ValidatedClassifier(cascade, validator)
        
        # For other types, create single classifier
        if classifier_type not in cls._classifiers:
            raise ValueError(f"Unknown classifier type: {classifier_type}")
        
        classifier = cls._classifiers[classifier_type](**kwargs)
        await classifier.setup()
        return classifier 