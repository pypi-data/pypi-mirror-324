"""
Test for verifying that the package can be installed via pip and used correctly.
This test should be run in an isolated environment.
"""
import sys
import subprocess
import pytest
import os


def test_package_installation():
    """Test that the package can be installed via pip."""
    # Install the package
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "llm_img_cat"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Failed to install package: {result.stderr}"

    # Verify we can import the package
    result = subprocess.run(
        [sys.executable, "-c", "import llm_img_cat; print(llm_img_cat.__version__)"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Failed to import package: {result.stderr}"
    assert result.stdout.strip(), "Version should not be empty"

def test_basic_functionality():
    """Test that basic package functionality works."""
    # Check for DASHSCOPE_API_KEY
    api_key = os.environ.get('DASHSCOPE_API_KEY')
    if not api_key:
        pytest.skip("DASHSCOPE_API_KEY environment variable not set")

    test_code = f'''
import os
os.environ['DASHSCOPE_API_KEY'] = "{api_key}"  # Set API key for the subprocess
os.environ['DEFAULT_MODEL'] = "qwen-vl-plus"  # Set default model

import llm_img_cat
from llm_img_cat import ImageCategorizer

# Initialize the categorizer
categorizer = ImageCategorizer()

# Test with a simple URL (replace with a stable test image URL)
test_url = "https://raw.githubusercontent.com/almazkun/llm_img_cat/main/tests/data/test_image.jpg"
result = categorizer.categorize_image(test_url)

# Verify we got some result
assert isinstance(result, dict), "Result should be a dictionary"
assert "is_category" in result, "Result should contain is_category"
assert "confidence" in result, "Result should contain confidence"
assert "reasoning" in result, "Result should contain reasoning"
print("Test passed successfully!")
'''
    
    result = subprocess.run(
        [sys.executable, "-c", test_code],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Functionality test failed: {result.stderr}"
    assert "Test passed successfully!" in result.stdout, "Test should complete successfully"

if __name__ == "__main__":
    pytest.main([__file__]) 