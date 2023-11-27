## Task API

A task brings three objects: `Splitter`, `Target`, `Evaluator` to a given `proteinshake.Dataset` instance.

The `Splitter` object returns a 3-tuple of train, val and test indices for a given dataset.

The `Target` object returns the prediction target for a single Entity object (or pair of Entity objects in pairwise tasks).

The `Evaluator` object returns a dictionary of performance measures given a list of predictions and `Target` values.

We offer many instances of these objects which can be combined to create tasks.

You can create a task on the fly like this:

```python
my_task = Task(dataset, splitter=TemporalSplitter(), target=PairwisePropertyTarget(label='is_interface'), evaluator=BinaryPairwiseEval())
```

Or contribute a predefined task like this:

```python
class ProteinInterfaceTask(Task):
    def __init__(self, dataset):
        super().__init__(splitter=TemporalSplitter(cutoff=2018), 
                         target=PairwisePropertyTarget(label='is_interface), 
                         evaluation=BinaryPairwiseEval())
```

You can pass any dataset to a `Task` object provided it contains the information needed by the splitter/target/and eval functions (e.g. structure publication date for temporal splits). 

```
dataset_1 = ProteinshakeECDataset()
dataset_2 = DeepFriECDataset()
task_1 = EnzymeClassTask(dataset_1)
task_2 = EnzymeClassTask(dataset_2)
```

Task machinery is fully framework agnostic tokenizing happens at the dataset transform level.
