from proteinshake.split import Split
import itertools


class DummySplit(Split):
    def __call__(self, Xy):
        train, testval = itertools.tee(Xy)
        test, val = itertools.tee(testval)
        return {
            "train": filter(lambda Xy: Xy[0][0]["split"] == "train", train),
            "test": filter(lambda Xy: Xy[0][0]["split"] == "test", test),
            "val": filter(lambda Xy: Xy[0][0]["split"] == "val", val),
        }
