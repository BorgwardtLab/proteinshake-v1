from proteinshake.task import Task
from proteinshake.metrics import DummyMetric
from proteinshake.targets import AttributeTarget
from proteinshake.splits import DummySplit


class DummyTask(Task):
    dataset = "test"
    split = DummySplit
    target = AttributeTarget
    metrics = DummyMetric
