## Filestructure:

- **backend:** Collects and processes raw pdb files from various databases. Creates Collections.

   - **adapters:** Database adapters to PDB, AFDB, etc.

   - **protein:** The protein object specification.

   - **collection:** A set of protein objects.

   - **database:** Unifying database mirror that allows query access to create a collection.

- **frontend:** High level specifications for datasets and tasks.

   - **datasets:** Load a collection and apply transforms.

   - **tasks:** Various ML prediction problems. Takes a dataset and rearranges the data (sklearn-style X_train, y_train, ...) such that it can be fed to the model (X) and evaluated (y).

   - **evaluators:** Groups relevant metrics for a given class of problems (e.g. classification or regression).

   - **splitters:** Takes a dataset and generates split indices, either from the data/labels itself or from other resources.

- **datasets:** Some relevant collections of proteins, for preprocessed hosting. Each dataset covers some biological topic.

- **tasks:** The actually implemented biological tasks for the end-user, consisting of a frontend.task in combination with a specific dataset.

- **transforms:** Various functions to transform proteins, representations, and frameworks.
