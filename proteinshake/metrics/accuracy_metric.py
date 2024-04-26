from typing import Any
from ..metric import Metric
from sklearn.metrics import accuracy_score


class AccuracyMetric(Metric):

    def __init__(self, threshold=0.5) -> None:
        super().__init__()
        self.threshold = threshold

    def __call__(self, y_true, y_pred):
        y_pred = (y_pred >= self.threshold).astype(int)
        return accuracy_score(y_true, y_pred)
