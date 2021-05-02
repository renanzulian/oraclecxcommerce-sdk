from oraclecxcommerce.services import OccAuthenticator
from oraclecxcommerce.errors import InvalidOccCredentialsError
import pytest
import requests_mock


def test_instantiate_occ_authenticator_without_credentials_should_return_a_type_error():
    with pytest.raises(TypeError):
        OccAuthenticator()


@requests_mock.Mocker()
def test_instantiate_occ_authenticator_with_invalid_store_url_and_app_token_should_return_error(mock):
    invalid_url = "https://valid-url-test.occa.ocs.oraclecloud.com"
    invalid_token = "eyJhbGciOiJSUzI1NiIsSI6InA3OTA3OTE4YzYiLCJraWQiOiIwDVjWxsLCJ4NXUiOiJodHL3"
    mock.get(invalid_url, status_code=200)
    with pytest.raises(InvalidOccCredentialsError):
        OccAuthenticator(invalid_url, invalid_token)
