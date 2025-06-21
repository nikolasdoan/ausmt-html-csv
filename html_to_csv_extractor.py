#!/usr/bin/env python3
"""
HTML to CSV Article Extractor
Extracts article information from journal HTML files and creates a CSV summary
"""

import csv
import re
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd

# Configuration: Set the folder containing HTML files
HTML_FOLDER = "html_files"  # Change this to your folder name


def clean_text(text):
    """Clean and normalize text content."""
    if not text:
        return ""
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    
    return text.strip()


def parse_issue_info(issue_text):
    """Parse issue string into volume, number, and year components."""
    # Pattern to match "Vol X, No Y (YYYY)" format
    pattern = r'Vol\s+(\d+),\s+No\s+(\d+)\s+\((\d{4})\)'
    match = re.search(pattern, issue_text)
    
    if match:
        vol = int(match.group(1))
        no = int(match.group(2))
        year = int(match.group(3))
        return vol, no, year
    else:
        # Fallback parsing if format is different
        print(f"Warning: Could not parse issue format: {issue_text}")
        return None, None, None


def extract_issue_name(soup):
    """Extract the issue name from the HTML."""
    # Try to find in h2 tag first
    h2_tag = soup.find('h2')
    if h2_tag:
        issue_name = clean_text(h2_tag.get_text())
        if issue_name and "Vol" in issue_name:
            return issue_name
    
    # Fallback: try to find in title tag
    title_tag = soup.find('title')
    if title_tag:
        title_text = clean_text(title_tag.get_text())
        if "Vol" in title_text:
            return title_text
    
    # Last resort: try breadcrumb
    breadcrumb = soup.find('div', {'id': 'breadcrumb'})
    if breadcrumb:
        current_link = breadcrumb.find('a', class_='current')
        if current_link:
            return clean_text(current_link.get_text())
    
    return "Unknown Issue"


def extract_articles(soup):
    """Extract all articles from the HTML."""
    articles = []
    
    # Find all article tables
    article_tables = soup.find_all('table', class_='tocArticle')
    
    for table in article_tables:
        try:
            # Extract article title
            title_cell = table.find('td', class_='tocTitle')
            if not title_cell:
                continue
                
            # Get title text, removing any links but keeping the text
            title_link = title_cell.find('a')
            if title_link:
                title = clean_text(title_link.get_text())
            else:
                title = clean_text(title_cell.get_text())
            
            # Skip if title is empty or too short
            if not title or len(title) < 5:
                continue
            
            # Extract authors
            authors_cell = table.find('td', class_='tocAuthors')
            authors = ""
            if authors_cell:
                authors = clean_text(authors_cell.get_text())
            
            # Extract pages
            pages_cell = table.find('td', class_='tocPages')
            pages = ""
            if pages_cell:
                pages = clean_text(pages_cell.get_text())
            
            # Add to articles list
            articles.append({
                'title': title,
                'authors': authors,
                'pages': pages
            })
            
        except Exception as e:
            print(f"  Warning: Error extracting article from table: {e}")
            continue
    
    return articles


def process_html_file(html_file_path):
    """Process a single HTML file and extract article data."""
    try:
        # Read HTML file
        with open(html_file_path, 'r', encoding='utf-8', errors='ignore') as file:
            html_content = file.read()
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract issue name
        issue_name = extract_issue_name(soup)
        
        # Parse issue info into components
        vol, no, year = parse_issue_info(issue_name)
        
        # Extract articles
        articles = extract_articles(soup)
        
        # Prepare results
        results = []
        for article in articles:
            results.append({
                'Vol': vol,
                'No': no,
                'Year': year,
                'Article': article['title'],
                'Author': article['authors'],
                'Pages': article['pages']
            })
        
        return results, len(articles)
        
    except Exception as e:
        print(f"✗ Error processing {html_file_path}: {str(e)}")
        return [], 0


def apply_year_grouping(df):
    """Apply year grouping - only show year in first occurrence of each year."""
    if 'Year' not in df.columns:
        return df
    
    # Create a copy to avoid modifying original
    df_grouped = df.copy()
    
    # Sort by Year, Vol, No to ensure proper grouping
    df_grouped = df_grouped.sort_values(['Year', 'Vol', 'No'], na_position='last')
    
    # Keep track of previous year
    prev_year = None
    
    # Apply grouping logic
    for idx in df_grouped.index:
        current_year = df_grouped.loc[idx, 'Year']
        
        # If this year is the same as previous, blank it out
        if current_year == prev_year:
            df_grouped.loc[idx, 'Year'] = ''
        else:
            # Update previous year for next iteration
            prev_year = current_year
    
    return df_grouped


