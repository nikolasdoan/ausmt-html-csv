# HTML Processing Scripts for Journal Articles

This project contains Python scripts to process HTML journal table of contents files and convert them to clean Markdown and structured CSV/Excel formats, plus advanced PDF title matching capabilities.

## Scripts Overview

### 1. `html-md.py` - HTML to Markdown Conversion
### 2. `html-csv.py` - HTML to Structured Data Extraction  
### 3. `pdf_title_matcher.py` - PDF Title Extraction and Matching

## What Was Accomplished

✅ **Successfully processed 33 HTML files** (journal volumes from 2011-2020)  
✅ **Converted to clean Markdown format** with preserved structure  
✅ **Extracted structured data to CSV/Excel** with 267 individual articles  
✅ **Implemented intelligent folder detection** for organized file management  
✅ **Added year grouping functionality** for better data presentation  
✅ **Created advanced PDF title matching** to link articles with their PDF files
✅ **Implemented fuzzy matching algorithms** to handle title variations

## Files Created

- `html_to_markdown_converter.py` - Converts HTML to clean Markdown
- `html_to_csv_extractor.py` - Extracts structured data to CSV/Excel
- `pdf_title_matcher_improved.py` - Matches articles with PDF files using title extraction
- `requirements.txt` - Python dependencies
- `markdown_files/` - Directory containing converted .md files
- `journal_articles_summary.csv` - Structured article data in CSV format
- `journal_articles_summary.xlsx` - Structured article data in Excel format
- `journal_articles_summary_with_filenames.xlsx` - Excel file with PDF filename mappings
- `README.md` - This documentation file

## New Feature: PDF Title Matching

### Problem Solved
You have 273 PDF files representing individual articles, but the filenames are cryptic (like `850-1826-1-PB.pdf`) and don't indicate which article they contain. The PDF title matcher solves this by:

1. **Extracting actual titles** from the PDF content
2. **Matching titles** with your Excel article database using fuzzy matching
3. **Adding filename columns** to your Excel file for easy reference

### How It Works

#### Step 1: Intelligent PDF Title Extraction
```python
# The script reads PDF files and extracts titles using multiple methods:
- Identifies and skips headers/footers (copyright, journal info, page numbers)
- Locates section markers (EDITORIAL, ORIGINAL ARTICLE, etc.)
- Handles multi-line titles that span several lines
- Cleans artifacts and assembles complete titles
```

#### Step 2: Advanced Fuzzy Matching
```python
# Uses three different matching algorithms for best results:
- token_sort_ratio: Handles word order differences
- partial_ratio: Allows partial title matches  
- token_set_ratio: Manages different word sets
- Configurable confidence threshold (default: 60%)
```

#### Step 3: Excel Integration
- Adds "File Name" column with the PDF filename
- Adds "Match Confidence" column showing match quality percentage
- Preserves all existing data while adding new columns

### Usage Instructions

#### For PDF Title Matching:
```bash
# Ensure your PDF files are in a folder called "Published"
# Make sure journal_articles_summary.xlsx exists

python pdf_title_matcher_improved.py
```

#### Expected Input Structure:
```
project/
├── Published/                     # Folder with PDF files
│   ├── 850-1826-1-PB.pdf         # Individual article PDFs
│   ├── 107-682-1-PB.pdf
│   └── ...
├── journal_articles_summary.xlsx  # Your Excel file with articles
└── pdf_title_matcher_improved.py
```

#### Output:
- `journal_articles_summary_with_filenames.xlsx` - Updated Excel with PDF mappings

## CSV/Excel Data Structure

The extracted data uses the following column structure with intelligent grouping:

| Vol | No | Year | Article | Author | Pages | File Name | Match Confidence |
|-----|----|----- |---------|--------|-------|-----------|------------------|
| 1   | 1  | 2011 | EDITORIAL: First HOOT from International Journal... | Chih-Kung Lee | 1-2 | 105-15-1-PB.pdf | 85% |
| 1   | 1  |      | The Application Trend of Smart Sensing Technology... | Meng-Hsien Hsieh | 3-5 | 95-7-1-PB.pdf | 92% |
| 1   | 2  |      | The Global Trend of Energy Saving... | Chih-Lun Chen | 1-3 | 301-12-1-PB.pdf | 78% |
| 2   | 1  | 2012 | SPECIAL ISSUE: Bio-Inspired Sensing... | Yao-Joe Joseph Yang | 1-2 | 146-606-1-PB.pdf | 88% |

