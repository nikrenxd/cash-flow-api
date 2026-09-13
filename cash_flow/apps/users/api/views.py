import logging

from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from cash_flow.apps.users.api.serializers import (
    UserCreateSerializer,
)
from cash_flow.apps.users.exceptions import (
    UserActivationIdExpired,
    UserForActivationNotFound,
    UserIsAlreadyActivated,
    UserIsAlreadyActive,
)
from cash_flow.apps.users.selectors import UserSelector
from cash_flow.apps.users.services.activation_token import ActivationTokenService
from cash_flow.apps.users.services.user import UserService
from cash_flow.apps.users.tasks import (
    task_delete_not_active_user,
    task_send_activation_email,
)

logger = logging.getLogger(__name__)


@extend_schema(tags=["users"])
class UserViewSet(GenericViewSet, CreateModelMixin):
    queryset = UserSelector().list_users()
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer: UserCreateSerializer) -> None:
        data = serializer.validated_data
        user = UserService().create_user(**data)
        activation_service = ActivationTokenService()

        email_token = str(activation_service.set_email_id_token(user_id=user.id))
        activation_service.set_activation_user_id(
            email_id=email_token,
            user_id=user.id,
        )

        serializer.instance = user

        task_send_activation_email.delay(email=user.email)
        task_delete_not_active_user.apply_async(
            args=(user.id,),
            countdown=settings.ACTIVATION_EMAIL_ID_TTL,
        )

    @action(
        methods=["GET"],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def user_me(self, request: Request) -> Response:
        return Response(
            {
                "email": request.user.email,  # type: ignore
                "is_authenticated": True,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["users"])
class UserActivateView(APIView):
    def get(self, request: Request, uuid: str, token: str) -> Response:
        try:
            user_id = ActivationTokenService().retrieve_activation_user_id(
                email_id=uuid
            )
            UserService().update_user_active_status(
                user_id=user_id,
                token=token,
            )
        except (UserForActivationNotFound, UserActivationIdExpired) as e:
            raise NotFound(detail="User not found or invalid activation link") from e
        except UserIsAlreadyActive as e:
            raise UserIsAlreadyActivated from e

        return Response(
            {
                "details": "Your account activated successfully",
                "activated": True,
            },
            status=status.HTTP_200_OK,
        )
