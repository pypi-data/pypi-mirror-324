"""Testing utilities for creating test data and mock responses."""
import os
import json
import time
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from PIL import Image

def create_test_image(
    path: Union[str, Path],
    size: Tuple[int, int] = (100, 100),
    mode: str = 'RGB',
    color: Optional[Union[Tuple[int, ...], int]] = None
) -> Path:
    """Create a test image file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    if color is None:
        if mode == 'RGB':
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        elif mode == 'RGBA':
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
        else:
            color = random.randint(0, 255)
    
    img = Image.new(mode, size, color)
    img.save(path)
    return path

def create_test_json(
    path: Union[str, Path],
    data: Optional[Dict] = None
) -> Path:
    """Create a test JSON file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    if data is None:
        data = {
            'id': str(random.randint(1000, 9999)),
            'name': f'test_{random.randint(1, 100)}',
            'value': random.random(),
            'enabled': random.choice([True, False])
        }
    
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    
    return path

def assert_image_valid(
    path: Union[str, Path],
    min_size: Optional[Tuple[int, int]] = None,
    max_size: Optional[Tuple[int, int]] = None,
    required_mode: Optional[str] = None
) -> None:
    """Assert that an image file is valid and meets requirements."""
    path = Path(path)
    assert path.exists(), f"Image file does not exist: {path}"
    
    try:
        img = Image.open(path)
    except Exception as e:
        raise AssertionError(f"Failed to open image file: {e}")
    
    if min_size:
        assert img.size[0] >= min_size[0] and img.size[1] >= min_size[1], \
            f"Image size {img.size} is smaller than minimum size {min_size}"
    
    if max_size:
        assert img.size[0] <= max_size[0] and img.size[1] <= max_size[1], \
            f"Image size {img.size} is larger than maximum size {max_size}"
    
    if required_mode:
        assert img.mode == required_mode, \
            f"Image mode {img.mode} does not match required mode {required_mode}"

def assert_json_valid(
    path: Union[str, Path],
    required_fields: Optional[List[str]] = None
) -> None:
    """Assert that a JSON file is valid and contains required fields."""
    path = Path(path)
    assert path.exists(), f"JSON file does not exist: {path}"
    
    try:
        with open(path) as f:
            data = json.load(f)
    except Exception as e:
        raise AssertionError(f"Failed to parse JSON file: {e}")
    
    if required_fields:
        for field in required_fields:
            assert field in data, f"Required field '{field}' not found in JSON data"

class MockResponse:
    """Mock response object for testing API calls."""
    
    def __init__(
        self,
        status_code: int = 200,
        json_data: Optional[Dict] = None,
        text: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        """Initialize mock response."""
        self.status_code = status_code
        self._json_data = json_data
        self._text = text
        self.headers = headers or {}
    
    def json(self) -> Dict:
        """Get JSON response data."""
        return self._json_data
    
    @property
    def text(self) -> str:
        """Get text response."""
        return self._text or ''
    
    def raise_for_status(self):
        """Raise an exception for error status codes."""
        if self.status_code >= 400:
            raise Exception(f"HTTP Error: {self.status_code}")

def create_mock_api_response(
    success: bool = True,
    data: Optional[Dict] = None,
    status_code: Optional[int] = None
) -> MockResponse:
    """Create a mock API response."""
    if success:
        if status_code is None:
            status_code = 200
            
        if data is None:
            data = {
                'status': 'success',
                'data': {
                    'id': str(random.randint(1000, 9999)),
                    'timestamp': time.time()
                }
            }
    else:
        if status_code is None:
            status_code = random.choice([400, 401, 403, 404, 500])
            
        if data is None:
            data = {
                'status': 'error',
                'error': {
                    'code': str(status_code),
                    'message': f'Mock error response (code: {status_code})'
                }
            }
    
    return MockResponse(
        status_code=status_code,
        json_data=data,
        text=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )