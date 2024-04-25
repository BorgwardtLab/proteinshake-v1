from ..adapter import Adapter
from ..utils import amino_acid_alphabet, ProteinGenerator
import numpy as np


class SyntheticAdapter(Adapter):

    def download(self, n=10):
        rng = np.random.default_rng(42)
        proteins = (
            {
                "ID": f"protein_{i}",
                "coords": rng.integers(0, 100, size=(300, 3)).tolist(),
                "sequence": str(
                    "".join(rng.choice(list(amino_acid_alphabet)) for _ in range(300))
                ),
                "label": int(rng.random() * 100),
                "split": str(rng.choice(["train", "test", "val"])),
            }
            for i in range(10)
        )
        return ProteinGenerator(proteins, 10, {})
