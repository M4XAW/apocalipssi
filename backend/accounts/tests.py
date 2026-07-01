"""Tests pédagogiques pour l'app accounts.

Ces tests servent d'exemples : signup, login, logout, accès protégé.
Lancez : pytest accounts/
"""

import pytest
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(
        username="alice", email="alice@test.com", password="motdepasse123"
    )


def test_signup_creates_user(client):
    # Lot 3 : inscription par EMAIL (username = email en interne).
    response = client.post(
        "/api/accounts/signup/",
        {
            "email": "bob@test.com",
            "password": "motdepasse123",
        },
        format="json",
    )
    assert response.status_code == 201, response.data
    assert User.objects.filter(email="bob@test.com").exists()


def test_signup_requires_email(client):
    response = client.post(
        "/api/accounts/signup/",
        {"password": "motdepasse123"},
        format="json",
    )
    assert response.status_code == 400


def test_login_sets_auth_cookie(client, user):
    response = client.post(
        "/api/accounts/login/",
        {"email": "alice@test.com", "password": "motdepasse123"},
        format="json",
    )
    assert response.status_code == 200, response.data
    assert "token" not in response.data
    assert response.data["user"]["email"] == "alice@test.com"
    assert settings.AUTH_TOKEN_COOKIE_NAME in response.cookies
    assert response.cookies[settings.AUTH_TOKEN_COOKIE_NAME]["httponly"]
    assert "csrftoken" in response.cookies


def test_login_with_wrong_password(client, user):
    response = client.post(
        "/api/accounts/login/",
        {"email": "alice@test.com", "password": "wrong"},
        format="json",
    )
    assert response.status_code == 400


def test_me_requires_auth(client):
    response = client.get("/api/accounts/me/")
    assert response.status_code in (401, 403)


def test_me_with_token(client, user):
    from rest_framework.authtoken.models import Token

    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = client.get("/api/accounts/me/")
    assert response.status_code == 200
    assert response.data["username"] == "alice"


def test_me_with_auth_cookie(client, user):
    client.post(
        "/api/accounts/login/",
        {"email": "alice@test.com", "password": "motdepasse123"},
        format="json",
    )
    response = client.get("/api/accounts/me/")
    assert response.status_code == 200
    assert response.data["email"] == "alice@test.com"


def test_logout_invalidates_token(client, user):
    from rest_framework.authtoken.models import Token

    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = client.post("/api/accounts/logout/")
    assert response.status_code == 204
    # Le token n'existe plus
    assert not Token.objects.filter(key=token.key).exists()


def test_logout_with_auth_cookie_clears_cookie(client, user):
    from rest_framework.authtoken.models import Token

    login_response = client.post(
        "/api/accounts/login/",
        {"email": "alice@test.com", "password": "motdepasse123"},
        format="json",
    )
    csrf_token = login_response.cookies["csrftoken"].value

    response = client.post("/api/accounts/logout/", HTTP_X_CSRFTOKEN=csrf_token)
    assert response.status_code == 204
    assert not Token.objects.filter(user=user).exists()
    assert response.cookies[settings.AUTH_TOKEN_COOKIE_NAME].value == ""


def test_logout_with_auth_cookie_without_csrf_still_clears_cookie(client, user):
    from rest_framework.authtoken.models import Token

    client.post(
        "/api/accounts/login/",
        {"email": "alice@test.com", "password": "motdepasse123"},
        format="json",
    )

    response = client.post("/api/accounts/logout/")
    assert response.status_code == 204
    assert not Token.objects.filter(user=user).exists()
    assert response.cookies[settings.AUTH_TOKEN_COOKIE_NAME].value == ""
