import json
import os

from docx import Document
from python_docx_symbol import (
  convert_symbols,
  ConversionResult,
)

from tests import protected_data_dir, output_dir

def test_convert():
  doc = Document(os.path.join(
    protected_data_dir, "sample.docx"
  ))
  
  result: ConversionResult = convert_symbols(doc)
  print(result.converted)
  print(result.unconverted)
  
  doc.save(os.path.join(
    output_dir, "sample.docx"
  ))
  
  assert len(result.converted) > 0  