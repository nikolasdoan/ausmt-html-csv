#!/usr/bin/env python3
"""
PDF Title Matcher - Improved Version
Extracts titles from PDF files and matches them with articles in the Excel file
"""

import os
import re
from pathlib import Path
import pandas as pd
from PyPDF2 import PdfReader
from fuzzywuzzy import fuzz, process
import warnings
warnings.filterwarnings("ignore")

# Configuration
EXCEL_FILE = "journal_articles_summary.xlsx"  # Input Excel file
PDF_FOLDER = "Published"  # Folder containing PDF files
OUTPUT_DIR = "output-files"  # Output directory


def extract_pdf_title(pdf_path, max_pages=2):
    """Extract title from a PDF file by reading the first few pages."""
    try:
        reader = PdfReader(pdf_path)
        
        # Extract text from first few pages
        text = ""
        pages_to_read = min(max_pages, len(reader.pages))
        
        for page_num in range(pages_to_read):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            text += page_text + "\n"
        
        # Clean and process the text
        text = text.strip()
        if not text:
            return None
            
        # Try different methods to extract title
        title = extract_title_from_text(text)
        return title
        
    except Exception as e:
        return None


def extract_title_from_text(text):
    """Extract the most likely title from PDF text with improved multi-line handling."""
    lines = text.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    
    if not lines:
        return None
    
    # Find potential title start (after common headers)
    title_start_idx = 0
    for i, line in enumerate(lines[:15]):
        line_lower = line.lower()
        # Skip header information
        if any(x in line_lower for x in ['www.ausmt.org', 'copyright', 'journal of automation', 'vol.', 'no.']):
            continue
        # Look for section indicators that come before title
        if any(x in line_lower for x in ['editorial', 'original article', 'trend', 'review', 'research']):
            title_start_idx = i + 1
            break
        # If we find a substantial line early, it might be the title
        if len(line) > 20 and i < 10:
            title_start_idx = i
            break
    
    # Extract title from the identified starting point
    if title_start_idx < len(lines):
        title_lines = []
        
        # Collect consecutive lines that look like title parts
        for i in range(title_start_idx, min(title_start_idx + 5, len(lines))):
            line = lines[i]
            cleaned_line = clean_title_line(line)
            
            if not cleaned_line:
                continue
                
            # Stop collecting if we hit obvious non-title content
            line_lower = cleaned_line.lower()
            if any(x in line_lower for x in ['abstract', 'introduction', 'keywords', 'received:', 'doi:']):
                break
            
            # Stop if line looks like author info (often all caps or has email/affiliations)
            if (len(cleaned_line) < 50 and 
                (cleaned_line.isupper() or '@' in cleaned_line or 'university' in line_lower)):
                break
            
            title_lines.append(cleaned_line)
            
            # If this line ends with punctuation, it might be complete
            if cleaned_line.endswith(('.', '?', '!')):
                break
        
        if title_lines:
            # Combine title lines
            full_title = ' '.join(title_lines)
            full_title = clean_full_title(full_title)
            
            if len(full_title) > 10 and len(full_title) < 300:
                return full_title
    
    # Fallback: look for the longest meaningful line
    meaningful_lines = []
    for line in lines[:20]:
        cleaned = clean_title_line(line)
        if len(cleaned) > 15 and len(cleaned) < 200:
            meaningful_lines.append(cleaned)
    
    if meaningful_lines:
        longest = max(meaningful_lines, key=len)
        return clean_full_title(longest)
    
    return None


def clean_title_line(line):
    """Clean a single line that might be part of a title."""
    if not line:
        return ""
    
    # Remove common PDF artifacts
    line = re.sub(r'^\d+\s*', '', line)  # Remove leading numbers
    line = re.sub(r'\s*\d+$', '', line)  # Remove trailing numbers
    
    # Remove extra whitespace
    line = re.sub(r'\s+', ' ', line).strip()
    
    # Skip obviously non-title lines
    line_lower = line.lower()
    if any(x in line_lower for x in ['www.', 'copyright', 'journal', 'vol.', 'no.', 'page']):
        return ""
    
    return line


