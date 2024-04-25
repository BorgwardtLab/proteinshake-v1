from pathlib import Path
from typing import Union
import os

from ..adapter import Adapter
from ..processor import Processor
from ..utils import ProteinGenerator


class LocalAdapter(Adapter):

    def __init__(self, path: Union[str, Path] = "") -> None:
        self.path = Path(path)

    def download(self):
        files = [
            os.path.join(root, file)
            for root, dirs, files in os.walk(self.path)
            for file in files
            if Processor.is_protein_file(file)
        ]

        def generator():
            for file in files[:10]:
                protein = Processor.process(file)
                yield protein

        return ProteinGenerator(generator(), len(files), {})
