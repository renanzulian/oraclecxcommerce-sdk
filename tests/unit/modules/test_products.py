from oraclecxcommerce.modules import ProductsModule
import pytest


def test_instantiate_products_module_class_without_authenticator_should_return_type_error():
    with pytest.raises(TypeError):
        ProductsModule()

