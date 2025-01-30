import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from cattle_grid.testing.fixtures import database  # noqa
from cattle_grid.account.models import Account, ActorForAccount
from cattle_grid.activity_pub.models import Actor

# from cattle_grid.config import GatewayAdminConfig
from cattle_grid.account.account import account_with_username_password
from . import create_user_router


@pytest.fixture
def test_client():
    app = FastAPI()
    app.include_router(create_user_router())

    yield TestClient(app)


@pytest.fixture
def test_client_reset():
    app = FastAPI()
    app.include_router(create_user_router())

    yield TestClient(app)


@pytest.mark.parametrize("form_data", [{}, {"username": "user"}, {"password": "pass"}])
async def test_create_user_bad_data(test_client, form_data):
    response = test_client.post(
        "/create",
        data=form_data,
        headers={"x-ap-location": "http://localhost/"},
    )

    assert response.status_code == 422


async def test_create_user_already_exists(test_client):
    await Account.create(name="user", password_hash="pass")

    response = test_client.post(
        "/create",
        data={"username": "user", "password": "pass"},
        headers={"x-ap-location": "http://localhost/"},
    )

    assert response.status_code == 409


async def test_create_user(test_client):
    username = "user"
    password = "pass"
    response = test_client.post(
        "/create",
        data={"username": username, "password": password},
        headers={"x-ap-location": "http://localhost/"},
    )

    assert response.status_code == 201
    assert 1 == await Account.filter().count()

    data = response.json()

    assert data["id"].startswith("http://localhost/actor")

    user = await account_with_username_password(username, password)
    assert user


@pytest.mark.skip("FIXME")
async def test_delete_not_found(test_client):
    username = "user"
    response = test_client.post(
        "/delete",
        data={"username": username},
    )

    assert response.status_code == 404


async def test_create_then_delete(test_client_reset):
    username = "user"
    password = "pass"
    response = test_client_reset.post(
        "/create",
        data={"username": username, "password": password},
        headers={"x-ap-location": "http://localhost/"},
    )

    assert response.status_code == 201
    assert 1 == await Account.filter().count()

    response = test_client_reset.post("/delete", data={"username": username})

    assert response.status_code == 200
    assert 0 == await Account.filter().count()
    assert 0 == await ActorForAccount.filter().count()
    assert 0 == await Actor.filter().count()

    response = test_client_reset.post(
        "/create",
        data={"username": username, "password": password},
        headers={"x-ap-location": "http://localhost/"},
    )

    assert response.status_code == 201
    assert 1 == await Account.filter().count()
