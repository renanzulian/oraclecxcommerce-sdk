class OracleCXCommerceError(Exception):
    """Base class for exceptions in this SDK"""
    pass


class InvalidOccCredentialsError(OracleCXCommerceError):
    def __init__(self, message: str = None):
        if message is not None:
            self.message = message
        else:
            self.message = "Invalid Oracle Commerce Cloud credentials"
