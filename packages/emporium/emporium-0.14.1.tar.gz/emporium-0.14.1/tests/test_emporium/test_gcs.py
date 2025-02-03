from emporium.implementations.gcs import RemoteStoreGCS


class TestRemoteStoreGCS:
    def test_substore_has_the_correct_path(self):
        store = RemoteStoreGCS("bucket", "a")
        substore = store.substore("b")
        expected = "https://storage.googleapis.com/storage/v1/b/bucket/o/a/b"
        assert expected == substore.location()

    def test_location_is_correctly_determined(self):
        store = RemoteStoreGCS("bucket", "a")
        expected = "https://storage.googleapis.com/storage/v1/b/bucket/o/a/b"
        assert expected == store.location("b")
