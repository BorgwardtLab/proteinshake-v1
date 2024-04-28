Quickstart
==========

ProteinShake provides a broad range of prediction tasks in protein biology. The tasks provide everything from data to evaluation, and can be used with most popular deep learning models and frameworks. 

.. tip::

  Click on your favorite representation/framework below to see how to use ProteinShake with your model.

.. code:: python
  
  from proteinshake.tasks import EnzymeClassificationTask
  from proteinshake.mocks import MockModel

  # Use proteins with enzyme class annotations
  # Convert them to point clouds
  # Load into PyTorch data structures
  task = EnzymeClassificationTask().to_point().torch()

  # Replace this with your own model
  model = MockModel(output_shape=task.output_shape)

  # Train using native data loaders
  for X,y in task.train_loader():
      model.train_step(X) # your model training goes here

  # Evaluation with the provided metrics
  for X,y in task.test_loader():
      prediction = model.test_step(X)
      metrics = task.evaluate(y, prediction)
      print(metrics)