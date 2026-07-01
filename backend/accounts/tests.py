"""Tests pédagogiques pour l'app accounts.

Ces tests servent d'exemples : signup, login, logout, accès protégé.
Lancez : pytest accounts/
"""

import json
import re

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

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


def test_login_returns_token(client, user):
    response = client.post(
        "/api/accounts/login/",
        {"email": "alice@test.com", "password": "motdepasse123"},
        format="json",
    )
    assert response.status_code == 200, response.data
    assert "token" in response.data
    assert response.data["user"]["email"] == "alice@test.com"


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


def test_me_export_json_is_strictly_filtered_by_authenticated_user(client, user):
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
