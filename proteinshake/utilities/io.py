from itertools import islice
import gzip, json, pickle, os
from pathlib import Path
import numpy as np
import time
import locale
from fastavro import parse_schema as parse_avro_schema


def avro_schema_from_example(example):
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

    def field_spec(k, v):
        if type(v) == dict:
            return {
                "name": k,
                "type": {
                    "name": k,
                    "type": "record",
                    "fields": [field_spec(_k, _v) for _k, _v in v.items()],
                },
            }
        elif type(v) == list:
            return {
                "name": k,
                "type": {
                    "type": "array",
                    "items": typedict[type(v[0]).__name__] if len(v) > 0 else "string",
                },
            }
        elif type(v).__name__ in typedict:
            return {"name": k, "type": typedict[type(v).__name__]}
        else:
            raise TypeError(
                f"All fields in a protein object need to be either int, float, bool or string, not {type(v).__name__}"
            )

    schema = {
        "name": "Protein",
        "namespace": "Dataset",
        "type": "record",
        "fields": [field_spec(k, v) for k, v in example.items()],
    }
    return parse_avro_schema(schema)


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
        return self

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
    save(np.arange(i), path / "index.npy")


def error(msg):
    raise "ERROR: " + msg


def warn(msg):
    print("WARNING:", msg)


def info(msg):
    print("INFO:", msg)