def clean_full_title(title):
    """Final cleaning of the assembled title."""
    if not title:
        return ""
    
    # Remove extra whitespace
    title = re.sub(r'\s+', ' ', title).strip()
    
    # Remove common prefixes/suffixes
    title = re.sub(r'^(the|an|a)\s+', '', title, flags=re.IGNORECASE)
    
    # Remove trailing punctuation that looks like artifacts
    title = re.sub(r'\s*[,;]\s*$', '', title)
    
    return title.strip()


def process_all_pdfs(pdf_folder):
    """Extract titles from all PDFs in the folder."""
    pdf_folder = Path(pdf_folder)
    pdf_titles = {}
    
    pdf_files = list(pdf_folder.glob('*.pdf'))
    total_files = len(pdf_files)
    
    print(f"Processing {total_files} PDF files...")
    
    for i, pdf_file in enumerate(pdf_files, 1):
        if i % 20 == 0 or i == total_files:
            print(f"  Progress: {i}/{total_files} ({i/total_files*100:.1f}%)")
        
        title = extract_pdf_title(pdf_file)
        if title:
            pdf_titles[pdf_file.name] = title
        
        # Show first few extractions for debugging
        if i <= 5:
            print(f"    {pdf_file.name}: {title}")
    
    print(f"Successfully extracted titles from {len(pdf_titles)} PDFs")
    return pdf_titles


def match_titles_fuzzy(pdf_titles, excel_articles, threshold=60):
    """Match PDF titles with Excel articles using fuzzy matching with lower threshold."""
    matches = {}
    unmatched_pdfs = []
    unmatched_articles = []
    
    excel_titles = excel_articles['Article'].tolist()
    pdf_title_list = list(pdf_titles.values())
    pdf_filename_list = list(pdf_titles.keys())
    
    print(f"\nMatching {len(pdf_titles)} PDF titles with {len(excel_titles)} Excel articles...")
    print(f"Using fuzzy matching threshold: {threshold}%")
    
    # For each Excel article, find the best PDF match
    for idx, excel_title in enumerate(excel_titles):
        if pd.isna(excel_title):
            continue
            
        # Try multiple fuzzy matching algorithms
        matches_found = []
        
        # Method 1: token_sort_ratio (ignores word order)
        match1 = process.extractOne(excel_title, pdf_title_list, scorer=fuzz.token_sort_ratio)
        if match1: matches_found.append(('token_sort', match1[0], match1[1]))
        
        # Method 2: partial_ratio (allows partial matches)
        match2 = process.extractOne(excel_title, pdf_title_list, scorer=fuzz.partial_ratio)
        if match2: matches_found.append(('partial', match2[0], match2[1]))
        
        # Method 3: token_set_ratio (handles different word sets)
        match3 = process.extractOne(excel_title, pdf_title_list, scorer=fuzz.token_set_ratio)
        if match3: matches_found.append(('token_set', match3[0], match3[1]))
        
        # Take the best match
        if matches_found:
            best_match = max(matches_found, key=lambda x: x[2])
            method, matched_pdf_title, confidence = best_match
            
            if confidence >= threshold:
                # Find the corresponding filename
                pdf_idx = pdf_title_list.index(matched_pdf_title)
                pdf_filename = pdf_filename_list[pdf_idx]
                
                matches[idx] = {
                    'filename': pdf_filename,
                    'pdf_title': matched_pdf_title,
                    'confidence': confidence,
                    'method': method
                }
                
                # Show first few matches for debugging
                if len(matches) <= 5:
                    print(f"    Match {len(matches)}: {excel_title[:50]}... -> {pdf_filename} ({confidence}%)")
            else:
                unmatched_articles.append((idx, excel_title))
        else:
            unmatched_articles.append((idx, excel_title))
    
    print(f"Matched {len(matches)} articles with PDFs")
    print(f"Unmatched articles: {len(unmatched_articles)}")
    
    # Find unmatched PDFs
    matched_filenames = {match['filename'] for match in matches.values()}
    unmatched_pdfs = [filename for filename in pdf_titles.keys() 
                     if filename not in matched_filenames]
    print(f"Unmatched PDFs: {len(unmatched_pdfs)}")
    
    return matches, unmatched_articles, unmatched_pdfs


