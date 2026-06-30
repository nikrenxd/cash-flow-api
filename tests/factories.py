import factory
from django.contrib.auth.hashers import make_password
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

from tests import constants


class CustomUserFactory(DjangoModelFactory):
    email = Sequence(lambda n: f"{constants.USERNAME}{n}@mail.com")
    password = make_password(constants.USER_PASSWORD)
    is_active = True
    is_staff = False

    class Meta:
        model = "users.CustomUser"


class StatusFactory(DjangoModelFactory):
    name = Sequence(lambda n: f"{constants.CUSTOM_STATUS}{n}")
    description = Sequence(lambda n: f"{constants.CUSTOM_STATUS_DESC}{n}")
    user = SubFactory(CustomUserFactory)

    class Meta:
        model = "statuses.Status"


class TransactionFactory(DjangoModelFactory):
    amount = factory.Faker("pydecimal", left_digits=5, right_digits=2)
    date = factory.Faker("date")

    user = SubFactory(CustomUserFactory)
    status = SubFactory(StatusFactory)

    class Meta:
        model = "transactions.Transaction"


class CommentFactory(DjangoModelFactory):
    body = factory.Faker("text", max_nb_chars=200)

    user = SubFactory(CustomUserFactory)
    transaction = SubFactory(TransactionFactory)

    class Meta:
        model = "comments.Comment"
