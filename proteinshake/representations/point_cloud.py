from proteinshake.transform import DataTransform
from proteinshake.representation import Representation
import numpy as np


class PointRepresentationTransform(Representation, DataTransform):
    def transform(self, X):
        return np.asarray([protein["coords"] for protein in X])
