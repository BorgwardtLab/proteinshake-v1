from proteinshake.target import Target


class AttributeTarget(Target):
    def __init__(self, attribute="label") -> None:
        super().__init__()
        self.attribute = attribute

    def __call__(self, dataset):
        return (((p,), p[self.attribute]) for p in dataset)
