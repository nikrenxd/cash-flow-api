from rest_framework import status
from rest_framework.exceptions import APIException

from src.cash_flow.common.exceptions import ObjectDoesNotExist


class CommentActionFailed(Exception):
    pass


class CommentCreationFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class CommentUpdateFailed(CommentCreationFailed):
    pass


class CommentObjectDoesNotExist(ObjectDoesNotExist):
    pass
