from django.urls import path
from rest_framework import routers

from src.cash_flow.apps.comments.api.views import (
    CommentListCreateView,
    CommentViewSet,
)

comments_router = routers.DefaultRouter()
comments_router.register(
    "comments",
    CommentViewSet,
    basename="comments-update-delete",
)

urlpatterns = [
    path(
        "transactions/<int:transaction_id>/comments/",
        CommentListCreateView.as_view(),
        name="comments-list-create",
    ),
]

urlpatterns += comments_router.urls