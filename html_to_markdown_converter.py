#!/usr/bin/env python3
"""
HTML to Markdown Converter
Converts all HTML files in the current directory to Markdown format
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup, Comment
import html2text


def setup_html2text_converter():
    """Configure the html2text converter with appropriate settings."""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.body_width = 0  # Don't wrap lines
    h.unicode_snob = True
    h.skip_internal_links = True
    h.ignore_tables = False
    h.decode_errors = 'ignore'
    return h


def clean_html_content(soup):
    """Remove unwanted elements from HTML content."""
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Remove comments
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()
    
    # Remove navigation and sidebar elements
    for element in soup.find_all(['div'], {'id': ['sidebar', 'navbar', 'header', 'footer']}):
        element.decompose()
    
    # Remove specific classes that are likely navigation/UI
    for element in soup.find_all(['div'], class_=['block', 'roundedCorner']):
        element.decompose()
    
    return soup


def extract_main_content(soup):
    """Extract the main content area from the HTML."""
    # Try to find main content area
    main_content = soup.find('div', {'id': 'main'}) or soup.find('div', {'id': 'content'})
    
    if main_content:
        return main_content
    
    # If no main content found, try to find the body content
    body_content = soup.find('div', {'id': 'body'})
    if body_content:
        # Remove sidebar from body content
        sidebar = body_content.find('div', {'id': 'sidebar'})
        if sidebar:
            sidebar.decompose()
        return body_content
    
    # Fallback to body tag
    return soup.find('body') or soup


def post_process_markdown(markdown_text):
    """Clean up the generated markdown."""
    # Remove excessive blank lines
    markdown_text = re.sub(r'\n\s*\n\s*\n', '\n\n', markdown_text)
    
    # Clean up breadcrumb navigation (usually appears as "Home > Archives > ...")
    markdown_text = re.sub(r'^.*?Home\s*>\s*.*?\n', '', markdown_text, flags=re.MULTILINE)
    
    # Remove "You are logged in as..." type content
    markdown_text = re.sub(r'You are logged in as.*?\n.*?\n', '', markdown_text, flags=re.DOTALL)
    
    # Remove font size controls and similar UI elements
    markdown_text = re.sub(r'Make font size.*?\n', '', markdown_text)
    
    # Clean up multiple consecutive dashes
    markdown_text = re.sub(r'-{3,}', '---', markdown_text)
    
    # Remove standalone bullet points
    markdown_text = re.sub(r'^\s*\*\s*$', '', markdown_text, flags=re.MULTILINE)
    
    return markdown_text.strip()


def convert_html_to_markdown(html_file_path, output_dir):
    """Convert a single HTML file to Markdown."""
    try:
        # Read HTML file
        with open(html_file_path, 'r', encoding='utf-8', errors='ignore') as file:
            html_content = file.read()
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Clean the HTML content
        soup = clean_html_content(soup)
        
        # Extract main content
        main_content = extract_main_content(soup)
        
        # Convert to markdown
        converter = setup_html2text_converter()
        markdown_content = converter.handle(str(main_content))
        
        # Post-process the markdown
        markdown_content = post_process_markdown(markdown_content)
        
        # Generate output filename
        base_name = Path(html_file_path).stem
        output_file = output_dir / f"{base_name}.md"
        
        # Write markdown file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(f"# {base_name}\n\n")
            file.write(markdown_content)
        
        print(f"✓ Converted: {html_file_path} → {output_file}")
        return True
        
    except Exception as e:
        print(f"✗ Error converting {html_file_path}: {str(e)}")
        return False


def main():
    """Main function to convert all HTML files to Markdown."""
    # Get current directory
    current_dir = Path('.')
    
    # Create output directory
    output_dir = current_dir / 'markdown_files'
    output_dir.mkdir(exist_ok=True)
    
    # Find all HTML files
    html_files = list(current_dir.glob('*.htm')) + list(current_dir.glob('*.html'))
    
    if not html_files:
        print("No HTML files found in the current directory.")
        return
    
    print(f"Found {len(html_files)} HTML files to convert...")
    print(f"Output directory: {output_dir.absolute()}")
    print("-" * 50)
    
    # Convert each HTML file
    successful_conversions = 0
    for html_file in html_files:
        if convert_html_to_markdown(html_file, output_dir):
            successful_conversions += 1
    
    print("-" * 50)
    print(f"Conversion complete! {successful_conversions}/{len(html_files)} files converted successfully.")
    print(f"Markdown files saved in: {output_dir.absolute()}")


if __name__ == "__main__":
    # Check if required libraries are available
    try:
        import html2text
        from bs4 import BeautifulSoup
    except ImportError as e:
        print("Required libraries not found. Please install them using:")
        print("pip install beautifulsoup4 html2text")
        exit(1)
    
    main() 