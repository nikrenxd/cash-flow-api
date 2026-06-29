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
