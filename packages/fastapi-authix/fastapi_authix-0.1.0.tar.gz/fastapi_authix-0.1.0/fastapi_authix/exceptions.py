class AuthixError(Exception):
    pass


class SerializeError(AuthixError):
    pass


class InvalidMode(SerializeError):
    pass


class UnknownObject(SerializeError):
    pass


class AccessDenied(AuthixError):
    pass
