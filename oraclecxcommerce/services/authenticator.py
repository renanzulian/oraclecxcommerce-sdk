from oraclecxcommerce.errors import OccAuthenticatorError
from requests import Session, request
from time import time


class OccAuthenticator:
    def __init__(self, commerce_url: str, app_key: str) -> None:
        self._auth_session = Session()  # TODO: DEFAULT TIMEOUT AND RETRIES
        self._commerce_url = commerce_url
        self._app_key = app_key
        self._access_token: str
        self._next_authentication: int
        self._get_occ_access()

    @property
    def access_token(self) -> str:
        if not self._is_authenticated():
            self._get_occ_access()
        return self._access_token

    def _is_authenticated(self) -> bool:
        if not self._access_token:
            return False
        return self._next_authentication - time() > 10

    def _get_occ_access(self) -> None:
        try:
            if not self._access_token:
                self._login()
            else:
                self._refresh_access()
        except TypeError as error:
            print(error)
            # TODO: MELHORAR O TRATAMENTO DE ERROS
            # raise InvalidOccCredentialsError('Unexpected error')
        except KeyError as error:
            print(error)
            # TODO: MELHORAR O TRATAMENTO DE ERROS
            # raise InvalidOccCredentialsError('Unexpected error')
        except Exception as error:
            print(error)
            # TODO: MELHORAR O TRATAMENTO DE ERROS
            raise OccAuthenticatorError('Unexpected error')

    def _login(self) -> None:
        response = self._auth_session.post(
            url=f'{self._commerce_url}/ccadmin/v1/login',
            data="grant_type=client_credentials",
            headers={"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Bearer {self._app_key}"},
        )
        if response.ok:
            occ_access = response.json()
            return self._pull_access(**occ_access)
        raise OccAuthenticatorError(f'Login receives {response.status_code} status code.\n'
                                    f'Body: {response.text}')

    def _refresh_access(self) -> None:
        response = self._auth_session.post(
            url=f'{self._commerce_url}/ccadmin/v1/refresh',
            headers={"Authorization": f"Bearer {self._access_token}"},
        )
        if response.ok:
            occ_access = response.json()
            return self._pull_access(**occ_access)
        raise OccAuthenticatorError(f'Refresh token receives {response.status_code} status code.'
                                    f'\nBody: {response.text}')

    def _pull_access(self, **access_args) -> None:
        self._access_token = access_args['access_token']
        self._next_authentication = time() + access_args['expires_in']

