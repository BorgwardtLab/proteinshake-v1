from ..transform import LabelTransform


class MinMaxScalerTransform(LabelTransform):
    def fit(self, Xy):
        labels = [p[0][0]["label"] for p in Xy]
        self.min, self.max = min(labels), max(labels)

    def transform(self, y):
        return (y - self.min) / (self.max - self.min)

    def inverse_transform(self, y):
        return y * (self.max - self.min) + self.min
