from django.urls import path
from rest_framework.routers import DefaultRouter

from src.cash_flow.apps.users.api.views import UserActivateView, UserViewSet

users_router = DefaultRouter()

users_router.register("users", UserViewSet, basename="users")
urlpatterns = [
    path(
        "activate/<str:uidb64>/<str:token>/",
        UserActivateView.as_view(),
        name="activate",
    )
]
urlpatterns += users_router.urls
