"""Example script to visualize image categorization results."""
import os
import json
import asyncio
import random
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image
from dotenv import load_dotenv

from llm_image_categorizator.classifiers import create_classifier
from llm_image_categorizator.utils.testing import create_test_image

# Load environment variables
load_dotenv()

def get_sample_images(count: int = 3) -> list[Path]:
    """Get random sample images from the test data."""
    # Use existing book cover images
    book_covers_dir = Path("tests/data/images/book_covers/manual")
    if not book_covers_dir.exists():
        raise RuntimeError(f"Book covers directory not found: {book_covers_dir}")
    
    # Get all image files
    image_files = []
    for ext in ['.jpg', '.jpeg', '.png']:
        image_files.extend(book_covers_dir.glob(f"*{ext}"))
    
    if not image_files:
        raise RuntimeError(f"No images found in {book_covers_dir}")
    
    # Select random images
    return random.sample(image_files, min(count, len(image_files)))

def create_result_visualization(
    img_path: Path,
    result: 'CategoryResult',
    ax_img,
    ax_text
) -> None:
    """Create visualization for a single image and its results."""
    # Display image
    img = Image.open(img_path)
    ax_img.imshow(img)
    ax_img.set_title(f'Input Image: {img_path.name}')
    ax_img.axis('off')
    
    # Format result text
    is_book_cover = result.confidence > 0.8
    result_text = (
        f"BOOK COVER: {'✓ YES' if is_book_cover else '✗ NO'}\n"
        f"{'=' * 30}\n"
        f"Category: {result.category}\n"
        f"Confidence: {result.confidence:.2%}\n"
        f"Model Used: {result.model_used}\n"
        f"Processing Time: {result.processing_time:.2f}s\n\n"
        f"Raw JSON Output:\n{json.dumps(result.__dict__, indent=2)}"
    )
    
    # Add result text with colored background based on result
    bg_color = 'palegreen' if is_book_cover else 'lightcoral'
    ax_text.text(
        0.05, 0.95,
        result_text,
        transform=ax_text.transAxes,
        fontsize=9,
        verticalalignment='top',
        family='monospace',
        bbox=dict(
            boxstyle='round',
            facecolor=bg_color,
            alpha=0.3,
            pad=1
        )
    )
    ax_text.axis('off')

async def visualize_categorization():
    """Create and categorize test images, then visualize results."""
    # Get sample images
    test_images = get_sample_images(3)
    
    # Initialize classifier
    classifier = create_classifier()
    
    # Set up the plot
    fig = plt.figure(figsize=(20, 7))
    fig.suptitle('Book Cover Image Categorization Results', fontsize=16, y=0.98)
    
    # Create grid for images and results
    gs = fig.add_gridspec(2, len(test_images), height_ratios=[1.5, 1])
    
    # Process each image
    for i, img_path in enumerate(test_images):
        # Create subplots for this image
        ax_img = fig.add_subplot(gs[0, i])
        ax_text = fig.add_subplot(gs[1, i])
        
        # Run categorization
        result = await classifier.classify(img_path)
        
        # Create visualization
        create_result_visualization(img_path, result, ax_img, ax_text)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('categorization_results.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    asyncio.run(visualize_categorization()) 