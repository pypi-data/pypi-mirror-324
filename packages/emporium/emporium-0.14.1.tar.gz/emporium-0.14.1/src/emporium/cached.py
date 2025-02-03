from contextlib import contextmanager
from typing import Iterator

from typing_extensions import Self

from emporium.base import Entry, Store
from emporium.utils import is_read_mode, is_write_mode


class Cached(Store):
    def __init__(self, origin: Store, cache: Store):
        self._origin = origin
        self._cache = cache

    @contextmanager
    # pylint: disable=inconsistent-return-statements
    def open(self, path, mode, *args, **kwargs):
        if is_write_mode(mode):
            with self._origin.open(path, mode, *args, **kwargs) as h:
                yield h
            return

        if is_read_mode(mode):
            try:
                with self._cache.open(path, mode, *args, **kwargs) as h:
                    yield h
            except Exception:  # pylint: disable=broad-except; TODO
                with self._origin.open(path, mode, *args, **kwargs) as origin:
                    write_mode = "w" + mode[1:]
                    with self._cache.open(path, write_mode) as cache:
                        for line in origin:
                            cache.write(line)
                    origin.seek(0)
                    yield origin

    def substore(self, path) -> Self:
        return self.__class__(self._origin.substore(path), self._cache.substore(path))  # type: ignore

    def location(self, path=None) -> str:
        return self._origin.location(path)

    def list(self, path=None) -> Iterator[Entry]:
        return self._origin.list(path)

    def remove(self, path: str) -> None:
        self._origin.remove(path)
        self._cache.remove(path)
