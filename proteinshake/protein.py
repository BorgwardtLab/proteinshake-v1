from .utilities import avro_schema_from_example


class Protein:
    """
    A dictionary-type data structure for a protein. Contains the PS-ID, other database IDs, sequences, protein-level information, and links to assets and structures.
    """

    def __init__(self) -> None:
        pass

    def from_dict(self, protein_dict):
        pass

    def to_dict(self):
        pass

    @classmethod
    def avro_schema(self):
        example = {
            "ID": "",
            "sequence": "",
            "x": [1.0],
            "y": [1.0],
            "z": [1.0],
        }
        return avro_schema_from_example(example)
