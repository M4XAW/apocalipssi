"""Tests pédagogiques pour l'app accounts.

Ces tests servent d'exemples : signup, login, logout, accès protégé.
Lancez : pytest accounts/
"""

import hashlib
import json
import re

import pytest
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from accounts.models import DataRequest
from quizzes.models import Question, Quiz

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


def test_me_export_requires_auth(client):
    response = client.get("/api/accounts/me/export/")
    assert response.status_code in (401, 403)


def test_me_export_json_is_strictly_filtered_by_authenticated_user(
    client, user
):
    other_user = User.objects.create_user(
        username="bob", email="bob@test.com", password="motdepasse123"
    )

    alice_quiz = Quiz.objects.create(
        user=user,
        title="Quiz Alice",
        source_text="Cours privé Alice",
        score=1,
    )
    Question.objects.create(
        quiz=alice_quiz,
        index=1,
        prompt="Question Alice ?",
        options=["A", "B", "C", "D"],
        correct_index=0,
        selected_index=1,
    )

    bob_quiz = Quiz.objects.create(
        user=other_user,
        title="Quiz Bob",
        source_text="Cours privé Bob",
        score=1,
    )
    Question.objects.create(
        quiz=bob_quiz,
        index=1,
        prompt="Question Bob ?",
        options=["A", "B", "C", "D"],
        correct_index=0,
        selected_index=2,
    )

    client.force_authenticate(user=user)
    response = client.get("/api/accounts/me/export/")

    assert response.status_code == 200
    assert response["Content-Disposition"].startswith("attachment; filename=")
    assert re.search(
        r"edututor-export-user-\d+-\d{8}-\d{6}\.json",
        response["Content-Disposition"],
    )

    payload = json.loads(response.content)
    assert payload["user"]["email"] == "alice@test.com"
    assert len(payload["quizzes"]) == 1
    assert payload["quizzes"][0]["title"] == "Quiz Alice"
    assert payload["quizzes"][0]["questions"][0]["prompt"] == "Question Alice ?"
    assert payload["reports"] == []

    serialized = json.dumps(payload, ensure_ascii=False)
    assert "Quiz Bob" not in serialized
    assert "Cours privé Bob" not in serialized
    assert "Question Bob ?" not in serialized
    assert "bob@test.com" not in serialized


def test_me_export_csv_is_machine_readable_attachment(client, user):
    quiz = Quiz.objects.create(
        user=user,
        title="Quiz CSV",
        source_text="Cours CSV",
        score=7,
    )
    Question.objects.create(
        quiz=quiz,
        index=1,
        prompt="Question CSV ?",
        options=["A", "B", "C", "D"],
        correct_index=0,
        selected_index=0,
    )

    client.force_authenticate(user=user)
    response = client.get("/api/accounts/me/export/?format=csv")

    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/csv")
    assert re.search(
        r"edututor-export-user-\d+-\d{8}-\d{6}\.csv",
        response["Content-Disposition"],
    )

    body = response.content.decode("utf-8")
    assert "entity,entity_id,parent_entity,parent_id,field,value" in body
    assert "Quiz CSV" in body
    assert "Question CSV ?" in body


def test_me_export_creates_sar_audit_trail(client, user):
    client.force_authenticate(user=user)
    response = client.get("/api/accounts/me/export/")

    assert response.status_code == 200
    assert DataRequest.objects.count() == 1

    audit = DataRequest.objects.get()
    assert audit.user == user
    assert audit.request_type == DataRequest.RequestType.ACCESS
    assert audit.status == DataRequest.Status.RESPONDED
    assert audit.export_format == "json"
    assert (
        audit.export_file_hash == hashlib.sha256(response.content).hexdigest()
    )
    assert audit.requested_at is not None
    assert audit.responded_at is not None


def test_me_export_csv_audit_trail_records_format(client, user):
    client.force_authenticate(user=user)
    response = client.get("/api/accounts/me/export/?format=csv")

    assert response.status_code == 200
    audit = DataRequest.objects.get()
    assert audit.export_format == "csv"
    assert (
        audit.export_file_hash == hashlib.sha256(response.content).hexdigest()
    )


def test_admin_data_requests_lists_sar_audit(client, user):
    from rest_framework.authtoken.models import Token

    admin = User.objects.create_user(
        username="admin@test.com",
        email="admin@test.com",
        password="motdepasse123",
        is_staff=True,
    )
    Token.objects.create(user=admin)

    client.force_authenticate(user=user)
    client.get("/api/accounts/me/export/")

    client.force_authenticate(user=admin)
    response = client.get("/api/admin/data-requests/")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["user_email"] == user.email
    assert response.data[0]["status"] == DataRequest.Status.RESPONDED
    assert len(response.data[0]["export_file_hash"]) == 64


def test_admin_data_requests_requires_staff(client, user):
    client.force_authenticate(user=user)
    client.get("/api/accounts/me/export/")

    response = client.get("/api/admin/data-requests/")
    assert response.status_code == 403


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