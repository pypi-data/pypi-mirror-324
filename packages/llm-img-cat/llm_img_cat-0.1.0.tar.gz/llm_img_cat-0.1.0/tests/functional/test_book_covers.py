"""Functional tests for book cover detection."""
import asyncio
import pytest
from pathlib import Path

from llm_image_categorizator import llm_img_cat

# Test data paths
TEST_DATA = Path("tests/data/images")
BOOK_COVERS = TEST_DATA / "book_covers"
NON_BOOKS = TEST_DATA / "non_books"

@pytest.mark.asyncio
async def test_basic_book_cover():
    """Test basic book cover detection."""
    image_path = BOOK_COVERS / "example_book.jpg"
    result = await llm_img_cat(image_path, "book cover")
    
    assert result["is_match"] == True
    assert result["confidence"] > 0.8
    assert len(result["reasoning"]) > 0
    assert result["processing_time"] < 5.0

@pytest.mark.asyncio
async def test_different_book_styles():
    """Test detection of different book cover styles."""
    test_cases = [
        ("hardcover_book.jpg", "hardcover book"),
        ("paperback_book.jpg", "paperback book"),
        ("scifi_book.jpg", "science fiction book")
    ]
    
    for filename, category in test_cases:
        image_path = BOOK_COVERS / filename
        if not image_path.exists():
            continue
            
        result = await llm_img_cat(image_path, category)
        assert result["is_match"] == True
        assert result["confidence"] > 0.7
        assert category.lower() in result["reasoning"].lower()

@pytest.mark.asyncio
async def test_language_specific_covers():
    """Test book cover detection in different languages."""
    language_dirs = {
        "english": "english book cover",
        "russian": "russian book cover",
        "japanese": "japanese book cover",
        "chinese": "chinese book cover"
    }
    
    for lang_dir, category in language_dirs.items():
        dir_path = BOOK_COVERS / lang_dir
        if not dir_path.exists() or not any(dir_path.iterdir()):
            continue
            
        # Test first image in each language directory
        test_image = next(dir_path.glob("*.jpg"))
        result = await llm_img_cat(test_image, category)
        
        assert result["is_match"] == True
        assert result["confidence"] > 0.7
        assert lang_dir in result["reasoning"].lower() or lang_dir.title() in result["reasoning"]

@pytest.mark.asyncio
async def test_non_book_images():
    """Test that non-book images are correctly identified."""
    test_cases = [
        ("landscape_mountain.jpg", "mountain landscape"),
        ("landscape_sea.jpg", "seascape"),
        ("landscape_forest.jpg", "forest"),
        ("portrait_professional.jpg", "portrait"),
        ("document_contract.jpg", "document"),
        ("magazine_cover.jpg", "magazine cover")
    ]
    
    for filename, actual_category in test_cases:
        image_path = NON_BOOKS / filename
        if not image_path.exists():
            continue
            
        result = await llm_img_cat(image_path, "book cover")
        assert result["is_match"] == False
        assert result["confidence"] < 0.5
        # The reasoning should mention it's not a book cover
        assert "not" in result["reasoning"].lower() and "book" in result["reasoning"].lower()

@pytest.mark.asyncio
async def test_specific_book_categories():
    """Test detection with specific book categories."""
    test_cases = [
        (BOOK_COVERS / "scifi_book.jpg", "science fiction book cover"),
        (BOOK_COVERS / "hardcover_book.jpg", "hardcover book with dust jacket"),
        (BOOK_COVERS / "paperback_book.jpg", "paperback novel")
    ]
    
    for image_path, category in test_cases:
        if not image_path.exists():
            continue
            
        result = await llm_img_cat(image_path, category)
        assert result["is_match"] == True
        assert result["confidence"] > 0.7
        # Reasoning should mention specific category elements
        assert any(word in result["reasoning"].lower() for word in category.lower().split())

@pytest.mark.asyncio
async def test_ambiguous_cases():
    """Test handling of ambiguous cases."""
    test_cases = [
        (NON_BOOKS / "magazine_cover.jpg", "book or magazine cover"),
        (BOOK_COVERS / "other", "book cover"),  # Mixed/experimental designs
    ]
    
    for image_path, category in test_cases:
        if isinstance(image_path, Path) and not image_path.exists():
            continue
        if isinstance(image_path, str) and not Path(image_path).exists():
            continue
            
        result = await llm_img_cat(image_path, category)
        # We care more about the reasoning than the binary result
        assert len(result["reasoning"]) > 50  # Should provide detailed explanation
        assert result["confidence"] != 1.0  # Shouldn't be completely certain

@pytest.mark.asyncio
async def test_performance():
    """Test performance requirements."""
    # Test with different types of book covers
    test_images = [
        BOOK_COVERS / "example_book.jpg",
        BOOK_COVERS / "english" / next(iter((BOOK_COVERS / "english").glob("*.jpg")), "example.jpg"),
        BOOK_COVERS / "japanese" / next(iter((BOOK_COVERS / "japanese").glob("*.jpg")), "example.jpg")
    ]
    
    times = []
    for image_path in test_images:
        if not image_path.exists():
            continue
            
        result = await llm_img_cat(image_path, "book cover")
        times.append(result["processing_time"])
    
    if times:  # Only if we have valid results
        avg_time = sum(times) / len(times)
        assert avg_time < 5.0, f"Average processing time {avg_time:.2f}s exceeds 5s limit"
        # Check time consistency
        time_variance = max(times) - min(times)
        assert time_variance < 2.0, f"Processing time variance {time_variance:.2f}s too high"

if __name__ == "__main__":
    asyncio.run(pytest.main([__file__])) 