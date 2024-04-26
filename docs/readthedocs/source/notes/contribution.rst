How to contribute
=================

We welcome any contributions (new tasks and datasets, features, or bug reports) through pull requests (PR) on the project `GitHub repository <https://github.com/BorgwardtLab/proteinshake-v1>`_.

We maintain a growing list of features to be implemented in the `repository issues <https://github.com/BorgwardtLab/proteinshake-v1/issues>`_. Feel free to assign yourself to one and then open a pull request linking the issue.

You can also implement your own features. It is a good idea in this case to open an issue beforehand to discuss if your proposed feature would benefit ProteinShake.

After a review we will merge your pull request.
Your dataset/task will be processed on our server with the next release, and the pre-processed data will be available for download.

Please also consider the contribution guidelines below.
If you have questions on how to contribute, please feel free to open an issue on GitHub or contact any of the authors.

.. tip::
    See the :doc:`Tutorial<custom>` for an example on how to build custom datasets and tasks. For more advanced features, see :doc:`Tutorial<developer>` for detailed information on the software organization and how to implement your own frameworks, representations and transforms.

Contribution guidelines
-----------------------

We try to maintain a performant implementation for everyone, covering as many features and applications as we can. For this community effort to work smoothly, we will enforce a few good practices of coding and research. The submitted feature needs to fulfill the following requirements in order to be merged.

General coding guidelines:
^^^^^^^^^^^^^^^^^^^^^^^^^^

- We follow Black formatting. It's best to install an extension for your editor.
- Use `typing` for your class and function signatures.
- Provide a docstring for every class or function. The online documentation will automatically build from these. Our documentation system uses `Sphinx <https://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html>`_ with the `awesome-sphinx theme <https://sphinxawesome.xyz/>`_, see their documentation for format instructions.
- Performance is key. Especially transforms are called very often during training, and it is crucial that execution time is minimized. Avoid for-loops and vectorize as much as you can.
- Every piece of code needs a test case. Our testing pipeline covers most modules automatically, see the coverage report when you open a PR. Ideally, a PR should not decrease the coverage.

Good scientific practice:
^^^^^^^^^^^^^^^^^^^^^^^^^
- One of the core motivations for ProteinShake is to provide transparent and reproducible code. We will only merge code that is comprehensible can be reproduced on our release servers (e.g. avoid using locally saved raw data and host it instead).
- If you provide a new dataset, try to clean it as much as you can, and avoid potential biases.
- If you provide a new task, make sure you choose appropriate metrics and splits.
- Respect other people's rights, especially if you consider to upload patient related data.
- Attribute appropriately. We require that you provide paper references and licenses for every dataset or task. Make sure they comply with our BSD-3/CC-BY-4.0 licensing policy.
    

