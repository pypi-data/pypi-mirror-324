# File Generation

A Python package for generating DOCX and XLSX files from templates and zipping them into a single archive. Perfect for automating document generation workflows.

---

## Features

- **DOCX Generation**: Create `.docx` files from templates using the `docxtpl` library.
- **XLSX Generation**: Generate `.xlsx` files with dynamic data and loops using `openpyxl`.
- **Zipping**: Combine multiple generated files into a single `.zip` archive.
- **Customizable**: Easily extendable for custom file types and workflows.
- **Framework-Agnostic**: Works independently of Django or other frameworks.

---

## Installation

Install the package via pip:

```bash
pip install file-generation
```
## Usage
1. Generating DOCX Files
Use the BaseDocxGenerator to generate .docx files from templates.
```
from file_generation.generators import BaseDocxGenerator
from file_generation.core import MultiFileGenerationService

# Define the output directory and instance ID
base_output_dir = "/path/to/output"
instance_id = 42

# Define the context data for the template
docx_context = {
    "company_name": "Example Corp",
    "date": "2025-01-31",
    "user": {"name": "John Doe", "email": "john.doe@example.com"}
}

# Initialize the DOCX generator
docx_generator = BaseDocxGenerator(
    base_output_dir=base_output_dir,
    instance_id=instance_id,
    templates=["/path/to/template1.docx", "/path/to/template2.docx"],
    context=docx_context
)

# Generate files and create a ZIP archive
service = MultiFileGenerationService(generators=[docx_generator])
zip_path = service.create_zip("output_files.zip")
print(f"ZIP created at: {zip_path}")
```

2. Generating XLSX Files
Use the BaseXlsxGenerator to generate .xlsx files with dynamic data and loops.
```
from file_generation.generators import BaseXlsxGenerator
from file_generation.core import MultiFileGenerationService

# Define the output directory and instance ID
base_output_dir = "/path/to/output"
instance_id = 42

# Define the context data for the template
xlsx_context = {
    "items": [
        {"name": "Item 1", "price": 10.99},
        {"name": "Item 2", "price": 15.99},
        {"name": "Item 3", "price": 7.50}
    ],
    "total": 34.48
}

# Initialize the XLSX generator
xlsx_generator = BaseXlsxGenerator(
    base_output_dir=base_output_dir,
    instance_id=instance_id,
    template_path="/path/to/template.xlsx",
    context=xlsx_context
)

# Generate files and create a ZIP archive
service = MultiFileGenerationService(generators=[xlsx_generator])
zip_path = service.create_zip("output_files.zip")
print(f"ZIP created at: {zip_path}")
```

3. Combining DOCX and XLSX Generation
You can combine multiple generators to create both .docx and .xlsx files in a single ZIP archive.

```
from file_generation.generators import BaseDocxGenerator, BaseXlsxGenerator
from file_generation.core import MultiFileGenerationService

# Define the output directory and instance ID
base_output_dir = "/path/to/output"
instance_id = 42

# DOCX context and generator
docx_context = {
    "company_name": "Example Corp",
    "date": "2025-01-31"
}
docx_generator = BaseDocxGenerator(
    base_output_dir=base_output_dir,
    instance_id=instance_id,
    templates=["/path/to/template1.docx"],
    context=docx_context
)

# XLSX context and generator
xlsx_context = {
    "items": [
        {"name": "Item 1", "price": 10.99},
        {"name": "Item 2", "price": 15.99}
    ],
    "total": 26.98
}
xlsx_generator = BaseXlsxGenerator(
    base_output_dir=base_output_dir,
    instance_id=instance_id,
    template_path="/path/to/template.xlsx",
    context=xlsx_context
)

# Generate files and create a ZIP archive
service = MultiFileGenerationService(generators=[docx_generator, xlsx_generator])
zip_path = service.create_zip("output_files.zip")
print(f"ZIP created at: {zip_path}")
```

## Advanced Usage
### Customizing Output Filenames
Override the _get_output_filename method in your generator to customize filenames.
```
class CustomDocxGenerator(BaseDocxGenerator):
    def _get_output_filename(self, doc_info: Dict) -> str:
        return f"custom_{self.instance_id}_{doc_info['template_name']}.docx"
```

### Adding New File Types
Extend the BaseFileGenerator to support new file types.

```
class CustomFileGenerator(BaseFileGenerator):
    def generate_files_and_return_paths(self) -> List[str]:
        # Implement your custom file generation logic here
        return ["/path/to/generated/file.custom"]
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Support
If you encounter any bug or have questions, please open an issue.