"""
Takes a dataset name as argument and creates a new version at the path specified in $PROTEINSHAKE_RELEASE_PATH.
"""

import argparse, importlib, os
from pathlib import Path

parser = argparse.ArgumentParser(
    prog="ProteinShake",
    description="Takes a dataset name as argument and creates a new version at the path specified in $PROTEINSHAKE_RELEASE_PATH.",
)
parser.add_argument("dataset", help="Name of the dataset")
args = parser.parse_args()

datasets = importlib.import_module("proteinshake.datasets")
Dataset = getattr(datasets, args.dataset)

Dataset(
    path=os.environ.get(
        "PROTEINSHAKE_RELEASE_PATH",
        Path.home() / ".proteinshake" / "datasets",
    )
)
