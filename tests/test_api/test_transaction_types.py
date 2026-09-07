import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from cash_flow.apps.transaction_types.api.serializers import (
    TransactionTypeDetailSerializer,
)
from cash_flow.apps.transaction_types.models import TransactionType
from tests import constants


@pytest.mark.django_db
class TestTransactionTypeEndpoints:
    transaction_type_view_name = "transaction-types-list"
    transaction_type_detail_view_name = "transaction-types-detail"

    def test_list(
        self,
        authenticated_client: APIClient,
        transaction_type_factory,
    ) -> None:
        expected = [
            transaction_type_factory()
            for _ in range(constants.NUMBER_OBJECTS_TO_GENERATE)
        ]

        response = authenticated_client.get(reverse(self.transaction_type_view_name))

        assert response.status_code == 200
        for instance in response.json():
            assert instance in expected

    def test_retrieve(
        self,
        authenticated_client: APIClient,
        transaction_type: TransactionType,
    ) -> None:
        expected = TransactionTypeDetailSerializer(transaction_type).data

        response = authenticated_client.get(
            reverse(
                self.transaction_type_detail_view_name,
                kwargs={"pk": transaction_type.pk},
            )
        )

        assert response.status_code == 200
        assert response.json() == expected

    def test_create(self, authenticated_client: APIClient) -> None:
        assert TransactionType.objects.count() == 0

        payload = {
            "name": "test",
        }
        response = authenticated_client.post(
            reverse(self.transaction_type_view_name), payload
        )

        assert response.status_code == 201
        assert TransactionType.objects.count() == 1

    def test_partial_update(
        self,
        authenticated_client: APIClient,
        transaction_type: TransactionType,
    ) -> None:
        new_name = "new name"
        payload = {
            "name": new_name,
        }

        response = authenticated_client.patch(
            reverse(
                self.transaction_type_detail_view_name,
                kwargs={"pk": transaction_type.id},
            ),
            data=payload,
        )

        assert response.status_code == 200
        assert response.json()["name"] == new_name

    def test_delete(
        self,
        authenticated_client: APIClient,
        transaction_type: TransactionType,
    ) -> None:
        assert TransactionType.objects.count() == 1

        authenticated_client.delete(
            reverse(
                self.transaction_type_detail_view_name,
                kwargs={"pk": transaction_type.id},
            )
        )

        assert TransactionType.objects.count() == 0
