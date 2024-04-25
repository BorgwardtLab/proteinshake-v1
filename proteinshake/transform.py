from typing import Tuple
from proteinshake.utils import error


class Transform:
    """
    Abstract class for transforms. A transform can be stochastic or deterministic, which decides whether the transformed result can be precomputed and saved to disk (deterministic), or if it needs to be computed when retrieving a data item (stochastic). Transforms generally take a batch of Xy tuples, some subclasses exist that facilitate reshaping (see below). Transforms can be fit beforehand (on the 'train' partition).
    """

    stochastic = False

    def __call__(self, Xy):
        raise NotImplementedError

    def fit(self, X):
        pass

    def transform(self, X):
        raise NotImplementedError


class DataTransform(Transform):
    def __call__(self, Xy):
        X, y = Xy
        shape = X.shape
        X = self.transform(X.flatten())
        return X.reshape(*shape, *X.shape[1:]), y

    def transform(self, X):
        return X


class CoTransform(Transform):
    def __call__(self, Xy):
        return self.transform(*Xy)

    def transform(self, X, y):
        return X, y


class TupleTransform(Transform):
    def __call__(self, Xy):
        X, y = Xy
        return self.transform(X), y

    def transform(self, X: Tuple):
        return X


class LabelTransform(Transform):
    def __call__(self, Xy):
        X, y = Xy
        return X, self.transform(y)

    def transform(self, y):
        return y

    def inverse_transform(self, y):
        return y


class IdentityTransform(Transform):
    def __call__(self, Xy):
        return Xy


class Compose:
    """
    Composes multiple transforms into one object. Takes care of splitting the deterministic and stochastic part, as well as storing the framework create_dataloader method.
    """

    def __init__(self, *transforms):
        self.transforms = transforms
        self.deterministic_transforms = []
        self.stochastic_transforms = []
        stochastic_breakpoint = False
        for transform in transforms:
            if transform.stochastic:
                stochastic_breakpoint = True
            if stochastic_breakpoint:
                self.stochastic_transforms.append(transform)
            else:
                self.deterministic_transforms.append(transform)
            if hasattr(transform, "create_loader"):
                if hasattr(self, "create_loader"):
                    error("You cannot use more than one framework.")
                setattr(self, "create_loader", transform.create_loader)

    @property
    def hash(self):
        return self.__class__.__name__

    def fit(self, dataset):
        for transform in self.transforms:
            transform.fit(dataset)

    def deterministic_transform(self, Xy):
        for transform in self.deterministic_transforms:
            Xy = transform(Xy)
        return Xy

    def stochastic_transform(self, Xy):
        for transform in self.stochastic_transforms:
            Xy = transform(Xy)
        return Xy

    def inverse_transform(self, y):
        for transform in self.transforms:
            if hasattr(transform, "inverse_transform"):
                y = transform.inverse_transform(y)
        return y
