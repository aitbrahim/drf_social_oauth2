import pytest
import logging
from django.urls import reverse
from faker import Faker
from pytest_django.fixtures import SettingsWrapper

from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def faker():
    f = Faker()
    f.seed(500)
    yield f


@pytest.fixture()
def rest_client():
    return APIClient()


@pytest.fixture()
def fb_access_token():
    return 'EAACegdMbJUABAP4quJdL59IedfVAmhiFCxlop9zAETp544rsKko6rkbJf09chUcKl8caU' \
           'JIKtXslEJcs2cq7ORMb1ZAH8vZBQqCJAUE8ZC0ZCe7GD9ClFDkcpMKtv9ofgZBmDbejgnZ' \
           'ArRsLzHWZB3HuKsEZBEZCuywxcHPWB703Ejl5ZAG5kmVKxWOGyc4IBIVIXhZCLJimOnGOgZDZD'
