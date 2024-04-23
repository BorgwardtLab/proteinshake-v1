from proteinshake.metric import Metric
import numpy as np


class DummyMetric(Metric):
    def __call__(self, y_true, y_pred):
        return {"Accuracy": np.random.random()}
