from pathlib import Path
from typing import Union
from biopandas.pdb import PandasPdb
from biopandas.mmcif import PandasMmcif


class FileProcessor:
    """
    Converts a pdb/mmcif file to a more efficient Atoms & Residue format. Implements QC.
    Applies transforms to clean and polish the structure, e.g. energy minimization.
    Also computes and annotates quality scores which can be used for later filtering.
    """

    @classmethod
    def is_protein_file(self, path):
        suffixes = Path(path).suffixes
        return any(suffix in [".pdb", ".cif"] for suffix in suffixes)

    @classmethod
    def process(self, path: Union[str, Path]):
        path = Path(path)
        if ".pdb" in path.suffixes:
            pdb = PandasPdb().read_pdb(str(path))
            df = pdb.df["ATOM"]
            sequence = "".join(pdb.amino3to1()["residue_name"].to_list())
            x, y, z = df.x_coord.to_list(), df.y_coord.to_list(), df.z_coord.to_list()
        elif ".cif" in path.suffixes:
            pdb = PandasMmcif().read_mmcif(str(path))
            df = pdb.df["ATOM"]
            sequence = "".join(pdb.amino3to1()["auth_comp_id"].to_list())
            x, y, z = df.Cartn_x.to_list(), df.Cartn_y.to_list(), df.Cartn_z.to_list()
        return {
            "ID": id,
            "sequence": sequence,
            "x": x,
            "y": y,
            "z": z,
        }
