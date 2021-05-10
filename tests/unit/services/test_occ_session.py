from oraclecxcommerce.errors import OccAuthenticatorError
from oraclecxcommerce.services import OccSession
from requests import Response
import requests_mock
import pytest


def test_instantiate_authenticator_with_invalid_credentials_should_return_an_error():
    invalid_url = "https://invalid-url-test.occa.ocs.oraclecloud.com"
    invalid_token = "WHAT1EVER2PASSWORD"
    with pytest.raises(OccAuthenticatorError):
        OccSession(invalid_url, invalid_token)


def test_instantiate_with_valid_credentials_should_be_possible_to_request_with_a_get():
    with requests_mock.Mocker() as mock:
        valid_url = "https://valid-url-test.occa.ocs.oraclecloud.com"
        valid_token = "eyJhbGciOiJSUzI1NiIsSI6InA3OTA3OTE4YzYiLCJraWQiOiIwDVjWxsLCJ4NXUiOiJodHL3"
        response_login = {"access_token": "R4ND0M", "token_type": "bearer", "expires_in": 300}
        response_get = {"links": [], "data": [], }
        mock.post(f'{valid_url}/ccadmin/v1/login', json=response_login)
        mock.get(f'{valid_url}/ccadmin/v1/products', json=response_get)

        session = OccSession(valid_url, valid_token)
        response = session.get("/ccadmin/v1/products")
        assert type(response) == Response


def test_payload_login_occ_is_invalid_should_return_an_error():
    with requests_mock.Mocker() as mock:
        valid_url = "mock://valid-url-test.occa.ocs.oraclecloud.com"
        valid_token = "eyJhbGciOiJSUzI1NiIsSI6InA3OTA3OTE4YzYiLCJraWQiOiIwDVjWxsLCJ4NXUiOiJodHL3"
        response = {"token_type": "bearer", "expires_in": 300}
        mock.post(f'{valid_url}/ccadmin/v1/login', json=response)

        with pytest.raises(OccAuthenticatorError):
            OccSession(valid_url, valid_token)


def test_authenticator_should_refresh_token_rightly_and_be_possible_to_keep_getting_data():
    with requests_mock.Mocker() as mock:
        valid_url = "https://valid-url-test.occa.ocs.oraclecloud.com"
        valid_token = "eyJhbGciOiJSUzI1NiIsSI6InA3OTA3OTE4YzYiLCJraWQiOiIwDVjWxsLCJ4NXUiOiJodHL3"
        response_login = {"access_token": "R4ND0M", "token_type": "bearer", "expires_in": 0}
        response_refresh = {"access_token": "R4ND0M11", "token_type": "bearer", "expires_in": 11}
        response_get = {"links": [], "data": [], }
        mock.post(f'{valid_url}/ccadmin/v1/login', json=response_login)
        mock.post(f'{valid_url}/ccadmin/v1/refresh', json=response_refresh)
        mock.get(f'{valid_url}/ccadmin/v1/products', json=response_get)

        session = OccSession(valid_url, valid_token)
        first_response = session.get("/ccadmin/v1/products")
        second_response = session.get("/ccadmin/v1/products")
        assert type(first_response) is Response
        assert type(second_response) is Response
