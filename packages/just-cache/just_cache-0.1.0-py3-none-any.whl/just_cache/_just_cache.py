import pickle
from collections.abc import Callable
from pathlib import Path
from typing import Any, BinaryIO, Final, TypeVar

T = TypeVar("T")


class Cache:
    """
    The caching object.

    Parameters
    ----------
    cache_dir
        The directory of the cache files. If given, then the cache paths will be considered relative to this directory.
    disabled
        If True, then the cache will behave as if there was no hit.
    """

    def __init__(self, cache_dir: Path | str | None = None, disabled: bool = False):
        if isinstance(cache_dir, str):
            cache_dir = Path(cache_dir)

        self.cache_dir = cache_dir
        self.disabled = disabled

    def cached(
        self,
        pkl: Path | str,
        x: Callable[[], T],
        /,
        depends: Any | None = None,
        disabled: bool = False,
    ) -> T:
        """
        Load the pre-calculated result from a pickle-based cache if a cache exists and the dependencies did not change.

        Since this cache is pickle-based, the cache should only be used for TRUSTED DATA. Deserialization of untrusted data can lead to ARBITRARY CODE EXECUTION.

        Parameters
        ----------
        pkl
            The pickle file to use.
        x
            The lambda function that creates the object if the cache does not exist.
        depends
            The values on which the cache depends.
        disabled
            If true, then this cache is disabled. If it is set to false, but the while cache object is disabled, then this cache will also be disabled regardless.

        Returns
        -------
        v
            The value.
        """
        if isinstance(pkl, str):
            pkl = Path(pkl)

        if self.cache_dir is not None:
            total_path = self.cache_dir / pkl
        else:
            total_path = pkl

        total_path.parent.mkdir(exist_ok=True, parents=True)

        if total_path.exists() and (not self.disabled) and (not disabled):
            with total_path.open("rb") as f:
                loaded_dict = pickle.load(f)
                if depends == loaded_dict["depends"]:
                    return loaded_dict["obj"]

        data = x()
        with total_path.open("wb") as f:
            pickle.dump({"depends": depends, "obj": data}, f)
        return data
