from ..transform import Transform
from proteinshake.frontend.representation import Representation
import numpy as np


class PointRepresentationTransform(Representation, Transform):
    def transform(self, X):
        return np.asarray([protein["coords"] for protein in X])
