import os.path
from typing import Any, Callable, Iterable, Iterator, Mapping, Optional, TypeVar

T = TypeVar("T")


def nested_apply(nested_dict: Any, func: Callable[[Any], Any]) -> Any:
    """Apply a function to each element of nested_dict and return resulting dictionary."""
    if isinstance(nested_dict, Mapping):
        return {k: nested_apply(v, func) for k, v in nested_dict.items()}
    else:
        return func(nested_dict)


def not_none(obj: Optional[T]) -> T:
    """Check that obj is not None. Raises TypeError if it is.

    This is meant to help get code to type check that uses Optional types.

    """
    if obj is None:
        raise TypeError("object is unexpectedly None")
    return obj


def expand_env_var_in_dict(indict: dict[Any, Any]) -> dict[Any, Any]:
    out_dict = {}
    for key in indict.keys():
        if isinstance(indict[key], dict):
            out_dict[key] = expand_env_var_in_dict(indict[key])
        else:
            out_dict[key] = os.path.expandvars(indict[key])
    return out_dict


def is_last(iterable: Iterable[Any]) -> Iterator[tuple[Any, bool]]:
    """
    Utility function to iterate on collections and having the info if it is the last one or not
    in case you need to do something different on the last element

    Parameters
    ----------
    iterable : an iterable to iterate on

    Returns
    -------
    generate tuple of (item, is_last) on the iterable
    """
    iter_ = iter(iterable)
    try:
        nextitem = next(iter_)
    except StopIteration:
        pass
    else:
        item = nextitem
        while True:
            try:
                nextitem = next(iter_)
                yield item, False
            except StopIteration:
                yield nextitem, True
                break
            item = nextitem
