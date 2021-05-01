from oraclecxcommerce import OracleCommerceCloud
import pytest


def test_instantiate_occ_class_should_return_not_implemented_error():
    with pytest.raises(NotImplementedError):
        OracleCommerceCloud()
