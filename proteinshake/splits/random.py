class MySplitter:
    def __init__(self, seed=None) -> None:
        self.rng = np.random.rng(seed)

    def fit(self, dataset):
        n = len(dataset)
        train, test_val = train_test_split(
            np.arange(n), test_size=0.2, random_state=self.rng.random()
        )
        test, val = train_test_split(
            test_val, test_size=0.5, random_state=self.rng.random()
        )
        self.lookup = {
            **{index: "train" for index in train},
            **{index: "test" for index in test},
            **{index: "val" for index in val},
        }

    def assign(self, index, protein):
        return self.lookup[index]
