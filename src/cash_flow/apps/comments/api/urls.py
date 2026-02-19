from django.urls import include, path
from rest_framework import routers

from src.cash_flow.apps.comments.api.views import CommentViewSet

comments_router = routers.DefaultRouter()
comments_router.register(
    "comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path(
        "transactions/<int:transaction_id>/",
        include(comments_router.urls),
    ),
]
