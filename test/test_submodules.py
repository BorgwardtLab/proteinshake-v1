import unittest, tempfile, importlib
import numpy as np


class TestSubmodules(unittest.TestCase):

    def _check_submodule(self, submodule, superclass):
        module = importlib.import_module(f"proteinshake.{submodule}")
        for name in dir(module):
            cls = getattr(module, name)
            if issubclass(cls, superclass):
                # try to instantiate submodule member class
                instance = cls()

    def test_adapters(self):
        from proteinshake.adapter import Adapter

        self._check_submodule("adapters", Adapter)

    def test_datasets(self):
        from proteinshake.adapter import Dataset

        self._check_submodule("datasets", Dataset)

    def test_metrics(self):
        from proteinshake.adapter import Metric

        self._check_submodule("metrics", Metric)

    def test_modifiers(self):
        from proteinshake.adapter import Modifier

        self._check_submodule("modifiers", Modifier)

    def test_targets(self):
        from proteinshake.adapter import Targets

        self._check_submodule("targets", Targets)

    def test_tasks(self):
        from proteinshake.adapter import Task

        self._check_submodule("tasks", Task)

    def test_transforms(self):
        from proteinshake.adapter import Transform

        self._check_submodule("transforms", Transform)


if __name__ == "__main__":
    unittest.main()
