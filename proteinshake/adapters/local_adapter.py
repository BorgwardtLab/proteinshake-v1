from pathlib import Path
from typing import Union
import os

from ..adapter import Adapter
from ..file_processor import FileProcessor
from ..utils import ProteinGenerator


class LocalAdapter(Adapter):

    def __init__(self, path: Union[str, Path]) -> None:
        super().__init__()
        self.path = Path(path)

    def sync(self):
        files = [
            os.path.join(root, file)
            for root, dirs, files in os.walk(self.path)
            for file in files
            if FileProcessor.is_protein_file(file)
        ]

        def generator():
            for file in files[:10]:
                protein = FileProcessor.process(file)
                yield protein

        return ProteinGenerator(generator(), len(files), {})
