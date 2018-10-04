class UnknownLoginLocation(BaseException):
    """ Raised when login from a new device or IP"""

class BadCredentials(BaseException):
    """ Raised when username or password is incorrect"""