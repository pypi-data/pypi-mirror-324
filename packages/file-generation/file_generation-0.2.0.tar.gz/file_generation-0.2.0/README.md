# File Generation

A Python package for generating DOCX and XLSX files from templates and zipping them.

## Installation

```bash
pip install file-generation
```

## Usage

```python
from file_generation.generators import BaseDocxGenerator
from file_generation.core import MultiFileGenerationService

base_output_dir = "/path/to/output"
instance_id = 42
docx_context = {"company_name": "Example Corp", "date": "2025-01-31"}

docx_generator = BaseDocxGenerator(
    base_output_dir=base_output_dir,
    instance_id=instance_id,
    templates=["/path/to/template1.docx"],
    context=docx_context
)

service = MultiFileGenerationService(generators=[docx_generator])
zip_path = service.create_zip("output_files.zip")
print(f"ZIP created at: {zip_path}")
```
