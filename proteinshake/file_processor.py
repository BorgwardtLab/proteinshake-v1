class FileProcessor:
    """
    Converts a pdb/mmcif file to a more efficient Atoms & Residue format. Implements QC.
    Applies transforms to clean and polish the structure, e.g. energy minimization.
    Also computes and annotates quality scores which can be used for later filtering.
    """

    def __init__(self) -> None:
        pass
