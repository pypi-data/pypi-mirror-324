from cattle_grid.testing.fixtures import database  # noqa

from .testing import *  # noqa


def test_settings(test_client, bearer_header):  # noqa
    response = test_client.get("/settings", headers=bearer_header)

    assert response.status_code == 200
    data = response.json()

    assert "http://abel" in data["baseUrls"]
