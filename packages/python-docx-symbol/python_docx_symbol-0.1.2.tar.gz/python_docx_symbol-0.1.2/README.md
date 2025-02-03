# python-docx-symbol

Convert docx Symbol characters to unicode characters.

## Installation

`pip install python-docx-symbol`

## Example

```python
from docx import Document
from python_docx_symbol import convert_symbols

doc = Document("/path/to/input.docx")
result = convert_symbols(doc)
print(result.converted)
print(result.unconverted)

doc.save("/path/to/output.docx")
```
