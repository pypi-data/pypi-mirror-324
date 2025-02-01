"""Test Qwen VL model for book cover classification."""
import os
import sys
import asyncio
import json
from datetime import datetime
from pathlib import Path
import logging
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich import print as rprint

from src.categorization import create_classifier

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Rich console
console = Console()

def ensure_venv():
    """Ensure we're running in the virtual environment."""
    if not hasattr(sys, 'real_prefix') and not sys.base_prefix != sys.prefix:
        console.print("[red]Error: Virtual environment is not activated![/red]")
        console.print("[yellow]Please run: source venv/bin/activate[/yellow]")
        sys.exit(1)
    console.print("[green]Virtual environment is active[/green]")

async def test_manual_books():
    """Test classification of manual book covers using Qwen VL."""
    # Ensure venv is activated
    ensure_venv()
    
    # Create results directory if not exists
    results_dir = Path("tests/manual/results")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Create classifier with Qwen VL model
    model_name = "qwen2.5-vl-3b-instruct"
    console.print(f"\n[bold green]Initializing Qwen VL classifier...[/bold green]")
    classifier = create_classifier(model_name=model_name)
    await classifier.setup()
    
    # Get all manual book images
    test_dir = Path("tests/data/manual")
    image_files = list(test_dir.glob("*.jpg"))
    
    if not image_files:
        console.print("[red]No images found in the manual books directory![/red]")
        return
    
    console.print(f"[bold green]Found {len(image_files)} images to process[/bold green]")
        
    # Create results table
    table = Table(title=f"Qwen VL Book Classification Results - {len(image_files)} Manual Books")
    table.add_column("Image", style="cyan", no_wrap=True)
    table.add_column("Valid Cover", style="blue", no_wrap=True)
    table.add_column("Category", style="green", no_wrap=True)
    table.add_column("Confidence", style="yellow", no_wrap=True)
    table.add_column("Time", style="blue", no_wrap=True)
    table.add_column("Explanation", style="magenta", no_wrap=False)
    
    results = []
    start_time = datetime.now()
    valid_covers = 0
    invalid_covers = 0
    
    # Process each image with progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Processing images...", total=len(image_files))
        
        for image_path in image_files:
            try:
                progress.update(task, description=f"[cyan]Processing {image_path.name}")
                
                # Classify image
                result = await classifier.classify(image_path)
                
                # Check if it's a valid book cover
                is_valid = result.category != "invalid_image"
                if is_valid:
                    valid_covers += 1
                else:
                    invalid_covers += 1
                
                # Store result
                result_data = {
                    "image": image_path.name,
                    "is_valid_cover": is_valid,
                    "category": result.category,
                    "confidence": f"{result.confidence:.2f}",
                    "time": f"{result.processing_time:.2f}s",
                    "explanation": result.metadata.get("explanation", "No explanation provided")
                }
                results.append(result_data)
                
                # Add to table
                table.add_row(
                    result_data["image"],
                    "[green]✓[/green]" if is_valid else "[red]✗[/red]",
                    result_data["category"],
                    result_data["confidence"],
                    result_data["time"],
                    result_data["explanation"]
                )
                
            except Exception as e:
                error_msg = f"Error processing {image_path.name}: {str(e)}"
                logger.error(error_msg)
                results.append({
                    "image": image_path.name,
                    "is_valid_cover": False,
                    "category": "ERROR",
                    "confidence": "0.0",
                    "time": "N/A",
                    "explanation": error_msg
                })
                table.add_row(
                    image_path.name,
                    "[red]✗[/red]",
                    "[red]ERROR[/red]",
                    "0.0",
                    "N/A",
                    f"[red]{str(e)}[/red]"
                )
                invalid_covers += 1
            
            progress.advance(task)
    
    total_time = (datetime.now() - start_time).total_seconds()
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = results_dir / f"qwen_vl_results_{timestamp}.json"
    with open(results_file, "w") as f:
        json.dump({
            "metadata": {
                "model": model_name,
                "total_images": len(image_files),
                "valid_covers": valid_covers,
                "invalid_covers": invalid_covers,
                "total_time": total_time,
                "average_time": total_time/len(image_files),
                "timestamp": timestamp
            },
            "results": results
        }, f, indent=2)
    
    # Print results
    console.print("\n[bold green]Classification Results:[/bold green]")
    console.print(table)
    
    # Print summary
    summary = Panel(
        f"""[bold]Classification Summary[/bold]
        Total images processed: {len(image_files)}
        Valid book covers: {valid_covers}
        Invalid book covers: {invalid_covers}
        Total processing time: {total_time:.2f} seconds
        Average time per image: {total_time/len(image_files):.2f} seconds
        Model used: {model_name} (Qwen VL)
        Results saved to: {results_file}
        """,
        title="Summary",
        border_style="blue"
    )
    console.print("\n")
    console.print(summary)

if __name__ == "__main__":
    try:
        asyncio.run(test_manual_books())
    except KeyboardInterrupt:
        console.print("\n[bold red]Test interrupted by user[/bold red]")
    except Exception as e:
        console.print(f"\n[bold red]Test failed with error: {str(e)}[/bold red]") 