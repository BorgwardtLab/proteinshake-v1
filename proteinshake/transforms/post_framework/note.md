"""
Post-framework transforms will not be implemented in ProteinShake, but are responsibility of the respective framework.
You can pass the framework-native transforms to the Dataset object though.

Example:

    from proteinshake.datasets import EnzymeDataset
    from torch_geometric.transforms import AddSelfLoops
    ds = EnzymeDataset(...).to_graph(...).pyg(..., post_transform=AddSelfLoops)

"""