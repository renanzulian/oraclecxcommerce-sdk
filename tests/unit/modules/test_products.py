from oraclecxcommerce.modules import ProductsModule
import pytest


def test_instantiate_products_module_class_should_return_not_implemented_error():
    with pytest.raises(NotImplementedError):
        occ = ProductsModule()
