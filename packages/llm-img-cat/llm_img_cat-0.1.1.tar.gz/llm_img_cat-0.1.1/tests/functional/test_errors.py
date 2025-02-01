"""Functional tests for error handling."""
import asyncio
import pytest
from pathlib import Path

from llm_image_categorizator import llm_img_cat

# Test data paths
TEST_DATA = Path("tests/data/images")
INVALID = TEST_DATA / "invalid"

@pytest.mark.asyncio
async def test_missing_file():
    """Test handling of missing image file."""
    with pytest.raises(FileNotFoundError):
        await llm_img_cat("nonexistent.jpg", "book cover")

@pytest.mark.asyncio
async def test_empty_category():
    """Test handling of empty category."""
    image_path = TEST_DATA / "book_covers/example_book.jpg"
    with pytest.raises(ValueError):
        await llm_img_cat(image_path, "")

@pytest.mark.asyncio
async def test_corrupted_jpeg_files():
    """Test handling of corrupted JPEG files."""
    # Test completely corrupted JPEG
    with pytest.raises(Exception) as exc_info:
        await llm_img_cat(INVALID / "corrupted.jpg", "book cover")
    assert "invalid" in str(exc_info.value).lower() or "corrupt" in str(exc_info.value).lower()
    
    # Test truncated JPEG
    with pytest.raises(Exception) as exc_info:
        await llm_img_cat(INVALID / "truncated.jpg", "book cover")
    assert "invalid" in str(exc_info.value).lower() or "truncated" in str(exc_info.value).lower()

@pytest.mark.asyncio
async def test_empty_files():
    """Test handling of empty and invalid files."""
    # Test empty file (created with touch)
    with pytest.raises(Exception) as exc_info:
        await llm_img_cat(INVALID / "empty.jpg", "book cover")
    assert "empty" in str(exc_info.value).lower() or "invalid" in str(exc_info.value).lower()
    
    # Test zero-byte file (created with write)
    with pytest.raises(Exception) as exc_info:
        await llm_img_cat(INVALID / "zero_byte.jpg", "book cover")
    assert "empty" in str(exc_info.value).lower() or "invalid" in str(exc_info.value).lower()
    
    # Test text file with jpg extension
    with pytest.raises(Exception) as exc_info:
        await llm_img_cat(INVALID / "text.jpg", "book cover")
    assert "invalid" in str(exc_info.value).lower() or "not an image" in str(exc_info.value).lower()

@pytest.mark.asyncio
async def test_unsupported_formats():
    """Test handling of unsupported image formats."""
    unsupported_formats = [
        ("image.gif", "GIF"),
        ("image.bmp", "BMP"),
        ("image.tiff", "TIFF")
    ]
    
    for filename, format_name in unsupported_formats:
        with pytest.raises(ValueError) as exc_info:
            await llm_img_cat(INVALID / filename, "book cover")
        assert "format" in str(exc_info.value).lower() or format_name.lower() in str(exc_info.value).lower()

@pytest.mark.asyncio
async def test_dimension_issues():
    """Test handling of images with dimension issues."""
    # Test oversized image
    with pytest.raises(Exception) as exc_info:
        await llm_img_cat(INVALID / "oversized.jpg", "book cover")
    assert "size" in str(exc_info.value).lower() or "large" in str(exc_info.value).lower()
    
    # Note: zero width/height images are not tested as they cannot be created
    # (PIL prevents creation of images with zero dimensions)

@pytest.mark.asyncio
async def test_invalid_paths():
    """Test handling of invalid file paths."""
    invalid_paths = [
        "",  # Empty path
        " ",  # Space only
        "../../etc/passwd",  # Path traversal attempt
        "http://example.com/image.jpg",  # URL instead of file path
        "/dev/null",  # Special file
        "image.jpg\0.txt",  # Null byte injection
    ]
    
    for path in invalid_paths:
        with pytest.raises(Exception) as exc_info:
            await llm_img_cat(path, "book cover")
        assert any(msg in str(exc_info.value).lower() for msg in ["path", "invalid", "file"])

@pytest.mark.asyncio
async def test_invalid_categories():
    """Test handling of invalid category descriptions."""
    image_path = TEST_DATA / "book_covers/example_book.jpg"
    invalid_categories = [
        "",  # Empty string
        " ",  # Space only
        "\n",  # Newline only
        "a" * 1000,  # Too long
        "book\0cover",  # Null byte injection
        "<script>alert('xss')</script>",  # Script injection attempt
    ]
    
    for category in invalid_categories:
        with pytest.raises(Exception) as exc_info:
            await llm_img_cat(image_path, category)
        assert any(msg in str(exc_info.value).lower() for msg in ["category", "invalid", "empty"])

if __name__ == "__main__":
    asyncio.run(pytest.main([__file__])) 