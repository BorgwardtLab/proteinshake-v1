class ClassificationEvaluator(Evaluator):
    def __call__(self, pred : list, truth: list):
        return {'accuracy': sklearn.accuracy(pred, truth)}
        pass