### Column Descriptions:
- **Vol**: Volume number (1, 2, 3, etc.)
- **No**: Issue number (1, 2, 3, 4)  
- **Year**: Publication year (shown only on first occurrence per year)
- **Article**: Complete article title
- **Author**: Author names (comma-separated for multiple authors)
- **Pages**: Page range (e.g., "1-3", "21-34")
- **File Name**: PDF filename containing this article
- **Match Confidence**: Fuzzy matching confidence percentage

## Setup and Usage

### Installation
```bash
# Install required dependencies
pip install -r requirements.txt
```

### For HTML to CSV/Excel Extraction

#### Option 1: Configure Folder Path
1. Edit `html_to_csv_extractor.py`
2. Change line 12: `HTML_FOLDER = "your_folder_name"`
3. Run the script:
```bash
python html_to_csv_extractor.py
```

#### Option 2: Auto-Detection
The script automatically searches for folders containing HTML files:
```bash
python html_to_csv_extractor.py
```

#### Option 3: Current Directory
Place HTML files in the same directory as the script and run.

### For HTML to Markdown Conversion
```bash
python html_to_markdown_converter.py
```

### For PDF Title Matching
```bash
# Ensure PDFs are in "Published" folder
python pdf_title_matcher_improved.py
```

## Key Features

### PDF Title Matcher Features:
- **Intelligent title extraction**: Handles multi-line titles and PDF formatting artifacts
- **Multiple fuzzy matching algorithms**: Uses 3 different methods for optimal matching
- **Configurable thresholds**: Adjustable confidence levels (default 60%)
- **Robust error handling**: Processes corrupted or unusual PDF files gracefully
- **Progress tracking**: Shows real-time processing status
- **Detailed reporting**: Provides match statistics and confidence scores
- **Excel integration**: Seamlessly adds columns to existing data

### CSV/Excel Extractor Features:
- **Smart folder detection**: Automatically finds HTML files in subfolders
- **Configurable paths**: Easy to specify custom folder locations
- **Year grouping**: Repeated years are blanked for clean presentation
- **Data validation**: Handles encoding issues and malformed HTML
- **Dual output**: Creates both CSV and Excel files
- **Comprehensive logging**: Shows processing progress and statistics

### Markdown Converter Features:
- **Content extraction**: Focuses on main content, removes navigation/UI elements
- **Structure preservation**: Maintains journal organization with proper headings
- **Clean formatting**: Converts HTML tables to Markdown tables
- **Link preservation**: Keeps PDF and HTML download links intact
- **Post-processing cleanup**: Removes excessive whitespace and UI elements

## Technical Implementation

### PDF Processing Workflow:
1. **PDF Reading**: Uses PyPDF2 to extract text from first 2 pages
2. **Content Analysis**: Identifies headers, footers, and section markers
3. **Title Detection**: Locates title start position after common headers
4. **Multi-line Assembly**: Combines title fragments across multiple lines
5. **Text Cleaning**: Removes artifacts, normalizes whitespace
6. **Fuzzy Matching**: Applies 3 algorithms with confidence scoring
7. **Result Integration**: Updates Excel file with filename mappings

### Fuzzy Matching Algorithms:
```python
# token_sort_ratio: Ignores word order
"Smart Technology Applications" ↔ "Applications of Smart Technology" = 95%

# partial_ratio: Allows substring matching  
"IoT Based Home Automation" ↔ "IoT Based Home Automation System" = 88%

# token_set_ratio: Handles different word sets
"Machine Learning Applications" ↔ "Applications in Machine Learning" = 92%
```

### Title Extraction Logic:
```python
# Example: Multi-line title reconstruction
PDF Text:
"ORIGINAL ARTICLE
 Characterization of an 2x2 SCB Optical
 Switch Integrated with VOA
 Hen-Wei Huang and Yao-Joe Yang"

Extracted Title:
"Characterization of an 2x2 SCB Optical Switch Integrated with VOA"
```

## Processing Statistics

### Data Summary:
- **Input**: 33 HTML files (journal table of contents pages)
- **Output**: 267 individual articles extracted
- **PDF Files**: 273 PDF files processed for title matching
- **Success Rate**: Variable depending on PDF quality and title variations
- **Years Covered**: 2011-2020 (10 years)
- **Content Preserved**: Article titles, authors, page numbers, download links, PDF mappings

### Articles by Year:
- 2011: 27 articles
- 2012: 42 articles  
- 2013: 37 articles
- 2014: 34 articles
- 2015: 33 articles
- 2016: 25 articles
- 2017: 24 articles
- 2018: 19 articles
- 2019: 16 articles
- 2020: 10 articles

