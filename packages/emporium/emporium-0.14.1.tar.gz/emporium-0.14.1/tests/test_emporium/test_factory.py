import pytest
from mock import Mock

from emporium.implementations.local import LocalStore
from emporium.implementations.memory import InMemoryStore
from emporium.implementations.s3 import RemoteStoreS3
from emporium.implementations.gcs import RemoteStoreGCS
from emporium.factory import create_store


class TestCreateStore:
    def test_raise_value_error_when_no_key_type(self):
        with pytest.raises(ValueError):
            create_store({})

    def test_raise_value_error_when_invalid_type(self):
        with pytest.raises(ValueError):
            create_store({"type": "bogus"})

    @pytest.mark.parametrize(
        "cls,config",
        [
            (LocalStore, {"type": "local"}),
            (InMemoryStore, {"type": "memory"}),
            (RemoteStoreS3, {"type": "s3", "bucket": "bogus"}),
            (RemoteStoreGCS, {"type": "gcs", "bucket": "bogus"}),
        ],
    )
    def test_create_the_appropriate_store(self, cls, config):
        instance = create_store(config)
        assert isinstance(instance, cls), instance

    def test_parameter_extra_overrides_default_options(self):
        fn = Mock(return_value="X")
        config = {"type": "s3"}
        assert create_store(config, s3=fn) == "X"
