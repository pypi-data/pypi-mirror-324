# LLM Book Cover Detector

A Python package for detecting and analyzing book covers using Qwen Vision-Language model.

## Features

- Accurate book cover detection
- Similarity scoring (0-100%)
- Concise reasoning
- Beautiful CLI interface
- JSON response format
- Raw API response display
- Rich output formatting

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd llm_image_categorizator
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.template .env
# Edit .env with your DASHSCOPE_API_KEY
```

## Usage

### CLI Usage

The simplest way to use the book cover detector is through the CLI:

```bash
python scripts/llm_img_cat_cli.py path/to/image.jpg
```

This will:
1. Analyze if the image is a book cover
2. Provide a similarity score (0-100%)
3. Give a concise 5-word reasoning
4. Show raw API response

### Python API Usage

```python
from llm_img_cat.categorizer import llm_img_cat

# Analyze an image
result = llm_img_cat("path/to/image.jpg")

print(f"Is book cover: {result['is_category']}")
print(f"Similarity score: {result['confidence']}%")
print(f"Reasoning: {result['reasoning']}")
```

## Example Output

```
╭── Book Cover Detection Results ───╮
│ Is Book Cover    │ Yes           │
│ Similarity Score │ 90%           │
╰────────────────────────────────╯
╭── Reasoning ──────────────────────╮
│ Text and design typical of books  │
╰────────────────────────────────╯
```

## Configuration

Required environment variables in `.env`:
- `DASHSCOPE_API_KEY`: Your Qwen API key
- `DEFAULT_MODEL`: Default is "qwen2.5-vl-3b-instruct"

## Development

- Run tests: `./run_qwen_tests.sh`
- Check code: `scripts/lint.sh`
- Build docs: `scripts/build_docs.sh`

## License

MIT License

## Contributing

See CONTRIBUTING.md for guidelines. 