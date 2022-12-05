import time
import shutil
import tempfile
import os
import subprocess

import pandas as pd
from tqdm import tqdm
import numpy as np

from proteinshake.utils import protein_to_pdb

class Surface():
    """ Surface representation of a protein.

    Converts a protein object to a surface using open3d.

    Parameters
    ----------
    protein: dict
        A protein object.
    construction: str
        Whether to use knn or eps construction.

    """

    def __init__(self, protein, density=0.2):
        resolution = 'atom' if 'atom' in protein else 'residue'

        self.data = self._compute_surface(protein, d=density)

    def _compute_surface(self, protein, d=0.2):
        """ Call DMS to compute a surface for the PDB.

        Usage: dms input_file [-a] [-d density] [-g file] [-i file] [-n] [-w radius] [-v] -o file
        -a	use all atoms, not just amino acids
        -d	change density of points
        -g	send messages to file
        -i	calculate only surface for specified atoms
        -n	calculate normals for surface points
        -w	change probe radius
        -v	verbose
        -o	specify output file name (required)

        See: https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/midas/dms1.html#ref
        """
        with tempfile.TemporaryDirectory() as tf:
            pdb_path = os.path.join(tf, "in.pdb")
            dest = os.path.join(tf, "out.surf")
            protein_to_pdb(protein, pdb_path)
            assert shutil.which('dms') is not None, "DMS executable not in PATH go here to install https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/midas/dms1.html#ref."
            cmd = ['dms', pdb_path, '-n', '-d', str(d), '-o', dest]
            start = time.time()
            subprocess.run(cmd,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.STDOUT
                           )
            print(time.time() - start)
            data = self._parse_dms(dest)
            pass

    def _parse_dms(self, path):
        """ Extract surface points and normal vectors for each
        point.

        Parameters
        ------------
        path:
            Path to DMS output file.

        Returns
        --------
        pd.DataFrame
            DataFrame with one row for each surface atom.
        """
        names = ['residue_name',
                 'residue_index',
                 'atom_name',
                 'x',
                 'y',
                 'z',
                 'point_type',
                 'area',
                 'x_norm',
                 'y_norm',
                 'z_norm'
                 ]
        df = pd.read_csv(path,
                         delim_whitespace=True,
                         header=None,
                         names=names
                         )
        df = df.dropna(axis=0)
        return df

class SurfaceDataset():
    """ Graph representation of a protein structure dataset.

    Parameters
    ----------
    proteins: generator
        A generator of protein objects from a Dataset.
    size: int
        The size of the dataset.
    path: str
        Path to save the processed dataset.
    resolution: str, default 'residue'
        Resolution of the proteins to use in the graph representation. Can be 'atom' or 'residue'.
        Surface reconstruction algorithms (see http://www.open3d.org/docs/latest/tutorial/geometry/surface_reconstruction.html).
        Can be 'ball', 'alpha', 'poisson', Default is 'ball'.
    """

    def __init__(self, proteins, size, path, method='ball', resolution='atom'):
        assert resolution == 'atom', "For this rep. we need atom-level."
        self.path = f'{path}/processed/surface/{resolution}_{method}'
        self.surfaces = (Surface(protein) for protein in proteins)
        self.size = size
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def pyg(self, *args, **kwargs):
        from proteinshake.frameworks.pyg import PygGraphDataset
        return PygGraphDataset(self.surfaces, self.size, self.path+'.pyg', *args, **kwargs)

    def dgl(self, *args, **kwargs):
        from proteinshake.frameworks.dgl import DGLGraphDataset
        return DGLGraphDataset(self.surfaces, self.size, self.path+'.dgl', *args, **kwargs)

    def nx(self, *args, **kwargs):
        from proteinshake.frameworks.nx import NetworkxGraphDataset
        return NetworkxGraphDataset(self.surfaces, self.size, self.path+'.nx', *args, **kwargs)

if __name__ == "__main__":
    from proteinshake.datasets import TMAlignDataset
    import tempfile
    with tempfile.TemporaryDirectory() as tf:
        da = TMAlignDataset(root=tf)
        da_surf = da.to_surface(resolution='atom')
        list(da_surf.surfaces)
