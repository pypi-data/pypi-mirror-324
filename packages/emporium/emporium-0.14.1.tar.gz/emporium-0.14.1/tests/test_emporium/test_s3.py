import pytest
from emporium.implementations.s3 import RemoteStoreS3


LOCATIONS = [
    ("test-bucket", None, None, None, "https://test-bucket.s3-eu-west-1.amazonaws.com"),
    (
        "test-bucket",
        "foo",
        None,
        None,
        "https://test-bucket.s3-eu-west-1.amazonaws.com/foo",
    ),
    (
        "test-bucket",
        "foo",
        None,
        "report.html",
        "https://test-bucket.s3-eu-west-1.amazonaws.com/foo/report.html",
    ),
    (
        "test-bucket",
        "foo",
        "www.example.com",
        "report.html",
        "https://www.example.com/foo/report.html",
    ),
    (
        "test-bucket",
        "foo",
        "www.example.com",
        "/bar/report.html",
        "https://www.example.com/foo/bar/report.html",
    ),
]


class TestRemoteS3Store:
    @pytest.mark.parametrize("bucket,prefix,domain,path,location", LOCATIONS)
    # pylint: disable=too-many-arguments
    def test_location_returns_correct_path(
        self, bucket, prefix, domain, path, location
    ):
        assert RemoteStoreS3(bucket, prefix, domain).location(path) == location

    def test_location_is_nullary(self):
        expected = "https://www.example.com"
        assert RemoteStoreS3("bucket", domain="www.example.com").location() == expected

    def test_substore_returns_the_same_subclass(self):
        class CustomStore(RemoteStoreS3):
            pass

        actual = CustomStore("foo").substore("bar").__class__
        assert actual == CustomStore
