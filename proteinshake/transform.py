from typing import Tuple, Iterator, Any
from proteinshake.utils import error, ProteinGenerator
import hashlib, inspect


class Transform:
    """
    Abstract class for transforms. A transform can be stochastic or deterministic, which decides whether the transformed result can be precomputed and saved to disk (deterministic), or if it needs to be computed when retrieving a data item (stochastic). Transforms generally take a batch of Xy tuples, some subclasses exist that facilitate reshaping (see below). Transforms can be fit beforehand (on the 'train' partition).
    """

    stochastic = False

    def __call__(
        self, Xy: Iterator[Tuple[Tuple[Any], Any]]
    ) -> Iterator[Tuple[Tuple[Any], Any]]:
        return self.transform(Xy)

    def fit(self, X: ProteinGenerator) -> None:
        """Fits the transform.

        Parameters
        ----------
        X : ProteinGenerator
            The train partition of a protein dataset.
        """

    def transform(
        self, Xy: Iterator[Tuple[Tuple[Any], Any]]
    ) -> Iterator[Tuple[Tuple[Any], Any]]:
        """Transforms an Xy-iterator.

        Parameters
        ----------
        Xy : Iterator[Tuple[Tuple[Any], Any]]
            An Xy-iterator.

        Yields
        ------
        Iterator[Tuple[Tuple[Any], Any]]
            An Xy-iterator.
        """
        raise NotImplementedError

    def hash(self) -> str:
        """Computes a hash value encoding the class name and instantiation arguments.

        Returns
        -------
        str
            A hash value.
        """
        h = hashlib.sha256()
        h.update(str(self.__class__).encode())
        h.update(b"|")

        # Get argument names and values using inspect
        arg_spec = inspect.getargspec(self.__init__)
        args = arg_spec.args[1:]  # Skip "self"

        # Create a sorted list of key-value pairs for arguments
        arg_vals = [(arg, getattr(self, arg)) for arg in args]
        sorted_args = sorted(arg_vals)

        # Update hash with string representation of arguments
        h.update(repr(sorted_args).encode())
        return h.hexdigest()


class DataTransform(Transform):
    """Reshapes the Xy-iterator to take only a single X instance as input."""

    def __call__(self, Xy):
        X, y = Xy
        shape = X.shape
        X = self.transform(X.flatten())
        return X.reshape(*shape, *X.shape[1:]), y

    def transform(self, X: Iterator[Any]) -> Iterator[Any]:
        return X


class CoTransform(Transform):
    """Reshapes the Xy-iterator to take X and y as separate arguments."""

    def __call__(self, Xy):
        return self.transform(*Xy)

    def transform(self, X, y):
        return X, y


class TupleTransform(Transform):
    """Reshapes the Xy-iterator to take only X tuples as an input."""

    def __call__(self, Xy):
        X, y = Xy
        return self.transform(X), y

    def transform(self, X: Tuple):
        return X


class LabelTransform(Transform):
    """Reshapes the Xy-iterator to take only the label as input."""

    def __call__(self, Xy):
        X, y = Xy
        return X, self.transform(y)

    def transform(self, y):
        return y

    def inverse_transform(self, y):
        return y


class IdentityTransform(Transform):
    """Does nothing."""

    def __call__(self, Xy):
        return Xy

    def transform(self, Xy):
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

    def hash(self):
        h = hashlib.sha256()
        for transform in self.deterministic_transforms:
            h.update(transform.hash().encode())
        return h.hexdigest()

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