## Technical Details

### Dependencies Used:
- **beautifulsoup4**: HTML parsing and manipulation
- **html2text**: HTML to Markdown conversion
- **pandas**: Data manipulation and CSV/Excel export
- **openpyxl**: Excel file generation
- **lxml**: Fast XML/HTML processing
- **PyPDF2**: PDF text extraction
- **fuzzywuzzy**: Fuzzy string matching
- **python-Levenshtein**: Fast string distance calculations

### Processing Workflow:
1. **Folder Detection**: Locate HTML files in specified or detected folders
2. **HTML Parsing**: Extract content using BeautifulSoup
3. **Data Extraction**: Parse issue info and article details
4. **Data Cleaning**: Remove unwanted elements and normalize text
5. **Structure Processing**: Split issue information into Vol/No/Year columns
6. **Year Grouping**: Apply grouping logic for clean presentation
7. **PDF Processing**: Extract titles from PDF files using intelligent parsing
8. **Fuzzy Matching**: Match PDF titles with Excel articles using multiple algorithms
9. **Export**: Save to both CSV and Excel formats with UTF-8 encoding

## File Organization

```
project/
├── pdf_title_matcher_improved.py     # PDF title extraction and matching
├── html_to_csv_extractor.py          # CSV extraction script
├── html_to_markdown_converter.py     # Markdown conversion script
├── requirements.txt                  # Python dependencies
├── README.md                        # This documentation
├── journal_articles_summary.csv     # Extracted article data (CSV)
├── journal_articles_summary.xlsx    # Extracted article data (Excel)
├── journal_articles_summary_with_filenames.xlsx  # Excel with PDF mappings
├── Published/                       # PDF files folder
│   ├── 850-1826-1-PB.pdf
│   ├── 107-682-1-PB.pdf
│   └── ...
├── markdown_files/                  # Converted Markdown files
│   ├── Vol 1, No 1 (2011).md
│   ├── Vol 1, No 2 (2011).md
│   └── ...
└── html_files/                      # Original HTML files (configurable)
    ├── Vol 1, No 1 (2011).htm
    ├── Vol 1, No 2 (2011).htm
    └── ...
```

## Configuration

### Customizing the HTML Folder:
Edit the `HTML_FOLDER` variable in `html_to_csv_extractor.py`:
```python
HTML_FOLDER = "your_folder_name"  # Change this to your folder name
```

### Customizing PDF Matching:
Edit configuration in `pdf_title_matcher_improved.py`:
```python
# Adjust matching threshold (60-90% recommended)
threshold = 60  # Lower = more matches, higher = more precise

# Change PDF folder name
pdf_folder = "Published"  # Your PDF folder name

# Modify pages to read for title extraction
max_pages = 2  # Number of pages to read from each PDF
```

### Output Customization:
- CSV filename: Modify `csv_filename` variable
- Excel filename: Modify `excel_filename` variable
- Column order: Adjust the DataFrame column order in the processing function

## Troubleshooting

### Common Issues:

#### PDF Matching Issues:
1. **Low match rates**: Lower the threshold in `match_titles_fuzzy()` function
2. **PDF reading errors**: Some PDFs may be corrupted or password-protected
3. **Title extraction failures**: Complex layouts may confuse the extraction logic
4. **False matches**: Increase threshold for higher precision

#### General Issues:
1. **No HTML files found**: Check folder path and file extensions (.htm, .html)
2. **Encoding errors**: Files are processed with UTF-8 and error handling
3. **Missing dependencies**: Run `pip install -r requirements.txt`
4. **Empty results**: Verify HTML structure matches expected format

### File Format Support:
- **Input**: .htm, .html, .pdf files
- **Output**: .csv, .xlsx, .md files
- **Encoding**: UTF-8 with error tolerance

## Use Cases

The processed data is now ready for:
- 📊 **Data analysis** and visualization
- 📈 **Publication trend analysis** over time
- 🔍 **Academic research** and bibliometric studies
- 📋 **Database import** and cataloging
- 📄 **Report generation** and documentation
- 🌐 **Website integration** using Markdown files
- 📚 **Digital library management** with PDF-article mapping
- 🔗 **Cross-referencing** between metadata and full-text documents

## Results Summary

All HTML journal files have been successfully processed into clean, structured formats suitable for academic research, data analysis, and documentation purposes. The dual-output approach provides flexibility for different use cases while maintaining data integrity and readability. The addition of PDF title matching creates a complete bridge between bibliographic metadata and full-text documents, enabling comprehensive digital library management and research workflows. 