"""Integration tests for Qwen classifier."""
import pytest
from pathlib import Path
import base64
from typing import Dict, Any

from llm_image_categorizator.src.config import BaseConfig
from llm_image_categorizator.src.categorization.qwen_classifier import QwenClassifier

def encode_image(image_path: Path) -> str:
    """Encode image to base64."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

@pytest.fixture
def qwen_classifier(test_config) -> QwenClassifier:
    """Create a Qwen classifier instance."""
    return QwenClassifier(config=test_config)

@pytest.mark.integration
def test_classifier_initialization(qwen_classifier):
    """Test classifier initialization."""
    assert qwen_classifier.model_name == "qwen-vl-plus"
    assert qwen_classifier.config is not None

@pytest.mark.integration
def test_image_validation(qwen_classifier, mock_image_path):
    """Test image validation."""
    # Test with valid image
    encoded_image = encode_image(mock_image_path)
    assert qwen_classifier.validate_image(encoded_image) is True
    
    # Test with invalid base64
    with pytest.raises(ValueError):
        qwen_classifier.validate_image("invalid-base64")

@pytest.mark.integration
@pytest.mark.skipif(not os.getenv("DASHSCOPE_API_KEY"), reason="DashScope API key not set")
def test_classify_image(qwen_classifier, mock_image_path):
    """Test image classification."""
    encoded_image = encode_image(mock_image_path)
    result = qwen_classifier.classify_image(encoded_image)
    
    assert isinstance(result, dict)
    assert "is_book_cover" in result
    assert isinstance(result["is_book_cover"], bool)
    assert "confidence" in result
    assert isinstance(result["confidence"], float)
    assert 0 <= result["confidence"] <= 1

@pytest.mark.integration
def test_error_handling(qwen_classifier):
    """Test error handling."""
    # Test with empty image
    with pytest.raises(ValueError):
        qwen_classifier.classify_image("")
    
    # Test with invalid image data
    with pytest.raises(ValueError):
        qwen_classifier.classify_image("invalid-data")

@pytest.mark.integration
def test_confidence_threshold(qwen_classifier, mock_image_path):
    """Test confidence threshold behavior."""
    encoded_image = encode_image(mock_image_path)
    
    # Test with different thresholds
    thresholds = [0.5, 0.8, 0.9]
    for threshold in thresholds:
        qwen_classifier.confidence_threshold = threshold
        result = qwen_classifier.classify_image(encoded_image)
        
        assert result["confidence"] >= 0
        if result["is_book_cover"]:
            assert result["confidence"] >= threshold

@pytest.mark.integration
def test_batch_classification(qwen_classifier, test_data_dir):
    """Test batch image classification."""
    image_files = list(test_data_dir.glob("*.jpg"))
    assert len(image_files) > 0, "No test images found"
    
    results = []
    for image_path in image_files:
        encoded_image = encode_image(image_path)
        result = qwen_classifier.classify_image(encoded_image)
        results.append(result)
    
    assert len(results) == len(image_files)
    for result in results:
        assert isinstance(result, dict)
        assert "is_book_cover" in result
        assert "confidence" in result 