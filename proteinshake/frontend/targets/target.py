class Target:
    """ Returns the attribute to predict for a single instance, given arbitrary inputs.
    Different tasks will have target computations on different types and numbers of entitites.
    """
    def __call__(self, protein: proteinshake.Entity) ->  Any:
        pass
    pass
