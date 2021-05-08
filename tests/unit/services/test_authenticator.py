import requests

from oraclecxcommerce.services import OccAuthenticator
from oraclecxcommerce.errors import OccAuthenticatorError
from time import sleep
import pytest
import requests_mock


def test_instantiate_authenticator_with_invalid_credentials_should_return_an_error():
    invalid_url = "https://invalid-url-test.occa.ocs.oraclecloud.com"
    invalid_token = "WHAT1EVER2PASSWORD"
    with pytest.raises(OccAuthenticatorError):
        OccAuthenticator(invalid_url, invalid_token)


def test_instantiate_authenticator_should_login_with_valid_credentials():
    with requests_mock.Mocker() as mock:
        valid_url = "mock://valid-url-test.occa.ocs.oraclecloud.com"
        valid_token = "eyJhbGciOiJSUzI1NiIsSI6InA3OTA3OTE4YzYiLCJraWQiOiIwDVjWxsLCJ4NXUiOiJodHL3"
        response = {"access_token": "R4ND0M", "token_type": "bearer", "expires_in": 300}
        mock.post(f'{valid_url}/ccadmin/v1/login', json=response)

        authentication = OccAuthenticator(valid_url, valid_token)
        assert response['access_token'] in authentication.session.headers['Authorization']


def test_instantiate_authenticator_should_fail_if_occ_not_return_access_token():
    with requests_mock.Mocker() as mock:
        valid_url = "mock://valid-url-test.occa.ocs.oraclecloud.com"
        valid_token = "eyJhbGciOiJSUzI1NiIsSI6InA3OTA3OTE4YzYiLCJraWQiOiIwDVjWxsLCJ4NXUiOiJodHL3"
        response = {"token_type": "bearer", "expires_in": 300}
        mock.post(f'{valid_url}/ccadmin/v1/login', json=response)

        with pytest.raises(OccAuthenticatorError):
            OccAuthenticator(valid_url, valid_token)


def test_authenticator_should_refresh_token_rightly():
    with requests_mock.Mocker() as mock:
        valid_url = "mock://valid-url-test.occa.ocs.oraclecloud.com"
        valid_token = "eyJhbGciOiJSUzI1NiIsSI6InA3OTA3OTE4YzYiLCJraWQiOiIwDVjWxsLCJ4NXUiOiJodHL3"
        response_login = {"access_token": "R4ND0M", "token_type": "bearer", "expires_in": 11}
        response_refresh = {"access_token": "R4ND0M11", "token_type": "bearer", "expires_in": 11}
        mock.post(f'{valid_url}/ccadmin/v1/login', json=response_login)
        mock.post(f'{valid_url}/ccadmin/v1/refresh', json=response_refresh)

        authentication = OccAuthenticator(valid_url, valid_token)
        first_token = authentication.session.headers.get('Authorization')
        sleep(2)
        second_token = authentication.session.headers.get('Authorization')
        assert response_login.get("access_token") in first_token
        assert response_refresh.get("access_token") in second_token
        assert first_token != second_token
