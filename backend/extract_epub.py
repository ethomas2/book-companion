#!/usr/bin/env python3
"""
EPUB Text Extractor
Extracts text from EPUB files and saves each chapter as a separate text file.
"""

import os
import re
import sys
from pathlib import Path
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import argparse


def clean_text(text):
    """Clean and normalize extracted text."""
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove common HTML artifacts
    text = re.sub(r'\[.*?\]', '', text)  # Remove bracketed content
    text = re.sub(r'^\s*[0-9]+\s*$', '', text, flags=re.MULTILINE)  # Remove standalone numbers
    
    return text


def extract_chapter_text(html_content):
    """Extract clean text from HTML content."""
    if not html_content:
        return ""
    
    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html5lib')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get text content
    text = soup.get_text()
    
    return clean_text(text)


def extract_chapter_title(text_content):
    """Extract chapter title from content."""
    lines = text_content.split('\n')
    for line in lines:
        line = line.strip()
        if line and len(line) > 5 and len(line) < 200:
            # Look for chapter-like titles
            if any(keyword in line.lower() for keyword in ['chapter', 'part', 'prologue', 'epilogue', 'prelude']):
                return line
            # Look for all-caps lines that might be titles
            if line.isupper() and len(line.split()) <= 10:
                return line
            # Look for lines with numbers that might be chapter numbers
            if re.match(r'^[0-9]+\.?\s+', line):
                return line
    return ""


def is_actual_chapter(text_content, item_id=""):
    """Determine if this content is actually a story chapter."""
    if not text_content or len(text_content.strip()) < 100:
        return False
    
    # Filter out common non-chapter content
    text_lower = text_content.lower()
    
    # Skip acknowledgments, copyright, contents, etc.
    skip_patterns = [
        'acknowledgments', 'acknowledgements',
        'copyright', 'all rights reserved',
        'contents', 'table of contents',
        'dedication', 'for emily',
        'tor books by brandon sanderson',
        'map of', 'created by his majesty',
        'ars arcanum', 'endnote'
    ]
    
    for pattern in skip_patterns:
        if pattern in text_lower:
            return False
    
    # Skip very short content (likely metadata)
    if len(text_content.strip()) < 300:
        return False
    
    # Skip content that's mostly all caps (likely headers) unless it's a title
    upper_ratio = sum(1 for c in text_content if c.isupper()) / len(text_content)
    if upper_ratio > 0.8 and len(text_content.strip()) < 1000:
        return False
    
    # Look for story-like content indicators
    story_indicators = [
        '"',  # Dialogue quotes
        'said', 'asked', 'replied',
        'he', 'she', 'they',
        'walked', 'ran', 'looked',
        'chapter', 'part', 'prologue', 'epilogue', 'prelude'
    ]
    
    has_story_content = any(indicator in text_lower for indicator in story_indicators)
    
    return has_story_content


def get_chapter_filename(chapter_title, chapter_count):
    """Generate appropriate filename for chapter."""
    if not chapter_title:
        return f"chapter_{chapter_count:03d}.txt"
    
    # Clean the title for filename
    clean_title = re.sub(r'[^\w\s-]', '', chapter_title)
    clean_title = re.sub(r'\s+', '_', clean_title.strip())
    clean_title = clean_title.lower()
    
    # Limit length
    if len(clean_title) > 50:
        clean_title = clean_title[:50]
    
    return f"{clean_title}_{chapter_count:03d}.txt"


def extract_epub(epub_path, output_dir="extracted_chapters"):
    """Extract chapters from EPUB file."""
    try:
        # Open EPUB file
        book = epub.read_epub(epub_path)
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print(f"Extracting chapters from: {epub_path}")
        print(f"Output directory: {output_path.absolute()}")
        
        chapter_count = 0
        extracted_chapters = []
        
        # Process each document in the EPUB
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # Extract text content
                html_content = item.get_content().decode('utf-8')
                text_content = extract_chapter_text(html_content)
                
                # Check if this is actually a story chapter
                if is_actual_chapter(text_content, item.get_id()):
                    chapter_count += 1
                    
                    # Extract chapter title
                    chapter_title = extract_chapter_title(text_content)
                    
                    # Generate chapter filename
                    chapter_filename = get_chapter_filename(chapter_title, chapter_count)
                    chapter_path = output_path / chapter_filename
                    
                    # Save chapter to file
                    with open(chapter_path, 'w', encoding='utf-8') as f:
                        f.write(text_content)
                    
                    # Store chapter info
                    extracted_chapters.append({
                        'filename': chapter_filename,
                        'title': chapter_title,
                        'length': len(text_content),
                        'preview': text_content[:200] + "..." if len(text_content) > 200 else text_content
                    })
                    
                    print(f"  Chapter {chapter_count}: {chapter_filename}")
                    if chapter_title:
                        print(f"    Title: {chapter_title}")
                    print(f"    Length: {len(text_content)} characters")
                    print(f"    Preview: {text_content[:100]}...")
                    print()
        
        # Create summary file
        summary_path = output_path / "extraction_summary.txt"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(f"EPUB Extraction Summary\n")
            f.write(f"======================\n")
            f.write(f"Source file: {epub_path}\n")
            f.write(f"Total chapters extracted: {chapter_count}\n")
            f.write(f"Output directory: {output_path.absolute()}\n\n")
            
            for i, chapter in enumerate(extracted_chapters, 1):
                f.write(f"Chapter {i}:\n")
                f.write(f"  Filename: {chapter['filename']}\n")
                if chapter['title']:
                    f.write(f"  Title: {chapter['title']}\n")
                f.write(f"  Length: {chapter['length']} characters\n")
                f.write(f"  Preview: {chapter['preview']}\n\n")
        
        print(f"\nExtraction complete! {chapter_count} chapters extracted.")
        print(f"Summary saved to: {summary_path}")
        
        return True
        
    except Exception as e:
        print(f"Error extracting EPUB: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Extract text from EPUB files')
    parser.add_argument('epub_path', help='Path to the EPUB file')
    parser.add_argument('-o', '--output', default='extracted_chapters', 
                       help='Output directory for extracted chapters (default: extracted_chapters)')
    
    args = parser.parse_args()
    
    # Check if EPUB file exists
    if not os.path.exists(args.epub_path):
        print(f"Error: EPUB file not found: {args.epub_path}")
        sys.exit(1)
    
    # Extract EPUB
    success = extract_epub(args.epub_path, args.output)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main() 