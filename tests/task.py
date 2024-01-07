import unittest
import numpy as np
import itertools
from proteinshake.frontend.evaluators import Metrics
from proteinshake.frontend.targets import Target
from proteinshake.frontend.splitters import Split
from proteinshake.frontend.task import Task
from proteinshake.frontend.transforms import *
from proteinshake.frontend.transforms import Transform, LabelTransform


class TestTask(unittest.TestCase):
    def test_task(self):
        # CONTRIBUTOR
        class MyTarget(Target):
            def __call__(self, dataset):
                return (((p,), p["label"]) for p in dataset)

        class MyMetrics(Metrics):
            def __call__(self, y_true, y_pred):
                return {"Accuracy": np.random.random()}

        class MySplit(Split):
            def __call__(self, Xy):
                # this implementation looks a bit inefficient
                train, testval = itertools.tee(Xy)
                test, val = itertools.tee(testval)
                return {
                    "train": filter(lambda Xy: Xy[0][0]["split"] == "train", train),
                    "test": filter(lambda Xy: Xy[0][0]["split"] == "test", test),
                    "val": filter(lambda Xy: Xy[0][0]["split"] == "val", val),
                }

        class MyAugmentation(Transform):
            def transform(self, X):
                return X

        class MyTask(Task):
            dataset = "test"
            split = MySplit
            target = MyTarget
            metrics = MyMetrics
            augmentation = MyAugmentation

        # END USER
        class MyLabelTransform(LabelTransform):
            def transform(self, y):
                return -y

            def inverse_transform(self, y):
                return -y

        task = MyTask(shard_size=8).transform(
            MyLabelTransform(),
            PointRepresentationTransform(),
            TorchFrameworkTransform(),
        )

        for epoch in range(5):
            for X, y in task.train_loader(batch_size=64, random_seed=0):
                print("X", X.shape)
                print("y", y.shape)
                break


if __name__ == "__main__":
    unittest.main()
