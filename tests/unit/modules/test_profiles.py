from oraclecxcommerce.modules import ProfilesModule
import pytest


def test_instantiate_profile_module_class_should_return_not_implemented_error():
    with pytest.raises(NotImplementedError):
        occ = ProfilesModule()
