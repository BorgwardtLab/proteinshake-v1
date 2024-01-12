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
        print("EVALUATION")
        metrics = task.evaluate(np.ones((10,)) * 3, np.ones((10,)) * 5)
        print(metrics)


if __name__ == "__main__":
    unittest.main()
