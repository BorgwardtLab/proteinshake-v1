from itertools import islice
import gzip, json, pickle, os
from pathlib import Path
import numpy as np


def save(obj, path):
    """Saves an object to either pickle, json, or json.gz (determined by the extension in the file name).

    Parameters
    ----------
    obj:
        The object to be saved.
    path:
        The path to save the object.
    """
    path = Path(path)
    os.makedirs(path.parents[0], exist_ok=True)
    if path.suffix == ".json.gz":
        with gzip.open(path, "w") as file:
            file.write(json.dumps(obj).encode("utf-8"))
    elif path.suffix == ".json":
        with open(path, "w") as file:
            json.dump(obj, file)
    elif path.suffix == ".npy":
        np.save(path, obj)
    else:
        with open(path, "wb") as file:
            pickle.dump(obj, file, protocol=pickle.HIGHEST_PROTOCOL)


def load(path):
    """Loads a pickle, json or json.gz file.

    Parameters
    ----------
    path:
        The path to be loaded.

    Returns
    -------
    object
        The loaded object.
    """
    path = Path(path)
    if path.suffix == ".json.gz":
        with gzip.open(path, "r") as file:
            obj = json.loads(file.read().decode("utf-8"))
    elif path.suffix == ".json":
        with open(path, "r") as file:
            obj = json.load(file)
    elif path.suffix == ".npy":
        obj = np.load(path)
    else:
        with open(path, "rb") as handle:
            obj = pickle.load(handle)
    return obj


def sharded(iterator, shard_size):
    while shard := list(islice(iterator, shard_size)):
        X, y = list(zip(*shard))
        yield np.asarray(X, dtype=object), np.asarray(y, dtype=object)


def save_shards(iterator, path):
    path = Path(path)
    for i, shard in enumerate(iterator):
        save(shard, path / f"{i}.pkl")
    save(np.arange(i), path / "index.npy")


def error(msg):
    raise "ERROR: " + msg


def warn(msg):
    print("WARNING:", msg)


def info(msg):
    print("INFO:", msg)
