import unittest
from proteinshake.tasks import DummyTask
from proteinshake.transform import *
from proteinshake.transforms import *


class TestTask(unittest.TestCase):
    def test_task(self):
        class MyLabelTransform(LabelTransform):
            def transform(self, y):
                return -y

            def inverse_transform(self, y):
                return -y

        task = DummyTask(target_kwargs={"attribute": "label"}, shard_size=8).transform(
            MyLabelTransform(),
            PointRepresentationTransform(),
            TorchFrameworkTransform(),
        )

        for epoch in range(5):
            for X, y in task.train_loader(batch_size=16, shuffle=True, random_seed=0):
                print("X", X.shape)
                print("y", y.shape)
                break


if __name__ == "__main__":
    unittest.main()
