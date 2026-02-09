from django.urls import path

from src.cash_flow.root.auth.views import LoginView, LogoutView

urlpatterns = [
    path("api/auth/login/", LoginView.as_view(), name="user-login"),
    path("api/auth/logout/", LogoutView.as_view(), name="user-logout"),
]
