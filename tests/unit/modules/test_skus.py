from oraclecxcommerce.modules import SkusModule
import pytest


def test_instantiate_skus_module_class_should_return_not_implemented_error():
    with pytest.raises(NotImplementedError):
        occ = SkusModule()
