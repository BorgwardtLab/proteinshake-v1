import unittest, tempfile, importlib
import numpy as np


class TestSubmodules(unittest.TestCase):

    def _get_members(self, name):
        supermodule = importlib.import_module(f"proteinshake.{name}")
        superclass = getattr(supermodule, name.capitalize())
        submodule = importlib.import_module(f"proteinshake.{name}s")
        subclasses = dict(
            [
                (name, cls)
                for name, cls in submodule.__dict__.items()
                if isinstance(cls, type)
            ]
        )
        for cls_name, cls in subclasses.items():
            print(cls_name, cls)
            if issubclass(cls, superclass):
                yield cls

    def test_adapters(self):
        for Adapter in self._get_members("adapter"):
            adapter = Adapter()

    def test_datasets(self):
        with tempfile.TemporaryDirectory() as tmp:
            for Dataset in self._get_members("dataset"):
                dataset = Dataset(path=tmp)

    def test_frameworks(self):
        for Framework in self._get_members("framework"):
            framework = Framework()

    def test_metrics(self):
        for Metric in self._get_members("metric"):
            metric = Metric()

    def test_modifiers(self):
        for Modifier in self._get_members("modifier"):
            modifier = Modifier()

    def test_representations(self):
        for Representation in self._get_members("representation"):
            representation = Representation()

    def test_targets(self):
        for Target in self._get_members("target"):
            target = Target()

    def test_tasks(self):
        with tempfile.TemporaryDirectory() as tmp:
            for Task in self._get_members("task"):
                task = Task(root=tmp)

    def test_transforms(self):
        for Transform in self._get_members("transform"):
            transform = Transform()


if __name__ == "__main__":
    unittest.main()
