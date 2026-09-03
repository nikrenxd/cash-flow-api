import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from cash_flow.apps.transactions.api.serializers import (
    TransactionDetailSerializer,
)
from cash_flow.apps.transactions.models import Transaction
from tests import constants


@pytest.mark.django_db
class TestTransactionEndpoints:
    transaction_view_name = "transactions-list"
    transaction_detail_view_name = "transactions-detail"

    def test_list(
        self, authenticated_client: APIClient, transaction_factory
    ) -> None:
        expected = [
            transaction_factory()
            for _ in range(constants.NUMBER_OBJECTS_TO_GENERATE)
        ]

        response = authenticated_client.get(reverse(self.transaction_view_name))

        assert response.status_code == 200
        for instance in response.json():
            assert instance in expected

    def test_retrieve(
        self,
        authenticated_client: APIClient,
        transaction: Transaction,
    ) -> None:
        expected = TransactionDetailSerializer(transaction).data

        response = authenticated_client.get(
            reverse(
                self.transaction_detail_view_name,
                kwargs={"pk": transaction.id},
            ),
        )

        assert response.status_code == 200
        assert response.json() == expected

    def test_create(
        self, authenticated_client: APIClient, status, subcategory
    ) -> None:
        payload = {
            "amount": constants.TRANSACTION_AMOUNT,
            "status_id": status.id,
            "subcategory_id": subcategory.id,
        }

        assert Transaction.objects.count() == 0
        response = authenticated_client.post(
            reverse(self.transaction_view_name),
            data=payload,
        )

        assert response.status_code == 201
        assert Transaction.objects.count() == 1

    def test_create_with_default_status(
        self,
        authenticated_client: APIClient,
        default_status,
        subcategory,
        custom_user_factory,
    ) -> None:
        other_user = custom_user_factory()
        payload = {
            "amount": constants.TRANSACTION_AMOUNT,
            "status_id": default_status.id,
            "subcategory_id": subcategory.id,
        }

        response = authenticated_client.post(
            reverse(self.transaction_view_name),
            data=payload,
        )
        response_body = response.json()

        transaction_status_id = Transaction.objects.get(
            id=response_body["id"]
        ).status.id
        other_user_transactions_count = Transaction.objects.filter(
            user_id=other_user.id,
            status_id=transaction_status_id,
        ).count()

        assert response.status_code == 201
        assert transaction_status_id == default_status.id
        assert other_user_transactions_count == 0

    def test_partial_update(
        self, authenticated_client: APIClient, transaction: Transaction
    ) -> None:
        new_amount = 6767
        payload = {
            "amount": new_amount,
        }

        response = authenticated_client.patch(
            reverse(
                self.transaction_detail_view_name,
                kwargs={"pk": transaction.id},
            ),
            data=payload,
        )

        assert response.status_code == 200

    def test_delete(
        self, authenticated_client: APIClient, transaction: Transaction
    ) -> None:
        assert Transaction.objects.count() == 1
        authenticated_client.delete(
            reverse(
                self.transaction_detail_view_name,
                kwargs={"pk": transaction.id},
            )
        )

        assert Transaction.objects.count() == 0

    def test_access_to_other_user_transaction(
        self,
        other_authenticated_client: APIClient,
        transaction: Transaction,
    ) -> None:
        payload = {
            "amount": 0,
        }

        response = other_authenticated_client.patch(
            reverse(
                self.transaction_detail_view_name,
                kwargs={"pk": transaction.id},
            ),
            data=payload,
        )

        assert response.status_code == 404
