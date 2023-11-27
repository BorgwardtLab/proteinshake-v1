class PropertyTarget(Target):
    def __init__(self, attribute: str, resolution: str) -> None:
        self.attribute = attribute 
        self.resolution = resolution

    def __call__(self, entity):
        return entity[self.resolution][self.attribute]
    pass
