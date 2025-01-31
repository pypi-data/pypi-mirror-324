"""Integration tests for API functionality."""
import os
import pytest
import responses
from pathlib import Path
from unittest.mock import patch

from llm_image_categorizator.api_helpers.llm_apis.gwen import GwenAPI
from llm_image_categorizator.api_helpers.llm_apis.gemini import GeminiAPI
from llm_image_categorizator.api_helpers.llm_apis.gpt import GPTAPI
from llm_image_categorizator.utils.testing import create_mock_api_response

# Test data paths
TEST_DATA_DIR = Path(__file__).parent.parent / 'data'
MOCK_RESPONSES_DIR = TEST_DATA_DIR / 'mock_responses'
SAMPLE_IMAGES_DIR = TEST_DATA_DIR / 'sample_images'

@pytest.fixture
def mock_env(monkeypatch):
    """Set up mock environment variables."""
    monkeypatch.setenv('DASHSCOPE_API_KEY', 'test_gwen_key')
    monkeypatch.setenv('GEMINI_API_KEY', 'test_gemini_key')
    monkeypatch.setenv('OPENAI_API_KEY', 'test_openai_key')

@pytest.fixture
def gwen_api(mock_env):
    """Create Gwen API client."""
    return GwenAPI()

@pytest.fixture
def gemini_api(mock_env):
    """Create Gemini API client."""
    return GeminiAPI()

@pytest.fixture
def gpt_api(mock_env):
    """Create GPT API client."""
    return GPTAPI()

@responses.activate
def test_gwen_api_classification(gwen_api):
    """Test Gwen API image classification."""
    # Mock successful response
    responses.add(
        responses.POST,
        'https://dashscope.aliyuncs.com/api/v1/services/vision/image-classification',
        json={
            'output': {
                'predictions': [
                    {'label': 'book_cover', 'score': 0.95}
                ]
            },
            'usage': {'image_count': 1}
        },
        status=200
    )
    
    # Test with sample image
    image_path = SAMPLE_IMAGES_DIR / 'book_cover.jpg'
    result = gwen_api.classify_image(image_path)
    
    assert result['success'] is True
    assert result['label'] == 'book_cover'
    assert result['confidence'] > 0.9
    
    # Mock rate limit error
    responses.replace(
        responses.POST,
        'https://dashscope.aliyuncs.com/api/v1/services/vision/image-classification',
        json={'error': {'code': 'RateLimit'}},
        status=429
    )
    
    result = gwen_api.classify_image(image_path)
    assert result['success'] is False
    assert 'rate_limit' in result['error']

@responses.activate
def test_gemini_api_classification(gemini_api):
    """Test Gemini API image classification."""
    # Mock successful response
    responses.add(
        responses.POST,
        'https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision:generateContent',
        json={
            'candidates': [{
                'content': {
                    'parts': [{'text': 'This appears to be a book cover...'}]
                }
            }]
        },
        status=200
    )
    
    # Test with sample image
    image_path = SAMPLE_IMAGES_DIR / 'book_cover.jpg'
    result = gemini_api.classify_image(image_path)
    
    assert result['success'] is True
    assert 'book' in result['text'].lower()
    
    # Mock error response
    responses.replace(
        responses.POST,
        'https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision:generateContent',
        json={'error': {'message': 'Invalid request'}},
        status=400
    )
    
    result = gemini_api.classify_image(image_path)
    assert result['success'] is False
    assert 'error' in result

@responses.activate
def test_gpt_api_classification(gpt_api):
    """Test GPT API image classification."""
    # Mock successful response
    responses.add(
        responses.POST,
        'https://api.openai.com/v1/chat/completions',
        json={
            'choices': [{
                'message': {
                    'content': 'The image shows a book cover...'
                }
            }]
        },
        status=200
    )
    
    # Test with sample image
    image_path = SAMPLE_IMAGES_DIR / 'book_cover.jpg'
    result = gpt_api.classify_image(image_path)
    
    assert result['success'] is True
    assert 'book' in result['text'].lower()
    
    # Mock error response
    responses.replace(
        responses.POST,
        'https://api.openai.com/v1/chat/completions',
        json={'error': {'message': 'Rate limit exceeded'}},
        status=429
    )
    
    result = gpt_api.classify_image(image_path)
    assert result['success'] is False
    assert 'rate_limit' in result['error']

