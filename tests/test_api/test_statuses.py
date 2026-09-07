import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from cash_flow.apps.statuses.api.serializers import StatusDetailSerializer
from cash_flow.apps.statuses.models import Status
from tests import constants
from tests.factories import StatusFactory


@pytest.mark.django_db
class TestStatusEndpoints:
    status_view_name = "statuses-list"
    status_detail_view_name = "statuses-detail"

    def test_list(
        self, authenticated_client: APIClient, status_factory: StatusFactory
    ) -> None:
        expected = [
            status_factory.create()
            for _ in range(constants.NUMBER_OBJECTS_TO_GENERATE)
        ]
        response = authenticated_client.get(reverse(self.status_view_name))

        assert response.status_code == 200
        for instance in response.json():
            assert instance in expected

    def test_retrieve(self, authenticated_client: APIClient, status: Status) -> None:
        expected = StatusDetailSerializer(status).data
        response = authenticated_client.get(
            reverse(
                self.status_detail_view_name,
                kwargs={
                    "pk": status.id,
                },
            )
        )

        assert response.status_code == 200
        assert response.json()["name"] == expected["name"]

    def test_create(self, authenticated_client: APIClient) -> None:
        assert Status.objects.count() == 0

        payload = {
            "name": "test",
        }
        response = authenticated_client.post(
            reverse(self.status_view_name),
            payload,
        )

        assert response.status_code == 201
        assert Status.objects.count() == 1

    def test_partial_update(
        self, authenticated_client: APIClient, status: Status
    ) -> None:
        new_name = "updated name"
        payload = {
            "name": new_name,
        }
        response = authenticated_client.patch(
            reverse(self.status_detail_view_name, kwargs={"pk": status.id}),
            payload,
        )

        assert response.status_code == 200
        assert Status.objects.get(id=status.id).name == new_name

    def test_delete(self, authenticated_client: APIClient, status: Status) -> None:
        assert Status.objects.count() == 1

        authenticated_client.delete(
            reverse(
                self.status_detail_view_name,
                kwargs={"pk": status.id},
            )
        )

        assert Status.objects.count() == 0
