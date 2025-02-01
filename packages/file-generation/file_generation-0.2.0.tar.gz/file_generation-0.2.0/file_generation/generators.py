import os
import logging
from typing import List, Dict, Any, Callable
from docxtpl import DocxTemplate
from openpyxl import load_workbook
from .core import BaseFileGenerator, MultiFileGenerationError

logger = logging.getLogger(__name__)


class BaseDocxGenerator(BaseFileGenerator):
    def __init__(self, base_output_dir: str, instance_id: Any, templates: List[str], context: Dict[str, Any],
                 get_output_filename: Callable[[Dict[str, Any]], str] = None):
        super().__init__(base_output_dir, instance_id)
        self.templates = templates
        self.context = context
        self.get_output_filename = get_output_filename or self.default_get_output_filename

    def generate_files_and_return_paths(self) -> List[str]:
        rendered_paths = []
        for template_path in self.templates:
            output_filename = self.get_output_filename({"file": template_path})
            rendered_path = self._render_template(template_path, output_filename)
            rendered_paths.append(rendered_path)
        return rendered_paths

    def _render_template(self, template_path: str, output_filename: str) -> str:
        try:
            template_document = DocxTemplate(template_path)
            template_document.render(self.context)
            output_path = os.path.join(self.base_output_dir, output_filename)
            template_document.save(output_path)
            return output_path
        except Exception as e:
            logger.exception(f"Error rendering template '{template_path}'")
            raise MultiFileGenerationError(f"Error rendering DOCX template '{template_path}': {e}") from e

    def default_get_output_filename(self, doc_obj: Dict[str, Any]) -> str:
        base_name = os.path.splitext(os.path.basename(doc_obj['file']))[0]
        return f"{base_name}_{self.instance_id}.docx"
