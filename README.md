# HTML Processing Scripts for Journal Articles

This project contains Python scripts to process HTML journal table of contents files and convert them to clean Markdown and structured CSV/Excel formats.

## Scripts Overview

### 1. `html_to_markdown_converter.py` - HTML to Markdown Conversion
### 2. `html_to_csv_extractor.py` - HTML to Structured Data Extraction

## What Was Accomplished

✅ **Successfully processed 33 HTML files** (journal volumes from 2011-2020)  
✅ **Converted to clean Markdown format** with preserved structure  
✅ **Extracted structured data to CSV/Excel** with 267 individual articles  
✅ **Implemented intelligent folder detection** for organized file management  
✅ **Added year grouping functionality** for better data presentation  

## Files Created

- `html_to_markdown_converter.py` - Converts HTML to clean Markdown
- `html_to_csv_extractor.py` - Extracts structured data to CSV/Excel
- `requirements.txt` - Python dependencies
- `markdown_files/` - Directory containing converted .md files
- `journal_articles_summary.csv` - Structured article data in CSV format
- `journal_articles_summary.xlsx` - Structured article data in Excel format
- `README.md` - This documentation file

## CSV/Excel Data Structure

The extracted data uses the following column structure with intelligent grouping:

| Vol | No | Year | Article | Author | Pages |
|-----|----|----- |---------|--------|-------|
| 1   | 1  | 2011 | EDITORIAL: First HOOT from International Journal... | Chih-Kung Lee | 1-2 |
| 1   | 1  |      | The Application Trend of Smart Sensing Technology... | Meng-Hsien Hsieh | 3-5 |
| 1   | 2  |      | The Global Trend of Energy Saving... | Chih-Lun Chen | 1-3 |
| 2   | 1  | 2012 | SPECIAL ISSUE: Bio-Inspired Sensing... | Yao-Joe Joseph Yang | 1-2 |

### Column Descriptions:
- **Vol**: Volume number (1, 2, 3, etc.)
- **No**: Issue number (1, 2, 3, 4)  
- **Year**: Publication year (shown only on first occurrence per year)
- **Article**: Complete article title
- **Author**: Author names (comma-separated for multiple authors)
- **Pages**: Page range (e.g., "1-3", "21-34")

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

## Key Features

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

## Processing Statistics

### Data Summary:
- **Input**: 33 HTML files (journal table of contents pages)
- **Output**: 267 individual articles extracted
- **Success Rate**: 100% (33/33 files processed successfully)
- **Years Covered**: 2011-2020 (10 years)
- **Content Preserved**: Article titles, authors, page numbers, download links

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

### Processing Workflow:
1. **Folder Detection**: Locate HTML files in specified or detected folders
2. **HTML Parsing**: Extract content using BeautifulSoup
3. **Data Extraction**: Parse issue info and article details
4. **Data Cleaning**: Remove unwanted elements and normalize text
5. **Structure Processing**: Split issue information into Vol/No/Year columns
6. **Year Grouping**: Apply grouping logic for clean presentation
7. **Export**: Save to both CSV and Excel formats with UTF-8 encoding

## File Organization

```
project/
├── html_to_csv_extractor.py      # Main CSV extraction script
├── html_to_markdown_converter.py  # Markdown conversion script
├── requirements.txt               # Python dependencies
├── README.md                     # This documentation
├── journal_articles_summary.csv  # Extracted article data (CSV)
├── journal_articles_summary.xlsx # Extracted article data (Excel)
├── markdown_files/               # Converted Markdown files
│   ├── Vol 1, No 1 (2011).md
│   ├── Vol 1, No 2 (2011).md
│   └── ...
└── html_files/                   # Original HTML files (configurable)
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

### Output Customization:
- CSV filename: Modify `csv_filename` variable
- Excel filename: Modify `excel_filename` variable
- Column order: Adjust the DataFrame column order in the processing function

## Troubleshooting

### Common Issues:
1. **No HTML files found**: Check folder path and file extensions (.htm, .html)
2. **Encoding errors**: Files are processed with UTF-8 and error handling
3. **Missing dependencies**: Run `pip install -r requirements.txt`
4. **Empty results**: Verify HTML structure matches expected format

### File Format Support:
- **Input**: .htm, .html files
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

## Results Summary

All HTML journal files have been successfully processed into clean, structured formats suitable for academic research, data analysis, and documentation purposes. The dual-output approach provides flexibility for different use cases while maintaining data integrity and readability. 