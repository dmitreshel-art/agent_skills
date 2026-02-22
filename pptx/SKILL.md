---
name: pptx
description: Presentation creation, editing, and analysis. When GLM needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes, or any other presentation tasks.
license: Proprietary (based on Anthropic's pptx skill)
---

# PPTX Presentation Creation and Editing

This skill provides comprehensive PowerPoint presentation manipulation using Python libraries.

## Skills Path

**Skill Location**: `{workspace}/skills/pptx`

## Overview

PowerPoint presentations (.pptx) are essential for business communication. This skill guides creation, editing, and analysis of presentation files.

## Quick Reference

| Task | Library | Method |
|------|-----------|---------|
| Create presentation | `python-pptx` | `Presentation()` |
| Add slide | `python-pptx` | `add_slide()` |
| Add content | `python-pptx` | `shapes.add_textbox()` |
| Modify existing | `python-pptx` | `Presentation()` load |
| Extract content | `python-pptx` | Iterate through slides |

## Creating Presentations

### Basic Presentation Creation

```python
from pptx import Presentation

prs = Presentation()
title_slide = prs.slides.add_slide(prs.slide_layouts[0])

# Add title and subtitle
title = title_slide.shapes.title
title.text = "My Presentation"
subtitle = title_slide.placeholders[1]
subtitle.text = "Subtitle Here"

prs.save('presentation.pptx')
```

### Adding Multiple Slides

```python
from pptx import Presentation

prs = Presentation()

# Add 5 slides
for i in range(5):
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    text_box = slide.shapes.add_textbox(100, 100, 500, 100)
    text_box.text = f"Slide {i+1}"

prs.save('multi_slide.pptx')
```

### Working with Layouts

```python
from pptx import Presentation

prs = Presentation()

# Use different layouts
# Layout 0: Title slide
slide1 = prs.slides.add_slide(prs.slide_layouts[0])

# Layout 1: Title and Content
slide2 = prs.slides.add_slide(prs.slide_layouts[1])

# Layout 2: Section Header
slide3 = prs.slides.add_slide(prs.slide_layouts[2])

prs.save('layouts.pptx')
```

## Adding Content

### Text Boxes

```python
from pptx import Presentation
from pptx.util import Pt

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[1])

# Add text box
text_box = slide.shapes.add_textbox(100, 100, 600, 200)
text_frame = text_box.text_frame
text_frame.text = "Main Heading"

# Change font size
text_frame.paragraphs[0].font.size = Pt(32)
text_frame.paragraphs[0].font.bold = True

prs.save('with_text.pptx')
```

### Lists and Bullet Points

```python
from pptx import Presentation

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[1])

text_box = slide.shapes.add_textbox(100, 100, 600, 400)
text_frame = text_box.text_frame

# Add bullet points
text_frame.text = "First bullet"
p = text_frame.add_paragraph()
p.text = "Second bullet"
p.level = 1
p = text_frame.add_paragraph()
p.text = "Third bullet"
p.level = 2

prs.save('with_bullets.pptx')
```

### Images

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[1])

# Add image
img_path = 'image.png'
slide.shapes.add_picture(img_path, Inches(1), Inches(1), width=Inches(4))

prs.save('with_image.pptx')
```

### Tables

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[1])

# Add table
shape = slide.shapes.add_table(3, 4, Inches(1), Inches(1))
table = shape.table

# Fill table
for row in range(3):
    for col in range(4):
        cell = table.cell(row, col)
        cell.text = f"Row {row}, Col {col}"

prs.save('with_table.pptx')
```

## Modifying Presentations

### Reading Existing Presentations

```python
from pptx import Presentation

prs = Presentation('existing.pptx')

# Iterate through slides
for slide in prs.slides:
    for shape in slide.shapes:
        if hasattr(shape, "text"):
            print(shape.text)

# Add new slide
new_slide = prs.slides.add_slide(prs.slide_layouts[1])
new_slide.shapes.title.text = "New Slide"

prs.save('modified.pptx')
```

### Editing Slide Content

```python
from pptx import Presentation

prs = Presentation('existing.pptx')

# Get first slide
slide = prs.slides[0]

# Edit title
if slide.shapes.title:
    slide.shapes.title.text = "Updated Title"

# Edit text boxes
for shape in slide.shapes:
    if hasattr(shape, "text_frame"):
        if "old text" in shape.text:
            shape.text_frame.text = "new text"

prs.save('edited.pptx')
```

### Deleting Slides

