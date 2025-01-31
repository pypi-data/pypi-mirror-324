# Test Data Documentation

## Overview
This document describes the test data requirements and organization for the LLM Image Categorization package.

## Directory Structure
```
tests/data/images/
├── book_covers/
│   ├── manual/          # Manually curated book covers
│   ├── english/         # English language book covers
│   ├── russian/         # Russian language book covers
│   ├── japanese/        # Japanese language book covers
│   ├── chinese/         # Chinese language book covers
│   ├── other/           # Miscellaneous book covers
│   ├── example_book.jpg
│   ├── hardcover_book.jpg
│   ├── paperback_book.jpg
│   └── scifi_book.jpg
├── non_books/          # Non-book images for negative testing
│   ├── landscape.jpg
│   ├── portrait.jpg
│   └── document.jpg
└── invalid/           # Invalid/corrupted files for error testing
    ├── corrupted.jpg
    ├── truncated.jpg
    ├── empty.jpg
    ├── text.jpg
    ├── zero_byte.jpg
    ├── image.gif
    └── oversized.jpg
```

## Test Image Requirements

### Book Covers

#### Core Test Files
1. **Example Book** (`example_book.jpg`)
   - Clear, high-quality book cover
   - Title and author visible
   - Standard dimensions (around 1000x1500px)
   - Format: JPG

2. **Hardcover Book** (`hardcover_book.jpg`)
   - Traditional hardcover design
   - Dust jacket visible
   - Professional publishing quality
   - Format: JPG

3. **Paperback Book** (`paperback_book.jpg`)
   - Standard paperback format
   - Clear cover design
   - Text readable
   - Format: JPG

4. **Sci-fi Book** (`scifi_book.jpg`)
   - Science fiction genre
   - Distinctive sci-fi elements
   - Vintage or modern style
   - Format: JPG

#### Language-Specific Collections
1. **English Books**
   - Various genres and styles
   - Mix of classic and modern covers
   - Different publishers

2. **Russian Books**
   - Cyrillic text
   - Russian publishing styles
   - Different historical periods

3. **Japanese Books**
   - Manga and light novels
   - Japanese text layout
   - Unique design elements

4. **Chinese Books**
   - Chinese characters
   - Traditional and simplified text
   - Regional design styles

5. **Other/Miscellaneous**
   - Mixed languages
   - Experimental designs
   - Special editions

### Non-Book Images

#### Landscape Images
1. **Mountain Landscape** (`landscape_mountain.jpg`)
   - Natural mountain scenery
   - Wide aspect ratio
   - High contrast and detail

2. **Sea Landscape** (`landscape_sea.jpg`)
   - Ocean/water scene
   - Natural lighting
   - Horizontal composition

3. **Forest Landscape** (`landscape_forest.jpg`)
   - Natural forest scene
   - Rich in texture
   - Different from book cover layouts

#### Portrait Images
1. **Professional Portrait** (`portrait_professional.jpg`)
   - Business/formal setting
   - High quality headshot
   - Vertical orientation

2. **Casual Portrait** (`portrait_casual.jpg`)
   - Natural/candid style
   - Different lighting conditions
   - Personal photography

3. **Side Portrait** (`portrait_side.jpg`)
   - Profile view
   - Artistic composition
   - Different from book cover portraits

#### Document Images
1. **Contract Document** (`document_contract.jpg`)
   - Business document
   - Text-heavy layout
   - Official formatting

2. **Handwritten Notes** (`document_notes.jpg`)
   - Personal notes
   - Mixed text and diagrams
   - Informal layout

3. **Document Table** (`document_table.jpg`)
   - Structured data
   - Grid layout
   - Different from book formats

#### Additional Test Images
1. **Product Photo** (`product_photo.jpg`)
   - Commercial product
   - Studio lighting
   - Marketing style

2. **Magazine Cover** (`magazine_cover.jpg`)
   - Similar to book covers
   - Different layout style
   - Multiple elements

3. **Newspaper** (`newspaper.jpg`)
   - News layout
   - Multiple columns
   - Dense text content

### Invalid Files

#### Corrupted JPEG Files
1. **Corrupted JPEG** (`corrupted.jpg`)
   - Invalid JPEG data structure
   - Contains random data with JPEG markers
   - Should trigger format validation error

2. **Truncated JPEG** (`truncated.jpg`)
   - Valid JPEG header
   - Incomplete/truncated data
   - Should trigger data integrity error

#### Empty/Invalid Files
1. **Empty File** (`empty.jpg`)
   - Zero-byte file
   - Just file extension
   - Should trigger validation error

2. **Text as JPG** (`text.jpg`)
   - Text file with .jpg extension
   - Contains plain text data
   - Should trigger format error

3. **Zero Byte** (`zero_byte.jpg`)
   - Empty file created with write mode
   - Different from touch-created empty file
   - Should trigger validation error

#### Unsupported Formats
1. **GIF Image** (`image.gif`)
   - Valid GIF file
   - Unsupported format
   - Should trigger format error

2. **BMP Image** (`image.bmp`)
   - Valid BMP file
   - Unsupported format
   - Should trigger format error

3. **TIFF Image** (`image.tiff`)
   - Valid TIFF file
   - Unsupported format
   - Should trigger format error

#### Dimension Issues
1. **Oversized Image** (`oversized.jpg`)
   - Extremely large dimensions (10000x10000)
   - Valid JPEG format
   - Should trigger size limit error

2. **Zero Width** (`zero_width.jpg`)
   - Zero width, positive height
   - Should fail to create
   - Tests dimension validation

3. **Zero Height** (`zero_height.jpg`)
   - Zero height, positive width
   - Should fail to create
   - Tests dimension validation

## Image Sources
For testing purposes, we use:
1. Public domain book covers from Project Gutenberg
2. Creative Commons licensed images
3. Generated test images for specific cases
4. Custom created invalid files

## Usage Guidelines
1. All test images must be:
   - Free for testing/distribution
   - Properly attributed if required
   - Consistent size/quality
   - Representative of real use cases

2. Test data should be:
   - Version controlled
   - Easily reproducible
   - Well documented
   - Minimal in size

## Maintenance
1. Regular validation of:
   - Image integrity
   - File permissions
   - Directory structure
   - Format compliance

2. Update process:
   - Document changes
   - Verify licenses
   - Test compatibility
   - Update documentation 