def update_excel_file(excel_file, matches):
    """Update the Excel file with the File Name column."""
    # Load the Excel file
    df = pd.read_excel(excel_file)
    
    # Add File Name column
    df['File Name'] = ''
    df['Match Confidence'] = ''
    
    # Fill in the matches
    for idx, match_info in matches.items():
        df.loc[idx, 'File Name'] = match_info['filename']
        df.loc[idx, 'Match Confidence'] = f"{match_info['confidence']}%"
    
    # Create output directory
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)
    
    # Save updated Excel file
    filename = Path(excel_file).stem + '_with_filenames.xlsx'
    output_file = output_dir / filename
    df.to_excel(output_file, index=False)
    
    print(f"Updated Excel file saved as: {output_file}")
    return output_file, df


def main():
    """Main function to process PDFs and update Excel file."""
    print("PDF Title Matcher - Improved Version")
    print("=" * 50)
    
    # Check if folders/files exist
    if not os.path.exists(PDF_FOLDER):
        print(f"Error: PDF folder '{PDF_FOLDER}' not found")
        return
    
    if not os.path.exists(EXCEL_FILE):
        print(f"Error: Excel file '{EXCEL_FILE}' not found")
        return
    
    # Step 1: Extract titles from all PDFs
    print("Step 1: Extracting titles from PDF files...")
    pdf_titles = process_all_pdfs(PDF_FOLDER)
    
    if not pdf_titles:
        print("No titles extracted from PDFs. Exiting.")
        return
    
    # Step 2: Load Excel data
    print("\nStep 2: Loading Excel data...")
    df = pd.read_excel(EXCEL_FILE)
    print(f"Loaded {len(df)} articles from Excel file")
    
    # Step 3: Perform fuzzy matching
    print("\nStep 3: Performing fuzzy matching...")
    matches, unmatched_articles, unmatched_pdfs = match_titles_fuzzy(pdf_titles, df)
    
    # Step 4: Update Excel file
    print("\nStep 4: Updating Excel file...")
    output_file, updated_df = update_excel_file(EXCEL_FILE, matches)
    
    # Step 5: Show results summary
    print("\n" + "=" * 50)
    print("MATCHING RESULTS SUMMARY:")
    print("=" * 50)
    print(f"Total PDF files: {len(pdf_titles)}")
    print(f"Total Excel articles: {len(df)}")
    print(f"Successful matches: {len(matches)}")
    print(f"Match rate: {len(matches)/len(df)*100:.1f}%")
    
    # Show some example matches
    if matches:
        print(f"\nSample successful matches:")
        for i, (idx, match_info) in enumerate(list(matches.items())[:5]):
            excel_title = df.loc[idx, 'Article'][:60] + "..." if len(df.loc[idx, 'Article']) > 60 else df.loc[idx, 'Article']
            pdf_title = match_info['pdf_title'][:60] + "..." if len(match_info['pdf_title']) > 60 else match_info['pdf_title']
            print(f"  {i+1}. {match_info['filename']} ({match_info['confidence']}%)")
            print(f"     Excel: {excel_title}")
            print(f"     PDF:   {pdf_title}")
            print()
    
    if unmatched_articles:
        print(f"\nFirst 5 unmatched articles:")
        for i, (idx, title) in enumerate(unmatched_articles[:5]):
            short_title = title[:80] + "..." if len(title) > 80 else title
            print(f"  {i+1}. {short_title}")
    
    print(f"\nOutput file created: {output_file}")
    

if __name__ == "__main__":
    main() 