```python
from pptx import Presentation

prs = Presentation('existing.pptx')

# Delete slide 2 (index 1)
if len(prs.slides) > 1:
    rId = prs.slides._sldIdLst[1]
    prs.part.drop_rel(rId)
    del prs.slides._sldIdLst[1]

prs.save('slide_deleted.pptx')
```

## Formatting and Styling

### Slide Backgrounds

```python
from pptx import Presentation
from pptx.util import RGBColor

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[1])

# Set background color
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = RGBColor(0x42, 0x24, 0xE9)

prs.save('colored_background.pptx')
```

### Text Formatting

```python
from pptx import Presentation
from pptx.util import Pt, RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[1])

text_box = slide.shapes.add_textbox(100, 100, 600, 200)
text_frame = text_box.text_frame
text_frame.text = "Styled Text"

# Font properties
p = text_frame.paragraphs[0]
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
p.alignment = PP_ALIGN.CENTER

prs.save('styled_text.pptx')
```

### Slide Masters and Themes

```python
from pptx import Presentation
from pptx.util import RGBColor

prs = Presentation()

# Access slide master
slide_master = prs.slide_master

# Set master background
slide_master.background.fill.solid()
slide_master.background.fill.fore_color.rgb = RGBColor(0x00, 0x50, 0x99)

prs.save('themed.pptx')
```

## Advanced Features

### Speaker Notes

```python
from pptx import Presentation

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[1])

# Add speaker notes
notes_slide = prs.slides.notes_slide(slide)
notes_text_frame = notes_slide.notes_text_frame
notes_text_frame.text = "These are speaker notes for this slide."

prs.save('with_notes.pptx')
```

### Comments

```python
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[1])

# Add comment (as a shape with specific formatting)
comment = slide.shapes.add_shape(
    MSO_SHAPE_TYPE.COMMENT,
    Inches(5),
    Inches(1)
)
comment.text = "This is a comment"

prs.save('with_comment.pptx')
```

### Slide Transitions

```python
from pptx import Presentation
from pptx.enum.slide import PP_SLIDE

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[1])

# Add transition
slide.slide_show_transition.entry_effect = PP_SLIDE.FADE
slide.slide_show_transition.speed = 2  # Fast

prs.save('with_transitions.pptx')
```

## Templates

### Professional Template

```python
from pptx import Presentation
from pptx.util import Pt
from pptx.enum.text import PP_ALIGN

prs = Presentation()

# Title slide
title_slide = prs.slides.add_slide(prs.slide_layouts[0])
title_slide.shapes.title.text = "Professional Presentation"
subtitle = title_slide.placeholders[1]
subtitle.text = "Your Subtitle Here"

# Content slide
content_slide = prs.slides.add_slide(prs.slide_layouts[1])
content_text = content_slide.shapes.add_textbox(100, 100, 600, 400)
tf = content_text.text_frame
tf.text = "Key Points"
p1 = tf.add_paragraph()
p1.text = "• First point"
p2 = tf.add_paragraph()
p2.text = "• Second point"
p3 = tf.add_paragraph()
p3.text = "• Third point"

prs.save('professional.pptx')
```

### Data Presentation Template

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()

# Data slide
slide = prs.slides.add_slide(prs.slide_layouts[1])

# Title
title = slide.shapes.title
title.text = "Data Analysis"

# Table
table = slide.shapes.add_table(4, 3, Inches(1), Inches(2))
data = [
    ['Metric', 'Value', 'Change'],
    ['Revenue', '$1.2M', '+15%'],
    ['Users', '500K', '+25%'],
    ['Churn', '2.1%', '-0.5%']
]

for i, row_data in enumerate(data):
    for j, cell_data in enumerate(row_data):
        table.cell(i, j).text = cell_data

prs.save('data_presentation.pptx')
```

## Best Practices

### DO
- Use `python-pptx` for reliable presentation creation
- Always test presentations in PowerPoint
- Use consistent formatting across slides
- Include speaker notes for important slides
- Use appropriate slide layouts
- Optimize images for file size

### DON'T
- Don't create presentations without testing
- Don't use too many animations
- Don't ignore slide masters
- Don't hardcode positions without testing
- Don't create slides with too much content

## Dependencies

- `python-pptx>=0.6.21`
- `Pillow>=9.0.0` (for images)

## Troubleshooting

### Common Issues

**Issue**: Images not displaying
**Solution**: Check image paths and dimensions, use `Inches` for sizing

**Issue**: Text overflow
**Solution**: Adjust text box size or font size, use word wrap

**Issue**: Layout misalignment
**Solution**: Use slide layouts instead of absolute positioning

**Issue**: File size too large
**Solution**: Compress images, remove unused elements
