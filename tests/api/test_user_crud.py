import pytest
from django.contrib.auth import get_user_model

from django.urls import reverse

from tests.conftest import add_auth

BASE_URL = reverse('user-list')

User = get_user_model()


@pytest.mark.parametrize('url,method,status,data', [
    [BASE_URL, 'get', 401, {}],
    [BASE_URL, 'post', 400, {}],
    [BASE_URL + 'alukard/', 'post', 401, {}],
    [BASE_URL + 'alukard/', 'get', 401, {}],
    [BASE_URL + 'alukard/', 'patch', 401, {}],
    [BASE_URL + 'alukard/', 'delete', 401, {}],
])
@pytest.mark.django_db
def test_method_without_auth(url, method, status, data, client, user):
    response = getattr(client, method)(url, data=data)
    assert response.status_code == status


@pytest.mark.parametrize('url,method,status,data', [
    [BASE_URL, 'get', 403, {}],
    [BASE_URL, 'post', 400, {}],
    [BASE_URL + 'alukard/', 'post', 405, {}],
    [BASE_URL + 'alukard/', 'get', 200, {}],
    [BASE_URL + 'alukard/', 'patch', 200, {}],
    [BASE_URL + 'alukard/', 'delete', 204, {}],
])
@pytest.mark.django_db
def test_method_with_auth(url, method, status, data, client, user):
    add_auth(client, user)
    response = getattr(client, method)(url, data=data, )
    assert response.status_code == status


@pytest.mark.django_db
def test_user_create(client, user_dict):
    response = client.post(BASE_URL, data=user_dict)
    assert response.status_code == 201
    assert response.data['username'] == user_dict['username']
    assert response.data['email'] == user_dict['email']


@pytest.mark.django_db
def test_create_user(client, user_dict):
    response = client.post(BASE_URL, data=user_dict)
    assert User.objects.get(username=user_dict['username'])


@pytest.mark.parametrize('data', [
    {'username': 'aluk', 'password': 'Qwerty123', 'email': 1},
    {'username': 'alukard', 'password': 'Qwerty123', 'email': 'alukard@tut.by'},
    {'password': 'Qwerty123', 'email': 'alukard@tut.by'},
    {'username': 'aluk', 'email': 'alukard@tut.by'},
    {'username': 'aluk', 'password': 'Qwerty123'},
    {'username': 'aluka', 'password': 'asd', 'email': 'alukard@tut.by'},
])
@pytest.mark.django_db
def test_create_user_bad_request(data, client, user):
    response = client.post(BASE_URL, data=data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_patch_user(client, user):
    data = {
        'username': 'aaa',
        'email': 'aaa@tut.by'
    }
    add_auth(client, user)
    response = client.patch(BASE_URL + f'{user.username}/', data=data)
    assert User.objects.get(username='aaa')
    assert User.objects.get(username='aaa').email == 'aaa@tut.by'
    assert User.objects.filter(username='alukard').count() == 0


@pytest.mark.django_db
def test_delete_user(client, user):
    add_auth(client, user)
    response = client.delete(BASE_URL + f'{user.username}/')
    assert User.objects.filter(username=user.username).count() == 0
