from proteinshake.frontend.dataset import Dataset
from proteinshake.frontend.splitters import Splitter
from proteinshake.frontend.targets import Target
from proteinshake.frontend.evaluators import Evaluator
from proteinshake.frontend.transforms import Transform


class Task:
    def __init__(
        self,
        dataset: Dataset,
        splitter: Splitter,
        target: Target,
        evaluator: Evaluator,
        transform: Transform,
    ) -> None:
        # compute splits. `splitter` returns a dictionary of name:index pairs.
        self.index = splitter(dataset)
        # partition the dataset. the dataset will optimize data loading.
        dataset.partition(self.index)
        # fit the transforms
        transform.fit(dataset)
        # create X,y,dataloader for each item in the split.
        for name, index in self.index.items():
            # get the partition of the split, apply transforms, and save to disk.
            X,y = dataset.split(name).apply(target, transform)
            # create a dataloader for the framework
            loader = dataset.create_dataloader(X, y)
            # add attributes to the task object
            setattr(self, f"X_{name}", X)
            setattr(self, f"y_{name}", y)
            setattr(self, f"{name}_dataloader", loader)
            setattr(self, f"{name}_index", index)
        # evaluator is a callable: `task.evaluate(y_true, y_pred)`
        self.evaluate = evaluator
