import contextlib
import errno
import hashlib
import json
import os
import pickle
from datetime import datetime, time
from os.path import exists
from random import sample, seed
from typing import Any, Dict, List, Union

import urllib3
from cachetools import TTLCache

STORAGE = "/tmp/partyatmyhouse"
is_dev_env = True


def get_filename(file: str) -> str:
    return f"{STORAGE}/{file}"


def load_cache(file: str) -> Union[Dict[str, Any], None]:
    filename = get_filename(file)
    if exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return None


def write_cache(file: str, data: Dict[str, Any]) -> None:
    filename = get_filename(file)
    with open(filename, "w") as f:
        json.dump(data, f)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
cache_object = TTLCache(maxsize=10000, ttl=360)


def repeatable_sample(lst: List[Any], sample_size: int = 5) -> list:
    """Create a list sample of min(list,sample_size) from the list, have it be deterministic.
    The random.sample function below samples a list randomly.  For the hashing function
    below, we need it to be repeatable, otherwise the hash will change and caching would be
    impossible, since the hashing value is the'key' in the cache.

    Args:
        lst (List[Any]): [description]
        sample_size (int, optional): [description]. Defaults to 5.

    Returns:
        list: [description]
    """
    list_length = len(lst)

    # in case the sample size is larger than the list length
    sample_columns_size = min(list_length, sample_size)

    # set random state = ...
    seed(sample_columns_size + list_length + sample_size)

    # return sample_size length list
    return sample(lst, k=sample_columns_size)


def hashing_function(v: Any) -> str:
    """Hashing function.  Used by caching routines

    Args:
        v (Any): Any object

    Returns:
        str: Hash string
    """
    if isinstance(v, str):
        return v
    elif isinstance(v, (int, float)):
        return str(v)
    elif isinstance(v, (list, tuple, set)):
        return "".join([hashing_function(_v) for _v in repeatable_sample(v, sample_size=250)])
    elif isinstance(v, (datetime, time)):
        return str(v)
    else:
        return ""


def cacher(func) -> Any:
    """Decorator to cache functions.  Similar to lru_cache, but disk based and with custom hashing

    Args:
        func ([type]): function name decorated

    Returns:
        Any: Function output
    """

    def if_cache_else_func(*args, **kwargs):
        function_name = func.__name__
        values = [function_name, *list(kwargs.values())]
        values.extend(list(args))
        hashable_string = "".join([hashing_function(v) for v in values])
        status = "HIT"
        hash_key = hash_string(hashable_string)

        cache = None
        if hash_key in cache_object:
            print(f"CACHE {status} MEM {func.__name__}\t->\t{hash_key}")
            return cache_object[hash_key]

        if is_dev_env:
            filename = f"{STORAGE}/cache/{hash_key}"
            cache = read_cache_file(filename)
            if cache:
                cache_object[hash_key] = cache
                print(f"CACHE {status} DISK {func.__name__}\t->\t{hash_key}")
                return cache

        if cache is None and not os.path.exists(filename):
            status = "MISS"
            cache = func(*args, **kwargs)
            with contextlib.suppress(KeyError):
                cache_object[hash_key] = cache
                if is_dev_env:
                    write_cache_file(filename, cache)
        return cache

    return if_cache_else_func


def hash_string(text: str = None) -> str:
    """return hash of string
    Keyword Arguments:
        text {str} -- any string value (default: {None})
    Returns:
        str -- hash of the string passed in
    """
    if text is None:
        return None
    hash_object = hashlib.sha256(text.encode("utf-8"))
    return hash_object.hexdigest()


def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred


def read_cache_file(file: str = None, default=None, age_limit: int = 86400):
    """read file, parse as json, return

    Keyword Arguments:
        file {str} -- file w/ path (default: {None})
        default -- default return value of file is not found
        age_limit -- maximum age allowed for cache file

    Returns:
        dict|list -- json object
    """
    if file is None:
        return None

    if not os.path.exists(file):
        return default
        # if age of cache file is too old

    try:
        file_date = os.path.getmtime(file)
    except OSError as e:
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred
        return default

    if age_limit is not None and datetime.now().timestamp() - file_date > age_limit:
        silentremove(file)

    data = None
    try:
        with open(file, "rb") as a_file:
            data = pickle.load(a_file)
    except Exception:
        silentremove(file)
        return default

    return data


def write_cache_file(file: str, data: Any) -> None:
    """Write string to file

    Keyword Arguments:
        file {str} -- file w/ path (default: {None})
        data {?} -- string to be written (default: {None})
    """
    if not os.path.exists(os.path.dirname(file)):
        try:
            os.makedirs(os.path.dirname(file))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(file, "wb") as a_file:
        pickle.dump(data, a_file)
