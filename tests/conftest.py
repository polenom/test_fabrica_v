import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from app.sheduler_app.services import UserDataClass, create_user


@pytest.fixture
def user():
    user_dc = UserDataClass(
        username='alukard',
        email='alik@tut.by',
        password='Qwerty123',
    )
    return create_user(user_dc)


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_dict():
    return dict(
        username='alukard123',
        password='Qwerty123',
        email='kalistro@tut.by'
    )


def add_auth(client: APIClient, user: UserDataClass) -> None:
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')
