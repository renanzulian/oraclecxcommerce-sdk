from oraclecxcommerce.services import OccAuthenticator
import pytest


def test_instantiate_occ_authenticator_class_should_return_not_implemented_error():
    with pytest.raises(NotImplementedError):
        OccAuthenticator()
