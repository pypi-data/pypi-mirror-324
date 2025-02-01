import os
import zipfile
from abc import ABC, abstractmethod
from typing import List, Optional


class MultiFileGenerationError(Exception):
    """
    Raised when any error occurs in file generation or zipping.
    """
    pass


class BaseFileGenerator(ABC):
    def __init__(self, instance):
        self.instance = instance

    @abstractmethod
    def generate_files_and_return_paths(self) -> List[str]:
        """
        Subclasses must generate the required files and return a list of absolute
        paths. If an error occurs, raise MultiFileGenerationError with details.
        """
        pass


class ZippingService:
    def __init__(self, output_filename: str, file_paths: List[str]):
        self.output_filename = output_filename
        self.file_paths = file_paths

    def zip(self) -> Optional[str]:
        if not self.file_paths:
            return None
        try:
            with zipfile.ZipFile(self.output_filename, "w", zipfile.ZIP_DEFLATED) as zf:
                for path in self.file_paths:
                    if os.path.exists(path):
                        zf.write(path, os.path.basename(path))
            return self.output_filename
        except Exception as e:
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
                raise MultiFileGenerationError("No files were generated. Possibly no documents or templates found.")

            zip_path = os.path.join("/tmp", zip_name)
            zipper = ZippingService(output_filename=zip_path, file_paths=all_generated_paths)
            final_zip = zipper.zip()
            if not final_zip:
                raise MultiFileGenerationError("No ZIP file was created. Possibly empty file list.")
            return final_zip
        except Exception as e:
            raise MultiFileGenerationError(str(e)) from e


    # The following methods (_process_static_placeholders, _replace_placeholders, etc.)
    # remain unchanged as they don't rely on Django.
    # [Include all the existing methods from the original BaseXlsxGenerator here]