"""Unit tests for testing utilities."""
import os
import json
import pytest
from pathlib import Path
from PIL import Image

from llm_image_categorizator.utils.testing import (
    create_test_image,
    create_test_json,
    assert_image_valid,
    assert_json_valid,
    create_mock_api_response,
    MockResponse
)

def test_create_test_image(tmp_path):
    """Test creating test images."""
    # Test default parameters
    path = tmp_path / 'test.png'
    img_path = create_test_image(path)
    
    assert img_path.exists()
    img = Image.open(img_path)
    assert img.size == (100, 100)
    assert img.mode == 'RGB'
    
    # Test custom parameters
    path = tmp_path / 'custom.png'
    size = (200, 300)
    mode = 'RGBA'
    color = (255, 0, 0, 255)
    
    img_path = create_test_image(path, size=size, mode=mode, color=color)
    
    assert img_path.exists()
    img = Image.open(img_path)
    assert img.size == size
    assert img.mode == mode
    assert img.getpixel((0, 0)) == color
    
    # Test creating in non-existent directory
    path = tmp_path / 'subdir' / 'test.png'
    img_path = create_test_image(path)
    assert img_path.exists()

def test_create_test_json(tmp_path):
    """Test creating test JSON files."""
    # Test with default data
    path = tmp_path / 'test.json'
    json_path = create_test_json(path)
    
    assert json_path.exists()
    with open(json_path) as f:
        data = json.load(f)
        
    assert isinstance(data, dict)
    assert 'id' in data
    assert 'name' in data
    assert 'value' in data
    assert 'enabled' in data
    
    # Test with custom data
    path = tmp_path / 'custom.json'
    custom_data = {
        'test': True,
        'numbers': [1, 2, 3],
        'nested': {'key': 'value'}
    }
    
    json_path = create_test_json(path, data=custom_data)
    
    assert json_path.exists()
    with open(json_path) as f:
        data = json.load(f)
        
    assert data == custom_data
    
    # Test creating in non-existent directory
    path = tmp_path / 'subdir' / 'test.json'
    json_path = create_test_json(path)
    assert json_path.exists()

def test_assert_image_valid(tmp_path):
    """Test image validation assertions."""
    # Create test image
    path = tmp_path / 'test.png'
    create_test_image(path, size=(100, 100), mode='RGB')
    
    # Test valid cases
    assert_image_valid(path)  # Default parameters
    assert_image_valid(path, min_size=(50, 50))
    assert_image_valid(path, max_size=(200, 200))
    assert_image_valid(path, required_mode='RGB')
    
    # Test invalid cases
    with pytest.raises(AssertionError):
        assert_image_valid(path, min_size=(200, 200))
        
    with pytest.raises(AssertionError):
        assert_image_valid(path, max_size=(50, 50))
        
    with pytest.raises(AssertionError):
        assert_image_valid(path, required_mode='RGBA')
        
    # Test non-existent file
    with pytest.raises(AssertionError):
        assert_image_valid(tmp_path / 'nonexistent.png')

def test_assert_json_valid(tmp_path):
    """Test JSON validation assertions."""
    # Create test JSON
    path = tmp_path / 'test.json'
    data = {
        'name': 'test',
        'value': 42,
        'nested': {'key': 'value'}
    }
    create_test_json(path, data=data)
    
    # Test valid cases
    assert_json_valid(path)  # No required fields
    assert_json_valid(path, required_fields=['name'])
    assert_json_valid(path, required_fields=['name', 'value'])
    
    # Test missing required field
    with pytest.raises(AssertionError):
        assert_json_valid(path, required_fields=['missing_field'])
        
    # Test invalid JSON
    invalid_path = tmp_path / 'invalid.json'
    with open(invalid_path, 'w') as f:
        f.write('invalid json content')
        
    with pytest.raises(AssertionError):
        assert_json_valid(invalid_path)
        
    # Test non-existent file
    with pytest.raises(AssertionError):
        assert_json_valid(tmp_path / 'nonexistent.json')

def test_mock_response():
    """Test mock response object."""
    # Test successful response
    response = MockResponse(
        status_code=200,
        json_data={'status': 'ok'},
        text='success',
        headers={'Content-Type': 'application/json'}
    )
    
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}
    assert response.text == 'success'
    assert response.headers['Content-Type'] == 'application/json'
    
    # Test error response
    response = MockResponse(status_code=404)
    with pytest.raises(Exception):
        response.raise_for_status()

def test_create_mock_api_response():
    """Test creating mock API responses."""
    # Test successful response
    response = create_mock_api_response(success=True)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert 'id' in data['data']
    assert 'timestamp' in data['data']
    
    # Test custom data
    custom_data = {'custom': 'data'}
    response = create_mock_api_response(success=True, data=custom_data)
    assert response.json() == custom_data
    
    # Test error response
    response = create_mock_api_response(success=False)
    assert response.status_code in [400, 401, 403, 404, 500]
    data = response.json()
    assert data['status'] == 'error'
    assert 'code' in data['error']
    assert 'message' in data['error'] 