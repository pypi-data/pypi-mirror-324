"""
Rich Console Demo for LLM Image Categorization
============================================

This script demonstrates the main features of the llm_img_cat package
with beautiful console output using the rich library.

Features demonstrated:
- Environment setup
- Image categorization
- Error handling
- Beautiful console output
- Test summary

Requirements:
- llm_img_cat
- rich

To run:
```bash
pip install llm_img_cat rich
python rich_demo.py
```
"""
import os
from rich.console import Console
from rich.panel import Panel
from llm_img_cat import ImageCategorizer

# Initialize rich console for beautiful output
console = Console()

def setup_environment():
    """Setup environment variables"""
    # Note: In production, load these from .env file or environment variables
    if not os.getenv('DASHSCOPE_API_KEY'):
        console.print("[yellow]Warning: DASHSCOPE_API_KEY not found in environment[/yellow]")
        console.print("[yellow]Using demo key - replace with your own for production use[/yellow]\n")
        os.environ['DASHSCOPE_API_KEY'] = 'your-api-key-here'
    
    if not os.getenv('DEFAULT_MODEL'):
        os.environ['DEFAULT_MODEL'] = 'qwen2.5-vl-3b-instruct'
    
    console.print(Panel.fit(
        "[bold green]Environment Setup[/bold green]\n"
        f"API Key: {'✓ Set' if os.getenv('DASHSCOPE_API_KEY') else '✗ Not Set'}\n"
        f"Model: {os.getenv('DEFAULT_MODEL')}"
    ))

def analyze_image(path, description):
    """Analyze a single image"""
    console.print(f"\n[bold]Analyzing image:[/bold] {description}")
    console.print(f"Path: {path}")
    
    try:
        categorizer = ImageCategorizer()
        result = categorizer.categorize_image(path)
        
        console.print(Panel.fit(
            "[bold blue]Analysis Results[/bold blue]\n"
            f"Is Book Cover: [{'green' if result['is_category'] else 'red'}]{result['is_category']}[/]\n"
            f"Confidence: {result['confidence']}%\n"
            f"Reasoning: {result['reasoning']}"
        ))
        return True
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        return False

def main():
    """Main demo function"""
    # Print header
    console.print("[bold]LLM Image Categorization Demo[/bold]\n")
    
    # Setup environment
    setup_environment()
    
    # Test images - using files from sample_images directory
    test_images = [
        {
            "path": "sample_images/book_cover.jpg",
            "description": "Book cover example"
        },
        {
            "path": "sample_images/not_book.jpg",
            "description": "Non-book cover example"
        }
    ]
    
    # Analyze each image
    success = 0
    for image in test_images:
        if analyze_image(image["path"], image["description"]):
            success += 1
    
    # Print summary
    console.print(Panel.fit(
        "[bold]Test Summary[/bold]\n"
        f"Total Tests: {len(test_images)}\n"
        f"Successful: {success}\n"
        f"Failed: {len(test_images) - success}"
    ))

if __name__ == "__main__":
    main() 