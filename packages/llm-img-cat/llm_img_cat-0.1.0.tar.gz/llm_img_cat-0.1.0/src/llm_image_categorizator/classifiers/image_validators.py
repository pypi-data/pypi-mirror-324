"""Image validation utilities."""
import logging
from pathlib import Path
from PIL import Image
import imagehash
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

def validate_image_path(image_path: Path) -> bool:
    """
    Validate if the image path is valid and the file is a supported image.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        bool: True if the image is valid, False otherwise
        
    Raises:
        ValueError: If the image path is invalid or file format is not supported
    """
    if not image_path.exists():
        raise ValueError(f"Image file not found: {image_path}")
        
    if not image_path.is_file():
        raise ValueError(f"Path is not a file: {image_path}")
        
    # Check file extension
    if image_path.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
        raise ValueError(f"Unsupported image format: {image_path.suffix}")
        
    # Try to open the image to verify it's valid
    try:
        with Image.open(image_path) as img:
            # Check format
            if img.format not in ['JPEG', 'PNG']:
                raise ValueError(f"Invalid image format: {img.format}")
            
            # Try to load the image data
            img.load()
            
        return True
        
    except Exception as e:
        raise ValueError(f"Failed to validate image {image_path}: {str(e)}")

class BookCoverValidator:
    """Validator for book cover images."""
    
    def __init__(self, min_size: Tuple[int, int] = (100, 100),
                 max_size: Tuple[int, int] = (4096, 4096),
                 min_ratio: float = 0.5,
                 max_ratio: float = 2.0):
        self.min_size = min_size
        self.max_size = max_size
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio
        self._hash_cache = {}
    
    async def validate(self, image_path: Path) -> bool:
        """Validate if the image is a valid book cover."""
        try:
            # Check if file exists and is readable
            if not image_path.exists():
                logger.error(f"Image file not found: {image_path}")
                return False
            
            # Try to open and validate the image
            with Image.open(image_path) as img:
                # Check format
                if img.format not in ['JPEG', 'PNG']:
                    logger.error(f"Invalid image format: {img.format}")
                    return False
                
                # Check dimensions
                width, height = img.size
                if not (self.min_size[0] <= width <= self.max_size[0] and
                        self.min_size[1] <= height <= self.max_size[1]):
                    logger.error(f"Invalid image dimensions: {width}x{height}")
                    return False
                
                # Check aspect ratio
                ratio = width / height
                if not (self.min_ratio <= ratio <= self.max_ratio):
                    logger.error(f"Invalid aspect ratio: {ratio:.2f}")
                    return False
                
                # Check if image is not empty or corrupted
                try:
                    img.load()
                except Exception as e:
                    logger.error(f"Failed to load image: {e}")
                    return False
                
                # Check for duplicate (if we have seen this image before)
                img_hash = str(imagehash.average_hash(img))
                if img_hash in self._hash_cache:
                    logger.warning(f"Duplicate image detected: {image_path} matches {self._hash_cache[img_hash]}")
                    return False
                
                # Cache the hash
                self._hash_cache[img_hash] = image_path
                
                return True
                
        except Exception as e:
            logger.error(f"Validation failed for {image_path}: {e}")
            return False
    
    def clear_cache(self):
        """Clear the hash cache."""
        self._hash_cache.clear() 