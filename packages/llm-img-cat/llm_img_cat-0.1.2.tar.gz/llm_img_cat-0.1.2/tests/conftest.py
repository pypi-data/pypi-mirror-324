"""Common test fixtures and configurations."""
import os
import pytest
from pathlib import Path
import tempfile
import json
import yaml
from PIL import Image
import numpy as np
import responses

from llm_image_categorizator.classifiers.qwen_classifier import QwenClassifier
from llm_image_categorizator.classifiers.gemini_classifier import GeminiClassifier
from llm_image_categorizator.classifiers.gpt_classifier import GPTClassifier

# Constants
TEST_DATA_DIR = Path(__file__).parent / "data"
SAMPLE_IMAGES_DIR = TEST_DATA_DIR / "sample_images"
MOCK_RESPONSES_DIR = TEST_DATA_DIR / "mock_responses"

# Ensure test directories exist
TEST_DATA_DIR.mkdir(exist_ok=True)
SAMPLE_IMAGES_DIR.mkdir(exist_ok=True)
MOCK_RESPONSES_DIR.mkdir(exist_ok=True)

@pytest.fixture(scope="session")
def test_data_dir():
    """Return path to test data directory."""
    return TEST_DATA_DIR

@pytest.fixture(scope="session")
def sample_images_dir():
    """Return path to sample images directory."""
    return SAMPLE_IMAGES_DIR

@pytest.fixture(scope="session")
def mock_responses_dir():
    """Return path to mock responses directory."""
    return MOCK_RESPONSES_DIR

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)

@pytest.fixture
def sample_image():
    """Create a sample test image."""
    img = Image.new('RGB', (100, 100), color='red')
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        img.save(tmp.name)
        yield Path(tmp.name)
    os.unlink(tmp.name)

@pytest.fixture
def mock_config():
    """Create a sample configuration."""
    return {
        'api_keys': {
            'dashscope': 'test_dashscope_key',
            'openai': 'test_openai_key',
            'google': 'test_google_key'
        },
        'thresholds': {
            'qwen': 0.8,
            'gemini': 0.85,
            'gpt': 0.9
        },
        'cache': {
            'enabled': True,
            'ttl': 3600
        }
    }

@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables."""
    monkeypatch.setenv('DASHSCOPE_API_KEY', 'test_dashscope_key')
    monkeypatch.setenv('OPENAI_API_KEY', 'test_openai_key')
    monkeypatch.setenv('GOOGLE_API_KEY', 'test_google_key')

@pytest.fixture
def qwen_classifier(mock_env):
    """Create a QwenClassifier instance."""
    return QwenClassifier()

@pytest.fixture
def gemini_classifier(mock_env):
    """Create a GeminiClassifier instance."""
    return GeminiClassifier()

@pytest.fixture
def gpt_classifier(mock_env):
    """Create a GPTClassifier instance."""
    return GPTClassifier()

@pytest.fixture
def mock_api_responses():
    """Mock API responses for all classifiers."""
    with responses.RequestsMock() as rsps:
        # Mock Qwen API response
        rsps.add(
            responses.POST,
            "https://dashscope.aliyuncs.com/api/v1/services/vision/image-classification",
            json={
                "output": {
                    "predictions": [
                        {"label": "book_cover", "score": 0.95}
                    ]
                }
            },
            status=200
        )
        
        # Mock Gemini API response
        rsps.add(
            responses.POST,
            "https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision",
            json={
                "candidates": [
                    {
                        "content": {
                            "parts": [
                                {"text": "This image appears to be a book cover"}
                            ]
                        },
                        "safetyRatings": []
                    }
                ]
            },
            status=200
        )
        
        # Mock GPT API response
        rsps.add(
            responses.POST,
            "https://api.openai.com/v1/chat/completions",
            json={
                "choices": [
                    {
                        "message": {
                            "content": "This is a book cover image"
                        }
                    }
                ]
            },
            status=200
        )
        yield rsps

@pytest.fixture
def load_mock_response():
    """Load mock response from file."""
    def _load(filename):
        path = MOCK_RESPONSES_DIR / filename
        if not path.exists():
            return None
        with open(path) as f:
            return json.load(f)
    return _load

@pytest.fixture
def save_mock_response():
    """Save mock response to file."""
    def _save(filename, data):
        path = MOCK_RESPONSES_DIR / filename
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    return _save 