from rest_framework import status
from rest_framework.exceptions import APIException

from cash_flow.common.exceptions import ObjectDoesNotExist


class TransactionObjectDoesNotExist(ObjectDoesNotExist):
    pass


class TransactionCreationError(Exception):
    pass


class TransactionUpdateError(Exception):
    pass


class TransactionBadRequest(APIException):
    default_detail = "Bad Request while trying to create/update a new transaction"
    status_code = status.HTTP_400_BAD_REQUEST
