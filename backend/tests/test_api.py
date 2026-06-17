

import os
import sys

from fastapi.testclient import TestClient

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

# Use an in-memory SQLite database during tests.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app.main import app
from app.database import engine
from app.models import Base

# Create tables in the test database.
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_user_registration_and_login():
    user_data = {"username": "testuser", "email": "test@example.com", "password": "password123"}
    register_response = client.post("/register", json=user_data)
    assert register_response.status_code == 201
    assert register_response.json()["username"] == "testuser"

    login_response = client.post(
        "/api/token",
        data={"username": "testuser", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert token_data["token_type"] == "bearer"
    assert "access_token" in token_data


def test_create_post_and_comment():
    login_response = client.post(
        "/api/token",
        data={"username": "testuser", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = login_response.json()["access_token"]

    create_post_response = client.post(
        "/posts/",
        json={"title": "Testing Post", "content": "This is a test post."},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_post_response.status_code == 201
    post = create_post_response.json()
    assert post["title"] == "Testing Post"

    create_comment_response = client.post(
        f"/posts/{post['id']}/comments",
        json={"text": "Nice post!"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_comment_response.status_code == 201
    comment = create_comment_response.json()
    assert comment["text"] == "Nice post!"

    comments_response = client.get(f"/posts/{post['id']}/comments")
    assert comments_response.status_code == 200
    assert len(comments_response.json()) == 1
