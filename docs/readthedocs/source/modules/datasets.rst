``datasets``
==========================


These classes define our currently supported datasets. See our :doc:`datasets tutorial<../notes/dataset>` for a quick intro to datasets, and :doc:`this tutorial<../notes/custom>` to learn how to create your own datasets.

.. currentmodule:: proteinshake.datasets

.. autosummary::
    :nosignatures:
    {% for cls in proteinshake.datasets.classes %}
      {{ cls }}
    {% endfor %}

.. automodule:: proteinshake.datasets
    :members:
    :exclude-members:
