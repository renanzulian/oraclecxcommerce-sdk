from oraclecxcommerce.modules import ProductsModule
import requests_mock
import pytest


def test_instantiate_products_module_class_without_authenticator_should_return_type_error():
    with pytest.raises(TypeError):
        ProductsModule()


def test_list_products_without_arguments_should_return_default_fields():
    with requests_mock.Mocker() as mock:
        valid_url = "https://valid-url-test.occa.ocs.oraclecloud.com"
        valid_token = "eyJhbGciOiJSUzI1NiIsSI6InA3OTA3OTE4YzYiLCJiIwDVjWxsLCJ4NXUiOiJodHL3"
        response_login = {"access_token": "R4ND0M", "token_type": "bearer", "expires_in": 300}
        response_get = {"links": [], "items": [
            {
                "displayName": "Bolo DaquelaMarca",
                "description": "Bolo DaquelaMarca - Fresco",
                "id": "3",
                "brand": "DaquelaMarca",
                "childSKUs": [
                    {
                        "displayName": "Laranja",
                        "barcode": None,
                        "quantity": 15,
                        "salePrice": None,
                        "active": True,
                        "repositoryId": "5",
                        "listPrice": None
                    }
                ],
                "route": "/bolo-daquelamarca/product/3",
                "listPrice": None,
                "salePrice": None,
                "active": True,
            }
        ], }
        mock.post(f'{valid_url}/ccadmin/v1/login', json=response_login)
        mock.get(f'{valid_url}/ccadmin/v1/products', json=response_get)