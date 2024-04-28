User guide
==========

The central object in ProteinShake is the `Task`.
It provides data and metrics to train and evaluate your model.
Let's start with the example from the Quickstart.

.. note::

    For this tutorial, we will work with the `PyG` framework and the `graph` representation, but feel free to replace them with your preferred setup.

.. code:: python

    from proteinshake.tasks import EnzymeClassificationTask
    from proteinshake.mocks import MockModel

    task = EnzymeClassificationTask().to_graph(eps=8).pyg()

    model = MockModel(output_shape=task.output_shape)

    for X,y in task.train_loader():
        model.train_step(X)

    for X,y in task.test_loader():
        prediction = model.test_step(X)
        metrics = task.evaluate(y, prediction)
        print(metrics)

All available tasks can be found in the `proteinshake.tasks` submodule.
See the documentation for an extensive list.

ProteinShake also provides some useful mock classes for testing purposes, we will make use of the `MockModel` here, which simulates a trainable deep learning model.
Replace this with your own model if you like.

Transforms
----------

The most important line is the instantiation of the task.
Here we provide all necessary information by chaining a `Representation` and a `Framework`, which will take the protein and convert it to a machine-readable representation (such as a point cloud or a graph) and prepare it for your deep learning framework of choice (in this case PyTorch).

Calling `.to_graph(eps=9).pyg()` is actually just syntactic sugar for:

.. code:: python

    from proteinshake.representations import GraphRepresentation
    from proteinshake.frameworks import PygFramework

    task = EnzymeClassificationTask().transform(
        GraphRepresentation(eps=8),
        PygFramework(),
    )

where `GraphRepresentation` and `PygFramework` are so-called transforms.
This is the core concept of how ProteinShake handles data:
The task is build on a dataset of proteins which are initially represented as a list of dictionaries with all the protein information stored in key-value pairs.
You then define a series of transforms which will manipulate and shape the data, until you eventually receive a tensor that you can feed to your model.

The `GraphRepresentation` transform for example takes a protein dictionary and builds a graph from it, which is now represented as an adjacency matrix and a node feature tensor.
This is followed by the `PygFramework` transform which takes the graph representation and converts it to a native `torch_geometric.data.Data` object.

You can further extend the transforms with all kinds of useful manipulations (see the documentation for an extensive list). For example, let's reduce the protein from atom resolution to residue resolution and add self-loops to the graph:


.. code:: python

    from proteinshake.frameworks import ResidueTransform
    from torch_geometric.transforms import AddSelfLoops

    task = EnzymeClassificationTask().transform(
        ResidueTransform(),
        GraphRepresentation(eps=8),
        PygFramework(),
        AddSelfLoops(),
    )

We even used a transform from another python package here!
You can mix and match transforms from ProteinShake and your preferred framework.
As you probably already realized, the order of the transform matters.
For example, the `AddSelfLoops` transform from PyG expects a PyG data object, and as such needs to be applied after `PygFramework`.
Check the documentation of the respective transform to see if they need to be applied before or after the representation or framework transform.

.. tip::

    Transforms are applied every time a protein is accessed through the dataloader. ProteinShake optimizes the transforms under the hood and writes them to disk after the first iteration. However, transforms with a random element (e.g. masking) cannot be precomputed as they change at every iteration. This also affects all transforms that come after it, so use them sparingly to avoid performance issues.

The code above can also be written using the chaining syntax.
Here, `pre_transform` and `post_transform` determine the transformation order.

.. code:: python

    from proteinshake.frameworks import ResidueTransform
    from torch_geometric.transforms import AddSelfLoops

    task = EnzymeClassificationTask().to_graph(eps=8,
            pre_transform=[ResidueTransform()]
        ).pyg(
            post_transform=[AddSelfLoops()]
        )

As your pipeline gets more complex, it is advisable though to use the `.transform()` syntax from above for readability.

Data loading
------------

Defining transforms is most of the work. ProteinShake then conveniently provides your transformed data through native dataloaders of your framework.
Just call `.train_dataloader()` or `.val_dataloader()` or `.test_dataloader()`.

Evaluation
----------

Evaluation is just as easy. Appropriate metrics are predefined, and you only need to provide ground-truth and predictions to the `.evaluate()` method of the task.