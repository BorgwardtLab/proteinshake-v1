from proteinshake.frontend.transforms import Transform


class MyLabelTransform(Transform):
    def fit(self, dataset):
        labels = [p["label"] for p in dataset.split("train").proteins]
        self.min, self.max = min(labels), max(labels)

    def transform(self, X, y, index):
        y_transformed = (y - self.min) / (self.max - self.min)
        return X, y_transformed, index

    def inverse_transform(self, y):
        return y * (self.max - self.min) + self.min
