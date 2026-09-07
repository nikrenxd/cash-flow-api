import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from cash_flow.apps.categories.api.serializers import CategoryDetailSerializer
from cash_flow.apps.categories.models import Category
from cash_flow.apps.transaction_types.models import TransactionType
from cash_flow.apps.users.models import CustomUser
from tests import constants
from tests.factories import (
    CategoryFactory,
    CustomUserFactory,
    TransactionTypeFactory,
)


@pytest.mark.django_db
class TestCategoryEndpoints:
    categories_view_name = "categories-list"
    categories_detail_view_name = "categories-detail"
    parent_path_param = "transaction_type_id"

    def test_list(
        self,
        authenticated_client: APIClient,
        category_factory: CategoryFactory,
        transaction_type: TransactionType,
    ) -> None:
        expected = [
            category_factory.create(transaction_type=transaction_type)
            for _ in range(constants.NUMBER_OBJECTS_TO_GENERATE)
        ]

        response = authenticated_client.get(
            reverse(
                self.categories_view_name,
                kwargs={self.parent_path_param: transaction_type.id},
            )
        )

        for instance in response.json():
            assert instance in expected

    def test_retrieve(
        self,
        authenticated_client: APIClient,
        transaction_type: TransactionType,
        category: Category,
    ) -> None:
        expected = CategoryDetailSerializer(category).data

        response = authenticated_client.get(
            reverse(
                self.categories_detail_view_name,
                kwargs={
                    self.parent_path_param: transaction_type.id,
                    "pk": category.id,
                },
            )
        )

        assert response.status_code == 200
        assert response.json() == expected

    def test_create(
        self,
        authenticated_client: APIClient,
        transaction_type: TransactionType,
    ) -> None:
        assert Category.objects.count() == 0
        payload = {
            "name": "test",
            "transaction_type_id": transaction_type.id,
        }
        response = authenticated_client.post(
            reverse(
                self.categories_view_name,
                kwargs={self.parent_path_param: transaction_type.id},
            ),
            payload,
        )

        assert response.status_code == 201
        assert Category.objects.count() == 1

    def test_create_with_default_transaction_type(
        self,
        authenticated_client: APIClient,
        default_transaction_type: TransactionType,
        custom_user: CustomUser,
        custom_user_factory: CustomUserFactory,
    ) -> None:
        assert Category.objects.count() == 0
        payload = {
            "name": "test",
            "transaction_type_id": default_transaction_type.id,
        }
        other_user = custom_user_factory.create()
        response = authenticated_client.post(
            reverse(
                self.categories_view_name,
                kwargs={self.parent_path_param: default_transaction_type.id},
            ),
            payload,
        )

        assert response.status_code == 201
        assert Category.objects.filter(user=custom_user).count() == 1
        assert Category.objects.filter(user=other_user).count() == 0

    def test_partial_update(
        self,
        authenticated_client: APIClient,
        transaction_type: TransactionType,
        category: Category,
        transaction_type_factory: TransactionTypeFactory,
    ) -> None:
        other_transaction_type = transaction_type_factory.create()
        payload = {
            "transaction_type_id": other_transaction_type.id,
        }
        response = authenticated_client.patch(
            reverse(
                self.categories_detail_view_name,
                kwargs={
                    self.parent_path_param: transaction_type.id,
                    "pk": category.id,
                },
            ),
            payload,
        )
        updated_object = Category.objects.get(id=category.id)

        assert response.status_code == 200
        assert updated_object.transaction_type_id == other_transaction_type.id

    def test_delete(
        self,
        authenticated_client: APIClient,
        transaction_type: TransactionType,
        category: Category,
    ) -> None:
        assert Category.objects.count() == 1

        authenticated_client.delete(
            reverse(
                self.categories_detail_view_name,
                kwargs={
                    self.parent_path_param: transaction_type.id,
                    "pk": category.id,
                },
            )
        )

        assert Category.objects.count() == 0
