Custom datasets and tasks
=========================

ProteinShake was made to be extended, and as such we made it easy to create new datasets or tasks.

Custom Datasets
---------------

To create a new dataset, inherit from the `Dataset` class and define a `.release()` method.

.. code:: python

    from proteinshake.dataset import Dataset
    from proteinshake.mocks import MockAdapter
    from proteinshake.modifiers import RandomSplit


    class TestDataset(Dataset):
        def release(self, version: str = None):
            proteins = SyntheticAdapter().download()
            proteins = RandomSplit()(proteins)
            return self.save(proteins, version)

The `.release()` method creates a new version of the dataset and defines what proteins and information will be contained in the dataset.
First, a set of proteins is downloaded through an `Adapter`.
The adapter provides an API to popular databases such as UniProt, PDB, and AlphaFold DB.
See their documentation for further options.
We will use a `MockAdapter` here which provides some randomly generated proteins.

.. tip::

    If your data is not accessible through the adapters provided by ProteinShake, see the developer guide on how to write your own adapter.

.. note::
    
    The return type of an adapter is always a `ProteinGenerator`. This is a standard python generator with some extended functionality, such as a `__len__` magic and additional meta info storage.

Then you can apply a series of `Modifier`s.
These are versatile in their function, but are mostly used to compute data splits, add annotations to proteins, or filter the protein set.
See a complete list in the documentation.

Once we are done with modifying the dataset we can save it and are done with the dataset!
To release your first version, just create an instance:

.. code:: python

    dataset = TestDataset()

This will automatically run the first release.


Custom Tasks
------------

A task is defined by a dataset, a prediction target, and a metric.
You can create a new task by defining these parameters:

.. code:: python

    from proteinshake.targets import AttributeTarget
    from proteinshake.metrics import AccuracyMetric

    class TestTask(Task):
        dataset = TestDataset()
        target = AttributeTarget("label")
        metrics = AccuracyMetric()

In this case, we take our `TestDataset` and apply an `AttributeTarget` to it.
Targets take a dataset and reshape it to define the prediction problem, i.e. they define the prediction target, and therefore mostly determine the type of task.
`AttributeTarget` specifically takes some attribute in the protein dictionary and sets it as the prediction target.

Lastly, we define some appropriate metrics (here accuracy) and we are done with the task!

You can now use your custom dataset and task just like any other ProteinShake task.