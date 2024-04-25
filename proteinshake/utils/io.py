from itertools import islice
import gzip, json, pickle, os
from pathlib import Path
import numpy as np
import time
import locale
from types import SimpleNamespace

LOCATIONS = SimpleNamespace(
    datasets=Path(
        os.environ.get(
            "PROTEINSHAKE_DATASET_ROOT",
            Path.home() / ".proteinshake" / "datasets",
        )
    ),
    raw=Path(
        os.environ.get(
            "PROTEINSHAKE_RAWDATA_ROOT",
            Path.home() / ".proteinshake" / "raw",
        )
    ),
    tasks=Path(
        os.environ.get(
            "PROTEINSHAKE_TASK_ROOT",
            Path.home() / ".proteinshake" / "tasks",
        )
    ),
    home=Path.home() / ".proteinshake",
)


def dict_to_avro_schema(data):
    """Guesses the avro schema from a dictionary.

    Parameters
    ----------
    example: dict
        A protein dictionary.

    Returns
    -------
    schema
        An avro schema.
    """
    typedict = {"int": "int", "float": "float", "str": "string", "bool": "boolean"}

    if isinstance(data, dict):
        fields = []
        for name, value in data.items():
            fields.append({"name": name, "type": dict_to_avro_schema(value)})
        return {"type": "record", "name": "Record", "fields": fields}
    elif isinstance(data, list):
        if len(data) > 0:
            return {"type": "array", "items": dict_to_avro_schema(data[0])}
        else:
            return {"type": "null"}
    elif type(data).__name__ in typedict:
        return {"type": typedict[type(data).__name__]}
    else:
        raise ValueError(f"Unsupported data type: {type(data)}")


class ProteinGenerator(object):
    def __init__(self, generator, length, assets={}):
        self.generator = generator
        self.length = length
        self.assets = assets

    def __len__(self):
        return self.length

    def __iter__(self):
        return self.generator

    def __next__(self):
        return next(self.generator)


def self_assign(func):
    """
    Decorator that assigns all arguments of __init__ to self.
    """

    def wrapper_init(self, *args, **kwargs):
        for name, value in zip(func.__code__.co_varnames[1:], args):
            setattr(self, name, value)
        for name, value in kwargs.items():
            setattr(self, name, value)
        if hasattr(func, "__self__"):
            func(self, *args, **kwargs)

    return wrapper_init


def current_date():
    lc = locale.setlocale(locale.LC_TIME)
    try:
        locale.setlocale(locale.LC_TIME, "C")
        return time.strftime("%Y%b%d").upper()
    finally:
        locale.setlocale(locale.LC_TIME, lc)


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
    save(np.arange(i + 1), path / "index.npy")


def error(msg):
    raise "ERROR: " + msg


def warn(msg):
    print("WARNING:", msg)


def info(msg):
    print("INFO:", msg)
