from rest_framework import status
from rest_framework.exceptions import APIException

from cash_flow.common.exceptions import ObjectDoesNotExist


class CommentCreationError(Exception):
    pass


class CommentCreationBadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class CommentObjectDoesNotExist(ObjectDoesNotExist):
    pass
