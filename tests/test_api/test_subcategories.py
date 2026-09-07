import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from cash_flow.apps.categories.models import Category
from cash_flow.apps.subcategories.api.serializers import SubcategorySerializer
from cash_flow.apps.subcategories.models import Subcategory
from cash_flow.apps.users.models import CustomUser
from tests import constants
from tests.factories import CustomUserFactory, SubcategoryFactory


# noinspection DuplicatedCode
@pytest.mark.django_db
class TestSubcategoryEndpoints:
    subcategory_view_name = "subcategories-list"
    subcategory_detail_view_name = "subcategories-detail"
    parent_path_param = "category_id"

    def test_list(
        self,
        authenticated_client: APIClient,
        category: Category,
        subcategory_factory: SubcategoryFactory,
    ) -> None:
        expected = [
            subcategory_factory.create()
            for _ in range(constants.NUMBER_OBJECTS_TO_GENERATE)
        ]

        response = authenticated_client.get(
            reverse(
                self.subcategory_view_name,
                kwargs={self.parent_path_param: category.id},
            )
        )

        assert response.status_code == 200
        for instance in response.json():
            assert instance in expected

    def test_retrieve(
        self,
        authenticated_client: APIClient,
        category: Category,
        subcategory: Subcategory,
    ) -> None:
        expected = SubcategorySerializer(subcategory).data

        response = authenticated_client.get(
            reverse(
                self.subcategory_detail_view_name,
                kwargs={
                    self.parent_path_param: category.id,
                    "pk": subcategory.id,
                },
            )
        )

        assert response.status_code == 200
        assert response.json()["name"] == expected["name"]

    def test_create(
        self,
        authenticated_client: APIClient,
        category: Category,
    ) -> None:
        assert Subcategory.objects.count() == 0

        payload = {
            "name": "test",
        }
        response = authenticated_client.post(
            reverse(
                self.subcategory_view_name,
                kwargs={self.parent_path_param: category.id},
            ),
            payload,
        )

        assert response.status_code == 201
        assert Subcategory.objects.count() == 1

    def test_create_with_default_category(
        self,
        authenticated_client: APIClient,
        default_category: Category,
        custom_user: CustomUser,
        custom_user_factory: CustomUserFactory,
    ) -> None:
        assert Subcategory.objects.count() == 0

        payload = {
            "name": "test",
        }
        other_user = custom_user_factory.create()
        response = authenticated_client.post(
            reverse(
                self.subcategory_view_name,
                kwargs={self.parent_path_param: default_category.id},
            ),
            payload,
        )

        assert response.status_code == 201
        assert Subcategory.objects.filter(user=custom_user).count() == 1
        assert Subcategory.objects.filter(user=other_user).count() == 0

    def test_update(
        self,
        authenticated_client: APIClient,
        category: Category,
        subcategory: Subcategory,
        category_factory: SubcategoryFactory,
    ) -> None:
        other_category = category_factory.create()
        payload = {
            "name": "test",
            "category_id": other_category.id,
        }
        response = authenticated_client.put(
            reverse(
                self.subcategory_detail_view_name,
                kwargs={
                    self.parent_path_param: category.id,
                    "pk": subcategory.id,
                },
            ),
            payload,
        )
        updated_subcategory = Subcategory.objects.get(id=subcategory.id)

        assert response.status_code == 200
        assert updated_subcategory.category_id == other_category.id

    def test_delete(
        self,
        authenticated_client: APIClient,
        category: Category,
        subcategory: Subcategory,
    ) -> None:
        assert Subcategory.objects.count() == 1

        authenticated_client.delete(
            reverse(
                self.subcategory_detail_view_name,
                kwargs={
                    self.parent_path_param: category.id,
                    "pk": subcategory.id,
                },
            )
        )

        assert Subcategory.objects.count() == 0
