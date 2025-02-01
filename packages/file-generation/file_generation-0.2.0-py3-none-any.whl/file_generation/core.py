import os
import zipfile
import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Any

logger = logging.getLogger(__name__)


class MultiFileGenerationError(Exception):
    pass


class BaseFileGenerator(ABC):
    def __init__(self, base_output_dir: str, instance_id: Any):
        self.base_output_dir = base_output_dir
        self.instance_id = instance_id

    @abstractmethod
    def generate_files_and_return_paths(self) -> List[str]:
        pass


class ZippingService:
    def __init__(self, output_filename: str, file_paths: List[str]):
        self.output_filename = output_filename
        self.file_paths = file_paths

    def zip(self) -> Optional[str]:
        if not self.file_paths:
            logger.warning("No files to zip.")
            return None
        try:
            with zipfile.ZipFile(self.output_filename, "w", zipfile.ZIP_DEFLATED) as zf:
                for path in self.file_paths:
                    if os.path.exists(path):
                        zf.write(path, os.path.basename(path))
            return self.output_filename
        except Exception as e:
            logger.error(f"Failed to create zip {self.output_filename}: {e}")
            raise MultiFileGenerationError(f"Failed to create zip: {e}") from e


class MultiFileGenerationService:
    def __init__(self, generators: List[BaseFileGenerator]):
        self.generators = generators

    def create_zip(self, zip_name: str) -> str:
        if not zip_name:
            raise ValueError("No zip name provided.")
        try:
            all_generated_paths = []
            for generator in self.generators:
                generated_paths = generator.generate_files_and_return_paths()
                all_generated_paths.extend(generated_paths)

            if not all_generated_paths:
                raise MultiFileGenerationError("No files were generated.")

            zip_path = os.path.join(self.generators[0].base_output_dir, zip_name)
            zipper = ZippingService(output_filename=zip_path, file_paths=all_generated_paths)
            final_zip = zipper.zip()
            if not final_zip:
                raise MultiFileGenerationError("No ZIP file was created.")
            return final_zip
        except Exception as e:
            logger.exception("Error generating files or creating zip.")
            raise MultiFileGenerationError(str(e)) from e
