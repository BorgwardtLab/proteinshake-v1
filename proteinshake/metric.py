from numpy import ndarray
from typing import Dict, Float


class Metric:
    """
    Computes a relevant metric for a task.
    """

    def __init__(self, *args, **kwargs) -> None:
        pass

    def __call__(self, y_true: ndarray, y_pred: ndarray) -> Dict[str, Float]:
        """Computes a metric value from ground truth and predictions.

        Parameters
        ----------
        y_true : ndarray
            Ground truth values.
        y_pred : ndarray
            Predictions.

        Returns
        -------
        Dict[str, Float]
            A dictionary with the name and value of the metric.
        """
        pass
