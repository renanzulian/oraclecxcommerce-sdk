from oraclecxcommerce.errors import OccAuthenticatorError
from requests import Session, ConnectionError
from time import time


class OccAuthenticator:
    def __init__(self, commerce_url: str, app_key: str) -> None:
        self._auth_session = Session()  # TODO: DEFAULT TIMEOUT AND RETRIES
        self._commerce_url = commerce_url
        self._app_key = app_key
        self._next_authentication: int
        self._pull_access()

    @property
    def session(self) -> Session:
        if not self._is_authenticated():
            self._pull_access()
        return self._auth_session

    def _is_authenticated(self) -> bool:
        if "Authorization" not in self._auth_session.headers.keys():
            return False
        return self._next_authentication - time() > 10

    def _pull_access(self) -> None:
        try:
            if "Authorization" not in self._auth_session.headers.keys():
                self._login()
            else:
                self._refresh_access()
        except OccAuthenticatorError as err:
            message_error = f'Unable to authenticate in OCC: {err}'
            raise OccAuthenticatorError(message_error)
        except ConnectionError as error:
            message_error = f'Connection error: {error}'
            raise OccAuthenticatorError(message_error)
        except TypeError as err:
            message_error = f'Type Error: {err}'
            raise OccAuthenticatorError(message_error)
        except KeyError as key:
            message_error = f'OCC did not return an elementary key: {key}.'
            raise OccAuthenticatorError(message_error)
        except Exception as error:
            message_error = f'Unexpected error: {error}'
            raise OccAuthenticatorError(message_error)

    def _login(self) -> None:
        response = self._auth_session.post(
            url=f'{self._commerce_url}/ccadmin/v1/login',
            data="grant_type=client_credentials",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {self._app_key}"},
        )
        if response.ok:
            occ_access = response.json()
            return self._pull_session(**occ_access)
        raise OccAuthenticatorError(
            f'Login receives {response.status_code} status code.\n'
            f'Body: {response.text}')

    def _refresh_access(self) -> None:
        response = self._auth_session.post(
            f'{self._commerce_url}/ccadmin/v1/refresh')
        if response.ok:
            occ_access = response.json()
            return self._pull_session(**occ_access)
        raise OccAuthenticatorError(
            f'Refresh token receives {response.status_code} status code.'
            f'\nBody: {response.text}')

    def _pull_session(self, **access_args) -> None:
        self._auth_session.headers.update(
            {"Authorization": f"Bearer {access_args['access_token']}"})
        self._next_authentication = time() + access_args['expires_in']
