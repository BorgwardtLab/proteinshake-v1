from proteinshake.frontend import (
    Dataset,
    Splitter,
    Target,
    Evaluator,
    TargetTransform,
    DataTransform,
)


class Task:
    def __init__(
        self,
        dataset: Dataset,
        splitter: Splitter,
        target: Target,
        evaluator: Evaluator,
        X_transform: DataTransform,
        y_transform: TargetTransform,
    ) -> None:
        # compute splits. `splitter` returns a dictionary of name:index pairs.
        self.index = splitter(dataset)
        # partition the dataset. the dataset will optimize data loading.
        dataset.partition(**self.index)
        # create X,y,dataloader for each item in the split.
        for name, index in self.index.items():
            # get the partition of the split, apply transforms, and save to disk.
            X = dataset.get(name).apply(X_transform)
            # apply the target transform
            y = dataset.get(name).apply(y_transform, target)
            # create a dataloader for the framework
            loader = self.dataset.framework.create_dataloader(X, y)
            # add attributes to the task object
            setattr(self, f"X_{name}", X)
            setattr(self, f"y_{name}", y)
            setattr(self, f"{name}_dataloader", loader)
            setattr(self, f"{name}_index", index)
        # evaluator is a callable: `task.evaluate(y_true, y_pred)`
        self.evaluate = evaluator
