import logging

from django.contrib.auth.tokens import default_token_generator
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

from src.cash_flow.apps.users.api.serializers import (
    UserActivateResponseSerializer,
    UserCreateSerializer,
    UserNotActivateResponseSerializer,
)
from src.cash_flow.apps.users.exceptions import UserObjectDoesNotExist
from src.cash_flow.apps.users.selectors import UserSelector
from src.cash_flow.apps.users.services.users_actions import UserService
from src.cash_flow.apps.users.tasks import task_send_activation_email

logger = logging.getLogger(__name__)


@extend_schema(tags=["users"])
class UserViewSet(GenericViewSet, CreateModelMixin):
    queryset = UserSelector().list_users()
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer: UserCreateSerializer) -> None:
        data = serializer.validated_data
        user = UserService().create_user(**data)
        serializer.instance = user

        task_send_activation_email.delay(email=user.email)

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
    @extend_schema(
        request=None,
        responses={
            200: UserActivateResponseSerializer,
            400: UserNotActivateResponseSerializer,
            404: UserNotActivateResponseSerializer,
        },
    )
    def get(
        self,
        request: Request,
        uidb64: str,
        token: str,
    ) -> Response:
        try:
            user = UserSelector().get_user_by_uidb(uidb64=uidb64)
        except UserObjectDoesNotExist:
            raise NotFound(detail="User not found or invalid activation link")

        if user.is_active:
            return Response(
                {
                    "details": "User has been already active",
                    "activated": True,
                },
                status=status.HTTP_200_OK,
            )

        if not default_token_generator.check_token(user, token):
            logger.warning(f"Invalid activation token for user: {user.id}")
            return Response(
                {
                    "details": "Invalid or expired activation token",
                    "activated": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        UserService().update_user_active_status(user=user)
        logger.info(f"User: {user.id} has been activated")

        return Response(
            {
                "details": "Your account activated successfully",
                "activated": True,
            },
            status=status.HTTP_200_OK,
        )
