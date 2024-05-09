import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create_chat_success(app: FastAPI, client: TestClient):
    url = app.url_path_for("create_chat_handler")
    title = "SuperTitle"
    response = client.post(url, json={"title": title})

    assert response.status_code == 201
    assert response.json()["title"] == title


@pytest.mark.asyncio
async def test_create_chat_title_starts_with_no_capital(
    app: FastAPI, client: TestClient
):
    url = app.url_path_for("create_chat_handler")
    title = "superTitle"
    response = client.post(url, json={"title": title})

    assert response.status_code == 400
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_create_chat_title_empty(app: FastAPI, client: TestClient):
    url = app.url_path_for("create_chat_handler")
    title = ""
    response = client.post(url, json={"title": title})

    assert response.status_code == 400
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_create_chat_title_too_long(app: FastAPI, client: TestClient):
    url = app.url_path_for("create_chat_handler")
    title = f'{"A"*101}'
    response = client.post(url, json={"title": title})

    assert response.status_code == 400
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_create_chat_title_already_exists(app: FastAPI, client: TestClient):
    url = app.url_path_for("create_chat_handler")
    title = "AnotherSuperTitle"
    response = client.post(url, json={"title": title})

    assert response.status_code == 201

    response = client.post(url, json={"title": title})

    assert response.status_code == 400
    assert response.json()["detail"]