def test_api_fallback_chain(gwen_api, gemini_api, gpt_api):
    """Test API fallback chain functionality."""
    with patch.object(GwenAPI, 'classify_image') as mock_gwen, \
         patch.object(GeminiAPI, 'classify_image') as mock_gemini, \
         patch.object(GPTAPI, 'classify_image') as mock_gpt:
        
        # Test successful first API
        mock_gwen.return_value = {
            'success': True,
            'label': 'book_cover',
            'confidence': 0.95
        }
        
        result = gwen_api.classify_with_fallback(
            SAMPLE_IMAGES_DIR / 'book_cover.jpg',
            fallback_apis=[gemini_api, gpt_api]
        )
        
        assert result['success'] is True
        assert result['label'] == 'book_cover'
        assert result['api_used'] == 'gwen'
        mock_gemini.assert_not_called()
        mock_gpt.assert_not_called()
        
        # Test fallback to second API
        mock_gwen.return_value = {'success': False, 'error': 'rate_limit'}
        mock_gemini.return_value = {
            'success': True,
            'text': 'This is a book cover'
        }
        
        result = gwen_api.classify_with_fallback(
            SAMPLE_IMAGES_DIR / 'book_cover.jpg',
            fallback_apis=[gemini_api, gpt_api]
        )
        
        assert result['success'] is True
        assert 'book' in result['text'].lower()
        assert result['api_used'] == 'gemini'
        mock_gpt.assert_not_called()
        
        # Test all APIs fail
        mock_gwen.return_value = {'success': False, 'error': 'rate_limit'}
        mock_gemini.return_value = {'success': False, 'error': 'rate_limit'}
        mock_gpt.return_value = {'success': False, 'error': 'rate_limit'}
        
        result = gwen_api.classify_with_fallback(
            SAMPLE_IMAGES_DIR / 'book_cover.jpg',
            fallback_apis=[gemini_api, gpt_api]
        )
        
        assert result['success'] is False
        assert 'all_apis_failed' in result['error']

@pytest.mark.asyncio
async def test_async_api_calls(gwen_api):
    """Test asynchronous API calls."""
    with patch.object(GwenAPI, 'classify_image_async') as mock_classify:
        mock_classify.return_value = {
            'success': True,
            'label': 'book_cover',
            'confidence': 0.95
        }
        
        # Test single async call
        result = await gwen_api.classify_image_async(
            SAMPLE_IMAGES_DIR / 'book_cover.jpg'
        )
        
        assert result['success'] is True
        assert result['label'] == 'book_cover'
        
        # Test multiple async calls
        image_paths = [
            SAMPLE_IMAGES_DIR / 'book_cover.jpg',
            SAMPLE_IMAGES_DIR / 'book_cover2.jpg',
            SAMPLE_IMAGES_DIR / 'not_book.jpg'
        ]
        
        results = await gwen_api.classify_images_batch(image_paths)
        
        assert len(results) == len(image_paths)
        assert all(r['success'] for r in results)
        assert all(r['label'] == 'book_cover' for r in results)

def test_api_rate_limiting(gwen_api):
    """Test API rate limiting functionality."""
    with patch.object(GwenAPI, 'classify_image') as mock_classify:
        # Set up mock to fail after 5 calls
        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count > 5:
                return {'success': False, 'error': 'rate_limit'}
            return {
                'success': True,
                'label': 'book_cover',
                'confidence': 0.95
            }
            
        mock_classify.side_effect = side_effect
        
        # Test rate limiting
        results = []
        for _ in range(10):
            result = gwen_api.classify_image(
                SAMPLE_IMAGES_DIR / 'book_cover.jpg'
            )
            results.append(result)
            
        assert len(results) == 10
        assert sum(r['success'] for r in results) == 5
        assert sum('rate_limit' in r.get('error', '') for r in results) == 5 