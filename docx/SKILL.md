---
name: docx
description: Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of "Word doc", "word document", ".docx", or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a "report", "memo", "letter", "template", or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.
license: Proprietary (based on Anthropic's docx skill)
---

# DOCX Creation, Editing, and Analysis

This skill provides comprehensive document creation, editing, and analysis capabilities for Microsoft Word (.docx) files using the docx library for Python.

## Skills Path

**Skill Location**: `{workspace}/skills/docx`

## Overview

A .docx file is a ZIP archive containing XML files. This skill guides:
- Creating new Word documents with proper formatting
- Editing existing documents
- Reading and extracting content
- Working with tracked changes and comments
- Converting between formats

## Quick Reference

| Task | Approach |
|------|----------|
| Read/analyze content | `docx` Python library |
| Create new document | `python-docx` library |
| Edit existing document | Unpack → edit XML → repack |
| Convert to images | `pdf2image` + `PIL` |

## Creating New Documents

### Installation

```bash
pip install python-docx
```

### Basic Document Creation

```python
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

doc = Document()
doc.add_heading('Document Title', 0)
doc.add_paragraph('This is a paragraph.')
doc.save('document.docx')
```

### Adding Tables

```python
from docx import Document
from docx.shared import Inches

doc = Document()

table = doc.add_table(rows=3, cols=3)
table.style = 'Table Grid'
for i in range(3):
    for j in range(3):
        table.cell(i, j).text = f'Cell {i},{j}'

doc.save('document.docx')
```

### Adding Images

```python
from docx import Document
from docx.shared import Inches

doc = Document()
doc.add_picture('image.png', width=Inches(2.0))
doc.save('document.docx')
```

### Page Setup

```python
from docx import Document
from docx.shared import Inches

doc = Document()
section = doc.sections[0]
section.page_height = Inches(11)  # Letter
section.page_width = Inches(8.5)
doc.save('document.docx')
```

## Reading Documents

### Extract Text

```python
from docx import Document

doc = Document('document.docx')
for paragraph in doc.paragraphs:
    print(paragraph.text)
```

### Extract Tables

```python
from docx import Document

doc = Document('document.docx')
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            print(cell.text)
```

### Extract Metadata

```python
from docx import Document

doc = Document('document.docx')
print(f"Title: {doc.core_properties.title}")
print(f"Author: {doc.core_properties.author}")
```

## Editing Existing Documents

### Find and Replace Text

```python
from docx import Document

doc = Document('document.docx')
for paragraph in doc.paragraphs:
    if 'old text' in paragraph.text:
        paragraph.text = paragraph.text.replace('old text', 'new text')
doc.save('edited.docx')
```

### Add Content

```python
from docx import Document

doc = Document('document.docx')
doc.add_paragraph('New paragraph added')
doc.add_heading('New Section', level=2)
doc.save('edited.docx')
```

## Working with Styles

### Apply Styles to Paragraphs

```python
from docx import Document
from docx.shared import Pt

doc = Document()
p = doc.add_paragraph('This is a styled paragraph')
p.runs[0].font.size = Pt(14)
p.runs[0].font.bold = True
doc.save('document.docx')
```

### Custom Styles

```python
from docx import Document
from docx.shared import Pt, RGBColor

doc = Document()
styles = doc.styles
style = styles.add_style('CustomStyle', 1)
style.font.size = Pt(12)
style.font.color.rgb = RGBColor(0x42, 0x24, 0xE9)
doc.save('document.docx')
```

## Templates

### Letter Template

```python
from docx import Document
from datetime import datetime

doc = Document()

# Header
doc.add_heading('Official Letter', 0)
doc.add_paragraph(f'Date: {datetime.now().strftime("%B %d, %Y")}')

# Content
doc.add_paragraph('Dear [Name],')
doc.add_paragraph('This is the body of the letter...')
doc.add_paragraph('Sincerely,')
doc.add_paragraph('[Your Name]')

doc.save('letter.docx')
```

### Report Template

```python
from docx import Document

doc = Document()

# Title page
doc.add_heading('Annual Report', 0)
doc.add_paragraph('Prepared by: [Department]')
doc.add_paragraph('Date: [Date]')

# Executive summary
doc.add_heading('Executive Summary', level=1)
doc.add_paragraph('This report summarizes...')

# Content sections
doc.add_heading('Introduction', level=2)
doc.add_paragraph('Introduction text...')

doc.save('report.docx')
```

## Best Practices

### DO
- Use `python-docx` for reliable document creation
- Always validate document before saving
- Use proper page sizes (Letter: 8.5" x 11")
- Include metadata for better document management
- Test documents in Word after creation

### DON'T
- Don't manually edit XML unless necessary
- Don't use excessive formatting
- Don't ignore document structure
- Don't create documents without testing

## Troubleshooting

### Common Issues

**Issue**: Document won't open
**Solution**: Check XML structure, ensure proper ZIP archive

**Issue**: Images not displaying
**Solution**: Verify image paths and dimensions

**Issue**: Tables misaligned
**Solution**: Check cell merging and column widths

## Dependencies

- `python-docx>=0.8.11`
- `Pillow>=9.0.0` (for images)

## Next Steps

- See REFERENCE.md for advanced XML editing
- See FORMS.md for form filling
- See EXAMPLES.md for more templates
