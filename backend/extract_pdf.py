#!/usr/bin/env python3
"""
PDF Text Extractor
Extracts text from PDF files and saves each page as a separate text file.
"""

import os
import re
import sys
from pathlib import Path
import PyPDF2
import argparse


def clean_text(text):
    """Clean and normalize extracted text."""
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove common PDF artifacts
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    text = re.sub(r'\f', '\n', text)  # Replace form feeds with newlines
    
    return text


def extract_pdf(pdf_path, output_dir="pdf_extracted_pages"):
    """Extract pages from PDF file."""
    try:
        # Open PDF file
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Create output directory
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            
            print(f"Extracting pages from: {pdf_path}")
            print(f"Output directory: {output_path.absolute()}")
            print(f"Total pages: {len(pdf_reader.pages)}")
            
            extracted_pages = []
            
            # Process each page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                
                # Extract text content
                text_content = page.extract_text()
                
                if text_content and len(text_content.strip()) > 50:  # Filter out very short content
                    # Clean the text
                    cleaned_text = clean_text(text_content)
                    
                    if cleaned_text:
                        # Generate page filename
                        page_filename = f"page_{page_num + 1:03d}.txt"
                        page_path = output_path / page_filename
                        
                        # Save page to file
                        with open(page_path, 'w', encoding='utf-8') as f:
                            f.write(cleaned_text)
                        
                        # Store page info
                        extracted_pages.append({
                            'filename': page_filename,
                            'page_number': page_num + 1,
                            'length': len(cleaned_text),
                            'preview': cleaned_text[:200] + "..." if len(cleaned_text) > 200 else cleaned_text
                        })
                        
                        print(f"  Page {page_num + 1}: {page_filename} ({len(cleaned_text)} characters)")
                        print(f"    Preview: {cleaned_text[:100]}...")
                        print()
                else:
                    print(f"  Page {page_num + 1}: Skipped (too short or empty)")
            
            # Create summary file
            summary_path = output_path / "extraction_summary.txt"
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(f"PDF Extraction Summary\n")
                f.write(f"=====================\n")
                f.write(f"Source file: {pdf_path}\n")
                f.write(f"Total pages in PDF: {len(pdf_reader.pages)}\n")
                f.write(f"Pages extracted: {len(extracted_pages)}\n")
                f.write(f"Output directory: {output_path.absolute()}\n\n")
                
                for page_info in extracted_pages:
                    f.write(f"Page {page_info['page_number']}:\n")
                    f.write(f"  Filename: {page_info['filename']}\n")
                    f.write(f"  Length: {page_info['length']} characters\n")
                    f.write(f"  Preview: {page_info['preview']}\n\n")
            
            print(f"\nExtraction complete! {len(extracted_pages)} pages extracted.")
            print(f"Summary saved to: {summary_path}")
            
            return True
            
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Extract text from PDF files')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('-o', '--output', default='pdf_extracted_pages', 
                       help='Output directory for extracted pages (default: pdf_extracted_pages)')
    
    args = parser.parse_args()
    
    # Check if PDF file exists
    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file not found: {args.pdf_path}")
        sys.exit(1)
    
    # Extract PDF
    success = extract_pdf(args.pdf_path, args.output)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main() 