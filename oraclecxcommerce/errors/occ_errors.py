class OracleCXCommerceError(Exception):
    """Base class for exceptions in this SDK"""
    pass


class OccAuthenticatorError(OracleCXCommerceError):
    def __init__(self, message: str):
        super(message)
