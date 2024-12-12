from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    success = False
    errors = None
    key = ""

    def __init__(self, detail, code, key="", errors=None):
        super().__init__(detail, code)
        self.status_code = code
        self.success = False
        self.key = key
        self.errors = errors


class UserAlreadyExistsException(BaseCustomException, IntegrityError):
    def __init__(self, message="User with this username or email already exists.", key="user_exists", errors=None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, key=key, errors=errors)


class InvalidEmailException(BaseCustomException):
    def __init__(self, message="Invalid email address provided.", key="invalid_email", errors=None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, key=key, errors=errors)


class UserNotFoundException(BaseCustomException):
    def __init__(self, message="User not found.", key="user_not_found", errors=None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, key=key, errors=errors)


class DatabaseIntegrityException(BaseCustomException):
    def __init__(self, message="Database integrity error occurred.", key="db_integrity_error", errors=None):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR, key=key, errors=errors)


class ValidationErrorException(BaseCustomException, ValidationError):
    def __init__(self, message="Validation failed for user input.", key="validation_error", errors=None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, key=key, errors=errors)


class AuthenticationErrorException(BaseCustomException):
    def __init__(self, message="Authentication failed.", key="authentication_error", errors=None):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, key=key, errors=errors)














class EntityNotFoundException(BaseCustomException):
    def __init__(self, message="Entity Not Found!", key="not_found", errors=None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, key=key, errors=errors)




class UserIntegrityError(BaseCustomException):
    def __init__(self, message="Entity Not Found!", key="not_found", errors=None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, key=key, errors=errors)


class MultipleObjectsReturnedException(BaseCustomException):
    def __init__(
        self,
        message="Multiple Objects Returned!",
        key="multiple_objects_returned",
        errors=None,
    ):
        super().__init__(
            message, status.HTTP_500_INTERNAL_SERVER_ERROR, key=key, errors=errors
        )


class EntityDeleteRestrictedException(BaseCustomException):
    def __init__(
        self,
        message="Entity Deletion Restricted!",
        key="delete_restricted",
        errors=None,
    ):
        super().__init__(message, status.HTTP_409_CONFLICT, key=key, errors=errors)


class EntityDeleteProtectedException(BaseCustomException):
    def __init__(
        self, message="Entity Deletion Protected!", key="delete_protected", errors=None
    ):
        super().__init__(message, status.HTTP_409_CONFLICT, key=key, errors=errors)


class CaptchaTokenInvalidException(BaseCustomException):
    def __init__(
        self,
        message="Captcha Token is Invalid!",
        key="captcha_token_invalid",
        errors=None,
    ):
        super().__init__(message, status.HTTP_403_FORBIDDEN, key=key, errors=errors)


class ValidationException(BaseCustomException):
    def __init__(
        self, message="Validation Error!", key="validation_error", errors=None
    ):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, key=key, errors=errors)


class InvalidTokenException(BaseCustomException):
    def __init__(self, message="Token is Invalid!", key="invalid_token", errors=None):
        super().__init__(message, status.HTTP_403_FORBIDDEN, key=key, errors=errors)


class InvalidIdException(BaseCustomException):
    def __init__(self, message="id is Invalid!", key="invalid_id", errors=None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, key=key, errors=errors)


class PasswordMissmatchException(BaseCustomException):
    def __init__(
        self, message="Password Missmatch!", key="password_missmatch", errors=None
    ):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, key=key, errors=errors)


class UserNotBannedException(BaseCustomException):
    def __init__(
        self, message="User is Not Banned", key="user_not_banned", errors=None
    ):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, key=key, errors=errors)


class UserIsNotActiveException(BaseCustomException):
    def __init__(
        self, message="User is Not Active", key="user_not_active", errors=None
    ):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, key=key, errors=errors)


class CastDtoException(BaseCustomException):
    def __init__(self, message="Cast Dto Error", key="cast_dto_error", errors=None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, key=key, errors=errors)
