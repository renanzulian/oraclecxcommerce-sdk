from oraclecxcommerce.modules import OrdersModule
import pytest


def test_instantiate_orders_module_class_should_return_not_implemented_error():
    with pytest.raises(NotImplementedError):
        occ = OrdersModule()
