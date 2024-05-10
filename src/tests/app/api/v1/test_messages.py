import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create_message_success(app: FastAPI, client: TestClient):
    url = app.url_path_for("create_chat_handler")
    title = "Title1"
    response = client.post(url, json={"title": title})

    assert response.status_code == 201
    chat_oid = response.json()["chat_oid"]

    url = app.url_path_for("create_message_handler", chat_oid=chat_oid)
    text = "super message"
    response = client.post(url, json={"chat_oid": chat_oid, "text": text})

    assert response.status_code == 201
    assert response.json()["text"] == text


@pytest.mark.asyncio
async def test_create_messages_empty(app: FastAPI, client: TestClient):
    url = app.url_path_for("create_chat_handler")
    title = "Title2"
    response = client.post(url, json={"title": title})

    assert response.status_code == 201
    chat_oid = response.json()["chat_oid"]

    url = app.url_path_for("create_message_handler", chat_oid=chat_oid)
    text = ""
    response = client.post(url, json={"chat_oid": chat_oid, "text": text})

    assert response.status_code == 400
    assert response.json()["detail"]


@pytest.mark.asyncio
async def test_create_messages_too_long(app: FastAPI, client: TestClient):
    url = app.url_path_for("create_chat_handler")
    title = "Title3"
    response = client.post(url, json={"title": title})

    assert response.status_code == 201
    chat_oid = response.json()["chat_oid"]

    url = app.url_path_for("create_message_handler", chat_oid=chat_oid)
    text = f"{'a'*1001}"
    response = client.post(url, json={"chat_oid": chat_oid, "text": text})

    assert response.status_code == 400
    assert response.json()["detail"]
