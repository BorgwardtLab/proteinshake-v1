from ..transform import RepresentationTransform


class PointRepresentationTransform(RepresentationTransform):
    def transform(self, protein):
        return protein["coords"]
