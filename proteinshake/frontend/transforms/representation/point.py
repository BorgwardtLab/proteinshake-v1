from .representation import RepresentationTransform


class PointRepresentationTransform(RepresentationTransform):
    def __call__(self, protein):
        return protein["coords"]
