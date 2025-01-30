from starlette import status
from starlette.exceptions import HTTPException

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)


class FastAuthException(ValueError):
    pass


class CredentialsException(FastAuthException):

    descriptor = "credentials"

    def __init__(self):
        super().__init__(f"Invalid {self.descriptor}")
        raise credentials_exception from self


class UserNotFound(CredentialsException):
    descriptor = "username"


class InvalidPassword(CredentialsException):
    descriptor = "password"


class DatabaseError(FastAuthException):
    pass
