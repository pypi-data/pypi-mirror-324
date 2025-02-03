from typing import Iterator

import pytest
from faker import Faker

from emporium import Entry, InMemoryStore, NoSuchFile, Store


@pytest.fixture
def store():
    return InMemoryStore()


@pytest.fixture
def faker():
    return Faker()


class TestInMemoryStore:
    @pytest.mark.parametrize("mode", ["w", "wt"])
    def test_handle_in_mode_wt_accepts_strings(self, mode, store):
        with store.open("test.txt", mode) as handle:
            try:
                handle.write("test")
            except TypeError:
                pytest.fail()

    @pytest.mark.parametrize("mode", ["w", "wt"])
    def test_handle_in_mode_wt_does_not_accept_bytes(self, mode, store):
        with store.open("test.txt", mode) as handle:
            with pytest.raises(TypeError):
                handle.write(b"test")

    def test_handle_in_mode_wb_accepts_bytes(self, store):
        with store.open("test.txt", "wb") as handle:
            try:
                handle.write(b"test")
            except TypeError:
                pytest.fail()

    def test_handle_in_mode_wv_does_not_accept_strings(self, store):
        with store.open("test.txt", "wb") as handle:
            with pytest.raises(TypeError):
                handle.write("test")

    def test_read_in_mode_b_returns_written_bytes(self, store):
        with store.open("test.txt", "wb") as handle:
            handle.write(b"test")
        with store.open("test.txt", "rb") as handle:
            assert handle.read() == b"test"

    def test_read_in_mode_b_return_written_string_as_utf8_bytes(self, store):
        with store.open("test.txt", "w") as handle:
            handle.write("test")
        with store.open("test.txt", "rb") as handle:
            assert handle.read() == "test".encode("utf-8")

    def test_read_raises_file_not_found_error(self, store):
        with pytest.raises(NoSuchFile):
            with store.open("bogus", "r"):
                pass

    def test_read_in_mode_t_returns_string(self, store):
        with store.open("test.txt", "w") as handle:
            handle.write("test")
        with store.open("test.txt", "r") as handle:
            assert handle.read() == "test"

    def test_files_accessible_via_substore(self, store):
        with store.open("prefix/test.txt", "w") as handle:
            handle.write("test")
        substore = store.substore("prefix/")
        with substore.open("test.txt", "r") as handle:
            assert handle.read() == "test"

    def test_files_accessible_via_parent_store(self, store):
        substore = store.substore("prefix/")
        with substore.open("test.txt", "w") as handle:
            handle.write("test")
        with store.open("prefix/test.txt", "r") as handle:
            assert handle.read() == "test"

    def test_substore_returns_the_same_subclass(self):
        class CustomStore(InMemoryStore):
            pass

        actual = CustomStore("foo").substore("bar").__class__
        assert actual == CustomStore

    def test_removing_non_existent_file_throws(self, store):
        with pytest.raises(NoSuchFile):
            store.remove("bogus")

    def test_removing_deletes_file(self, store):
        with store.open("test.txt", "w") as handle:
            handle.write("test")
        assert [Entry("test.txt", "file")] == list(store.list())
        store.remove("test.txt")
        assert [] == list(store.list())

    def test_clear_removes_all_files(self, store: Store, faker: Faker):
        names = [faker.file_name() for _ in range(10)]
        for name in names:
            with store.open(name, "w") as handle:
                handle.write(name)
        assert set(names) == set(entry.entry for entry in store.list())
        store.clear()
        assert [] == list(store.list())

    def test_clear_removes_only_files_in_substore(self, store: Store, faker: Faker):
        root_file_names = self._store_files(store, 10, faker)
        substore = store.substore("prefix/")
        substore_file_names = self._store_files(substore, 10, faker)
        assert set(substore_file_names) == set(self._get_file_names(substore))

        substore.clear()

        assert not set(self._get_file_names(substore))
        assert set(root_file_names) == set(self._get_file_names(store))

    def test_clear_also_removes_files_in_substore(self, store: Store, faker: Faker):
        root_file_names = self._store_files(store, 10, faker)
        substore = store.substore("prefix/")
        substore_file_names = self._store_files(substore, 10, faker)
        assert set(root_file_names) == set(self._get_file_names(store))
        assert set(["prefix"]) == set(self._get_dir_names(store))

        store.clear()

        assert not set(self._get_file_names(store))
        assert not set(self._get_file_names(substore))
        assert not set(self._get_dir_names(store))

    def _store_files(self, store: Store, n: int, faker: Faker) -> list[str]:
        names = [faker.file_name() for _ in range(n)]
        for name in names:
            with store.open(name, "w") as handle:
                handle.write(name)
        return names

    def _get_file_names(self, store: Store) -> Iterator[str]:
        for entry in store.list():
            if entry.entry_type == "file":
                yield entry.entry

    def _get_dir_names(self, store: Store) -> Iterator[str]:
        for entry in store.list():
            if entry.entry_type == "directory":
                yield entry.entry
