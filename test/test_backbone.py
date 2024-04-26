import unittest, tempfile
from proteinshake.dataset import Dataset
from proteinshake.task import Task
from proteinshake.adapter import Adapter
from proteinshake.metric import Metric
from proteinshake.target import Target
from proteinshake.utils import ProteinGenerator, amino_acid_alphabet
from proteinshake.transform import DataTransform
import numpy as np


class TestBackbone(unittest.TestCase):

    def test(self):
        with tempfile.TemporaryDirectory() as tmp:

            class TestAdapter(Adapter):

                def download(self):
                    rng = np.random.default_rng(42)
                    proteins = (
                        {
                            "ID": f"protein_{i}",
                            "coords": rng.integers(0, 100, size=(300, 3)).tolist(),
                            "sequence": str(
                                "".join(
                                    rng.choice(list(amino_acid_alphabet))
                                    for _ in range(300)
                                )
                            ),
                            "label": int(rng.random() * 100),
                            "split": str(rng.choice(["train", "test", "val"])),
                        }
                        for i in range(10)
                    )
                    return ProteinGenerator(proteins, 10, {})

            class TestDataset(Dataset):
                def release(self, version: str = None):
                    proteins = TestAdapter().download()
                    return self.save(proteins, version)

            class TestTarget(Target):
                def __call__(self, dataset):
                    return (((p,), p["label"]) for p in dataset)

            class TestMetric(Metric):
                def __call__(self, y_true, y_pred):
                    return {"Accuracy": np.random.random()}

            class TestTransform(DataTransform):
                def transform(self, X):
                    return X

                def create_loader(self, iterator, **kwargs):
                    return iterator()

            class TestTask(Task):
                dataset = TestDataset(root=tmp)
                target = TestTarget()
                metrics = TestMetric()

            class TestModel:
                def __call__(self, batch):
                    X, y = batch
                    return np.random.randn(*y.shape)

            task = TestTask().transform(TestTransform())
            model = TestModel()
            for batch in task.train_loader(shuffle=True):
                y_pred = model(batch)
            for batch in task.test_loader():
                X, y_true = batch
                y_pred = model(batch)
            metrics = task.evaluate(y_true, y_pred)
            print(metrics)


if __name__ == "__main__":
    unittest.main()
