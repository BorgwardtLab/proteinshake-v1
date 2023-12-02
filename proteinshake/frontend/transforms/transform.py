class Transform:
    def fit(self, x):
        pass

    def transform(self, x):
        return x

    def __call__(self, *args, **kwargs):
        return self.transform(*args, **kwargs)


class RepresentationTransform(Transform):
    pass


class FrameworkTransform(Transform):
    pass


class DataTransform(Transform):
    def __init__(
        self,
        representation_transform=RepresentationTransform(),
        framework_transform=FrameworkTransform(),
    ):
        self.representation_transform = representation_transform
        self.framework_transform = framework_transform

    def transform(self, x):
        return self.framework_transform(self.representation_transform(x))


class TargetTransform(Transform):
    pass


class LabelTransform(Transform):
    pass

class Compose(Transform):
    def __init__(self, *transforms):
        # split transforms at the first non-deterministic
        pass
    
    def transform_deterministic(self, proteins, labels):
        pass
    
    def transform_nondeterministic(self, proteins, labels):
        pass
    
    def fit(self, dataset):
        # fit each transform
        pass