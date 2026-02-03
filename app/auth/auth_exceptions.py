class AuthError(Exception):
    """Base auth exception"""


class EmailAlreadyExists(AuthError):
    pass


class EmailNotFound(AuthError):
    pass


class InvalidPassword(AuthError):
    pass
