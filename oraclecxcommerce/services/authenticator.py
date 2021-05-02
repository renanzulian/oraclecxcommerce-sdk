class OccAuthenticator:
    def __init__(self, commerce_url: str, app_key) -> None:
        if type(commerce_url) is not str:
            raise TypeError('Commerce url needs to be a str')
        if type(app_key) is not str:
            raise TypeError('App key needs to be a str')
        self._commerce_url = commerce_url
        self._app_key = app_key
