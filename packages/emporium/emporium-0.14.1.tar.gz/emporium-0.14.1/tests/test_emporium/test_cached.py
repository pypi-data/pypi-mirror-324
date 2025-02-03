import pytest
from mock import Mock

from emporium import Cached, InMemoryStore, NoSuchFile


@pytest.fixture
def origin():
    return Mock(wraps=InMemoryStore())


@pytest.fixture
def cache():
    return InMemoryStore()


@pytest.fixture
def store(origin, cache):
    return Cached(origin, cache)


class TestCached:
    def test_write_only_touches_origin(self, origin, cache, store):
        with store.write("test.txt") as h:
            h.write("test")

        with origin.read("test.txt") as h:
            assert h.read() == "test"

        with pytest.raises(NoSuchFile):
            with cache.read("test.txt") as h:
                pass

    def test_read_adds_to_cache(self, cache, store):
        with store.write("test.txt") as h:
            h.write("test")

        with store.read("test.txt") as h:
            h.read()

        with cache.read("test.txt") as h:
            assert h.read() == "test"

    def test_second_read_does_not_touch_origin(self, origin, store):
        with store.write("test.txt") as h:
            h.write("test")

        with store.read("test.txt") as h:
            h.read()

        before = origin.open.call_count

        with store.read("test.txt") as h:
            h.read()

        assert before == origin.open.call_count
