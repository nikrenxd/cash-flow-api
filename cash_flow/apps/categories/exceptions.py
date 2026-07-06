from rest_framework import status
from rest_framework.exceptions import APIException

from cash_flow.common.exceptions import ObjectDoesNotExist


class CategoryCreationError(Exception):
    pass


class CategoryCreationBadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class CategoryObjectDoesNotExist(ObjectDoesNotExist):
    pass
