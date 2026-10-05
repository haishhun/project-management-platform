class ApplicationException(Exception):
    pass


class DatabaseUnavailableException(ApplicationException):
    pass


class ResourceDoesNotExistException(ApplicationException):
    pass


class InvalidRequestException(ApplicationException):
    pass


class UnauthorizedException(ApplicationException):
    pass


class ForbiddenException(ApplicationException):
    pass
