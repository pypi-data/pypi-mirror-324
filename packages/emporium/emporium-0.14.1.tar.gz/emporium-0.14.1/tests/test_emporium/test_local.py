import pytest
from emporium.implementations.local import LocalStore


LOCATIONS = [
    ("/tmp", None, "/tmp"),
    ("/tmp", "foo", "/tmp/foo"),
    ("data", "foo", "data/foo"),
    (None, "foo", "foo"),
    ("data", "foo.yaml", "data/foo.yaml"),
    ("a/b/c/", "foo.yaml", "a/b/c/foo.yaml"),
]


class TestLocalStore:
    @pytest.mark.parametrize("base_path,path,location", LOCATIONS)
    def test_location_returns_correct_path(self, base_path, path, location):
        assert LocalStore(base_path).location(path) == location

    def test_location_is_nullary(self):
        assert LocalStore("/tmp").location() == "/tmp"

    def test_substore_returns_the_same_subclass(self):
        class CustomStore(LocalStore):
            pass

        actual = CustomStore("foo").substore("bar").__class__
        assert actual == CustomStore
