import unittest, importlib, tempfile

class TestDatasets(unittest.TestCase):

    def test_all(self):
        return
        with tempfile.TemporaryDirectory() as tmp:
            module = importlib.import_module("proteinshake.datasets")
            datasets = dict([(name, cls) for name, cls in module.__dict__.items() if isinstance(cls, type)])
            for name, Dataset in datasets.items():
                print(f'Testing {name}')
                Dataset(path=tmp)
            
if __name__ == '__main__':
    unittest.main()