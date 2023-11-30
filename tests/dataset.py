import unittest
import numpy as np
from proteinshake.frontend.dataset import Dataset
from proteinshake.frontend.transforms import *


class TestDataset(unittest.TestCase):
    def test_dataset(self):
        dataset = Dataset()

        X_transform = DataTransform(
            representation_transform=PointRepresentationTransform(),
            framework_transform=TorchFrameworkTransform(),
        )

        class MyTargetTransform(TargetTransform):
            def __call__(self, protein):
                return protein["label"]

        class MyLabelTransform(LabelTransform):
            def __call__(self, label):
                return label * 100

        target = MyTargetTransform()
        y_transform = MyLabelTransform()

        dataset.partition({"train": np.arange(90), "test": np.arange(90, 100)})
        print("train:", [p["ID"] for p in dataset.split("train").proteins])
        print("test:", [p["ID"] for p in dataset.split("test").proteins])

        X = dataset.split("train").apply(X_transform)
        y = dataset.split("train").apply(target, y_transform)
        print(next(X), next(y))

        loader = dataset.create_dataloader(X, y)


if __name__ == "__main__":
    unittest.main()
