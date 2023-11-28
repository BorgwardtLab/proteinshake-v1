class PairwisePropertyTarget(Target):
    def __init__(self, attribute: str, resolution: str, metadata: Any) -> None:
        self.attribute = attribute 
        self.resolution = resolution
        self.metadata = metadata

    def __call__(self, entity_1, entity_2) -> int:
        return self.metadata[entity_1.ID][entity_2.ID]
    pass