def find_html_folder():
    """Find the folder containing HTML files."""
    current_dir = Path('.')
    
    # First try the configured folder name
    html_folder = current_dir / HTML_FOLDER
    if html_folder.exists() and html_folder.is_dir():
        # Check if it contains HTML files
        html_files = list(html_folder.glob('*.htm')) + list(html_folder.glob('*.html'))
        if html_files:
            return html_folder
    
    # If configured folder doesn't exist or is empty, look for other folders with HTML files
    print(f"Configured folder '{HTML_FOLDER}' not found or empty.")
    print("Searching for folders containing HTML files...")
    
    for folder in current_dir.iterdir():
        if folder.is_dir() and not folder.name.startswith('.'):
            html_files = list(folder.glob('*.htm')) + list(folder.glob('*.html'))
            if html_files:
                print(f"Found HTML files in folder: {folder.name}")
                return folder
    
    # Last resort: check current directory
    html_files = list(current_dir.glob('*.htm')) + list(current_dir.glob('*.html'))
    if html_files:
        print("Using HTML files from current directory")
        return current_dir
    
    return None


def main():
    """Main function to extract data from all HTML files and create CSV."""
    # Find the folder containing HTML files
    html_folder = find_html_folder()
    
    if html_folder is None:
        print("No HTML files found in any directory.")
        print(f"Please check that:")
        print(f"1. The folder '{HTML_FOLDER}' exists and contains HTML files, or")
        print(f"2. Update the HTML_FOLDER variable at the top of this script, or")
        print(f"3. HTML files are in the current directory")
        return
    
    # Find all HTML files in the folder
    html_files = list(html_folder.glob('*.htm')) + list(html_folder.glob('*.html'))
    
    if not html_files:
        print(f"No HTML files found in {html_folder}")
        return
    
    print(f"Found {len(html_files)} HTML files in folder: {html_folder}")
    print("-" * 60)
    
    # Process all files
    all_articles = []
    total_articles = 0
    successful_files = 0
    
    for html_file in sorted(html_files):
        print(f"Processing: {html_file.name}")
        results, article_count = process_html_file(html_file)
        
        if results:
            all_articles.extend(results)
            total_articles += article_count
            successful_files += 1
            print(f"  ✓ Extracted {article_count} articles")
        else:
            print(f"  ✗ No articles found")
    
    print("-" * 60)
    print(f"Processing complete!")
    print(f"Files processed: {successful_files}/{len(html_files)}")
    print(f"Total articles extracted: {total_articles}")
    
    if not all_articles:
        print("No articles extracted. Please check the HTML file structure.")
        return
    
    # Create DataFrame
    df = pd.DataFrame(all_articles)
    
    # Apply year grouping
    df_grouped = apply_year_grouping(df)
    
    # Save to CSV
    csv_filename = 'journal_articles_summary.csv'
    df_grouped.to_csv(csv_filename, index=False, encoding='utf-8')
    print(f"CSV file created: {csv_filename}")
    
    # Save to Excel (optional)
    try:
        excel_filename = 'journal_articles_summary.xlsx'
        df_grouped.to_excel(excel_filename, index=False, engine='openpyxl')
        print(f"Excel file created: {excel_filename}")
    except ImportError:
        print("Excel file not created (openpyxl not available)")
    
    # Display sample data
    print("\n" + "="*80)
    print("SAMPLE DATA (first 15 rows):")
    print("="*80)
    print(df_grouped.head(15).to_string(index=False, max_colwidth=50))
    
    # Display summary statistics
    print(f"\n" + "="*60)
    print("SUMMARY STATISTICS:")
    print("="*60)
    print(f"Total articles: {len(df_grouped)}")
    
    # Count unique issues (excluding blanked years)
    df_original = pd.DataFrame(all_articles)
    unique_years = df_original['Year'].nunique()
    unique_issues = df_original.groupby(['Vol', 'No', 'Year']).size().shape[0]
    
    print(f"Unique years: {unique_years}")
    print(f"Unique issues: {unique_issues}")
    
    print(f"\nArticles by year:")
    year_counts = df_original['Year'].value_counts().sort_index()
    for year, count in year_counts.items():
        print(f"  {year}: {count} articles")


if __name__ == "__main__":
    # Check if required libraries are available
    try:
        from bs4 import BeautifulSoup
        import pandas as pd
    except ImportError as e:
        print("Required libraries not found. Please install them using:")
        print("pip install beautifulsoup4 pandas openpyxl")
        exit(1)
    
    print("HTML to CSV Article Extractor")
    print("=" * 40)
    print(f"Looking for HTML files in folder: {HTML_FOLDER}")
    print(f"To change this, edit the HTML_FOLDER variable at the top of this script")
    print("")
    
    main() 