---
name: xlsx
description: Use this skill when Codex needs to read, create, modify, or format Excel files. Typical tasks include reading data, creating spreadsheets, updating cells, appending rows, applying formatting, and working with multiple sheets. Also use for recalculating formulas, data analysis, and visualization tasks involving .xlsx files.
license: Proprietary (based on Anthropic's xlsx skill)
---

# XLSX File Operations

This skill provides comprehensive Excel file manipulation using Python libraries.

## Skills Path

**Skill Location**: `{workspace}/skills/xlsx`

## Overview

Excel files (.xlsx) are the most common format for spreadsheet data. This skill guides creation, reading, modification, and analysis of Excel files.

## Quick Reference

| Task | Library | Method |
|------|-----------|---------|
| Read data | `openpyxl` | `load_workbook()` |
| Create new | `openpyxl` | `Workbook()` |
| Write data | `openpyxl` | `save()` |
| Data analysis | `pandas` | `read_excel()` / `to_excel()` |
| Formulas | `openpyxl` | `cell.formula` |

## Creating Spreadsheets

### Basic Workbook Creation

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws['A1'] = 'Hello'
ws['B1'] = 'World!'
wb.save('hello.xlsx')
```

### Adding Multiple Sheets

```python
from openpyxl import Workbook

wb = Workbook()
ws1 = wb.active
ws1.title = 'Sheet1'

ws2 = wb.create_sheet('Sheet2')
ws2['A1'] = 'This is sheet 2'

wb.save('multi_sheet.xlsx')
```

### Working with Ranges

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# Set a range of values
data = [
    ['Name', 'Age', 'City'],
    ['Alice', 25, 'New York'],
    ['Bob', 30, 'Los Angeles']
]

for row in data:
    ws.append(row)

wb.save('data.xlsx')
```

## Reading Spreadsheets

### Reading Cell Values

```python
from openpyxl import load_workbook

wb = load_workbook('data.xlsx')
ws = wb.active

print(f"Cell A1: {ws['A1'].value}")
print(f"Cell B1: {ws['B1'].value}")
```

### Iterating Through Cells

```python
from openpyxl import load_workbook

wb = load_workbook('data.xlsx')
ws = wb.active

# Iterate through rows
for row in ws.iter_rows(min_row=1, max_row=10):
    for cell in row:
        print(cell.value)
```

### Reading by Column

```python
from openpyxl import load_workbook

wb = load_workbook('data.xlsx')
ws = wb.active

# Get all values in column A
column_a = [cell.value for cell in ws['A']]

# Get range of cells
cells = ws['A1:C10']
for row in cells:
    for cell in row:
        print(cell.value)
```

## Modifying Spreadsheets

### Updating Cells

```python
from openpyxl import load_workbook

wb = load_workbook('data.xlsx')
ws = wb.active

ws['A1'] = 'New Value'
ws.cell(row=2, column=3).value = 'Updated'

wb.save('modified.xlsx')
```

### Adding Rows and Columns

```python
from openpyxl import load_workbook

wb = load_workbook('data.xlsx')
ws = wb.active

# Append new row
ws.append(['New', 'Row', 'Data'])

# Insert column
ws.insert_cols(idx=2, amount=1)

wb.save('modified.xlsx')
```

### Deleting Data

```python
from openpyxl import load_workbook

wb = load_workbook('data.xlsx')
ws = wb.active

# Delete row
ws.delete_rows(idx=2, amount=1)

# Delete column
ws.delete_cols(idx=3, amount=1)

wb.save('modified.xlsx')
```

## Formatting

### Cell Formatting

```python
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = load_workbook('data.xlsx')
ws = wb.active

# Format cell A1
cell = ws['A1']
cell.font = Font(bold=True, size=12, color='FF0000')
cell.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
cell.alignment = Alignment(horizontal='center', vertical='center')

wb.save('formatted.xlsx')
```

### Number Formatting

```python
from openpyxl import load_workbook
from openpyxl.styles import numbers

wb = load_workbook('data.xlsx')
ws = wb.active

# Format as currency
ws['A1'].number_format = numbers.FORMAT_ACCOUNTING_USD

# Format as percentage
ws['B1'].number_format = numbers.FORMAT_PERCENTAGE

# Format as date
ws['C1'].number_format = numbers.FORMAT_DATE_YYYYMMDD

wb.save('formatted.xlsx')
```

## Formulas

### Adding Formulas

```python
from openpyxl import load_workbook

wb = load_workbook('data.xlsx')
ws = wb.active

# Simple sum
ws['C1'] = '=SUM(A1:A10)'

# Average
ws['D1'] = '=AVERAGE(B1:B10)'

# IF statement
ws['E1'] = '=IF(A1>100,"High","Low")'

wb.save('with_formulas.xlsx')
```

### Recalculating Formulas

```python
from openpyxl import load_workbook

wb = load_workbook('data.xlsx', data_only=False)
ws = wb.active

# Formula is preserved
print(f"Cell A1 value: {ws['A1'].value}")
print(f"Cell A1 formula: {ws['A1'].value if not ws['A1'].data_only else 'calculated'}")

# To recalculate, open in Excel or use xlwings
```

## Data Analysis with Pandas

### Reading Excel

```python
import pandas as pd

# Read entire workbook
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
print(df.head())

# Read multiple sheets
excel_file = pd.ExcelFile('data.xlsx')
df_sheet1 = pd.read_excel(excel_file, sheet_name='Sheet1')
df_sheet2 = pd.read_excel(excel_file, sheet_name='Sheet2')
```

### Writing Excel

```python
import pandas as pd

# Create DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['NY', 'LA', 'Chicago']
})

# Write to Excel
df.to_excel('output.xlsx', index=False, sheet_name='Data')

# Write multiple sheets
with pd.ExcelWriter('multi_sheet.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Sheet1', index=False)
    df2.to_excel(writer, sheet_name='Sheet2', index=False)
```

### Data Manipulation

```python
import pandas as pd

df = pd.read_excel('data.xlsx')

# Filter data
filtered = df[df['Age'] > 25]

# Group and aggregate
grouped = df.groupby('City')['Age'].mean()

# Add calculated column
df['Age_Squared'] = df['Age'] ** 2

# Sort
sorted_df = df.sort_values('Age', ascending=False)

df.to_excel('analyzed.xlsx', index=False)
```

## Working with Charts

### Creating Charts with openpyxl

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference

wb = Workbook()
ws = wb.active

# Add data
data = [
    ['Category', 'Value'],
    ['A', 10],
    ['B', 20],
    ['C', 30]
]

for row in data:
    ws.append(row)

# Create chart
chart = BarChart()
values = Reference(ws, min_col=2, min_row=2, max_col=2, max_row=4)
cats = Reference(ws, min_col=1, min_row=2, max_row=4)
chart.add_data(values, titles_from_data=True)
chart.set_categories(cats)

ws.add_chart(chart, "E2")

wb.save('with_chart.xlsx')
```

## Advanced Operations

### Merging Multiple Files

```python
import pandas as pd

# Read all sheets
all_sheets = []
with pd.ExcelFile('file1.xlsx') as xls1:
    all_sheets.append(pd.read_excel(xls1))

with pd.ExcelFile('file2.xlsx') as xls2:
    all_sheets.append(pd.read_excel(xls2))

# Combine
combined = pd.concat(all_sheets, ignore_index=True)
combined.to_excel('merged.xlsx', index=False)
```

### Conditional Formatting

```python
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font
from openpyxl.formatting.rule import CellIsRule

wb = load_workbook('data.xlsx')
ws = wb.active

# Highlight values > 100
red_fill = PatternFill(start_color='FFFF0000', end_color='FFFF0000', fill_type='solid')
font = Font(color='FFFFFFFF', bold=True)
rule = CellIsRule(operator='greaterThan', formula=['100'], stopIfTrue=True, fill=red_fill, font=font)
ws.conditional_formatting.add('A1:C10', rule)

wb.save('conditional.xlsx')
```

### Data Validation

```python
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation

wb = load_workbook('data.xlsx')
ws = wb.active

# Dropdown list
dv = DataValidation(type="list", formula1='"Yes,No"', allow_blank=True)
dv.error = 'Your entry is not in the list'
dv.errorTitle = 'Invalid Entry'
dv.prompt = 'Please select from the dropdown'
dv.promptTitle = 'Selected Dropdown'
dv.add('A1:A10')

ws.add_data_validation(dv)

wb.save('with_validation.xlsx')
```

## Best Practices

### DO
- Use `openpyxl` for Excel-specific operations
- Use `pandas` for data analysis
- Always save with a new filename before modifications
- Test files in Excel after creation
- Handle large files with chunking
- Use appropriate data types (int, float, datetime)

### DON'T
- Don't hardcode cell references
- Don't ignore formulas when reading
- Don't process huge files without memory management
- Don't assume file extensions are always lowercase
- Don't forget to close workbooks

## Dependencies

- `openpyxl>=3.0.0`
- `pandas>=1.3.0`
- `xlwings>=0.24.0` (for formula recalculation with Excel open)

## Troubleshooting

### Common Issues

**Issue**: File won't open in Excel
**Solution**: Check file extension, ensure proper closing of workbook

**Issue**: Formulas not calculated
**Solution**: Use `data_only=False` when loading, or use xlwings

**Issue**: Memory error with large files
**Solution**: Use pandas with chunking or process rows in batches
