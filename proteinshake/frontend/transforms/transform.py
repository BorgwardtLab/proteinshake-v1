class Transform:
    pass


class DataTransform:
    def __init__(self, representation_transform, framework_transform):
        self.representation_transform = representation_transform
        self.framework_transform = framework_transform

    def __call__(self, x):
        return self.framework_transform(self.representation_transform(x))


class TargetTransform:
    pass


class LabelTransform:
    pass
