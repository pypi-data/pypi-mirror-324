class HubException(Exception):
    """The base exception for all Hub issues"""

    pass


class OrganizationException(HubException):
    """The base exception for all Hub Organization issues"""

    pass


class ClosedOrganizationRegistrationException(OrganizationException):
    """New organizations cannot be registered anymore"""

    pass


class DisabledOrganizationException(OrganizationException):
    """The requested organization has been disabled from the platform"""

    pass


class DuplicateOrganizationException(OrganizationException):
    """An organization with the same NGO Hub ID already exists"""

    pass


class MissingOrganizationException(OrganizationException):
    """The requested organization does not exist"""

    pass


class UserException(HubException):
    """The base exception for all Hub User issues"""

    pass


class MissingUserException(UserException):
    """The requested user does not exist"""

    pass


class HubHTTPException(HubException):
    """The base exception for all Hub HTTP/network issues"""

    def __init__(self, message: str, status_code: int, path: str, reason: str):
        self.message = message
        self.status_code = status_code
        self.path = path
        self.reason = reason

        super().__init__(message)


class HubBadRequestException(HubHTTPException):
    """The request was malformed"""

    def __init__(self, message: str, path: str):
        super().__init__(message, 400, path, "Bad request")


class HubDecodeException(HubHTTPException):
    """Failed to decode response"""

    def __init__(self, message: str):
        super().__init__(message, 500, "", "Internal server error")
