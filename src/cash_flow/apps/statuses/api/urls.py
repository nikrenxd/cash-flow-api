from rest_framework.routers import DefaultRouter

from src.cash_flow.apps.statuses.api.views import StatusViewSet

statuses_router = DefaultRouter()

statuses_router.register("statuses", StatusViewSet, basename="statuses")

urlpatterns = statuses_router.urls
