from rest_framework import status
from rest_framework.exceptions import APIException

from cash_flow.common.exceptions import ObjectDoesNotExist


class UserObjectDoesNotExist(ObjectDoesNotExist):
    pass


class UserActivationIdExpired(Exception):
    pass


class UserForActivationNotFound(Exception):
    pass


class UserIsAlreadyActive(Exception):
    pass


class UserIsAlreadyActivated(APIException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User is already active"


class UserActivationUrlIsInvalid(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid activation link"
