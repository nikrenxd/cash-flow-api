from django.contrib.auth import authenticate, login, logout
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.cash_flow.root.auth.serializers import (
    LoginResponseSerializer,
    LoginSerializer,
    LogoutResponseSerializer,
)


class LoginView(APIView):
    @extend_schema(
        request=LoginSerializer,
        responses={
            200: LoginResponseSerializer,
            401: LoginResponseSerializer,
        },
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email, password = (
            serializer.validated_data["email"],
            serializer.validated_data["password"],
        )
        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response(
                {"details": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {"details": "Confirm your email before logging in"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)
        return Response(
            {"details": "Logged in successfully"},
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    @extend_schema(
        request=None,
        responses={200: LogoutResponseSerializer},
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        logout(request)
        return Response({"details": "Logged out successfully"})
