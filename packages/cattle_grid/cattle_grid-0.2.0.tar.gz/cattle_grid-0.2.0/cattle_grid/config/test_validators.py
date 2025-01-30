import pytest

import dynaconf
from dynaconf import Dynaconf

from .validators import all_validators


@pytest.fixture
def settings():
    return Dynaconf(validators=all_validators)


@pytest.mark.parametrize(
    ["key", "value"],
    [("internal_exchange", "cattle_grid_internal"), ("exchange", "cattle_grid")],
)
def test_activity_pub_validators(settings, key, value):
    assert settings.activity_pub[key] == value


@pytest.mark.parametrize(
    ["key", "value"],
    [("enable", False), ("enable_reset", False)],
)
def test_gateway_admin(settings, key, value):
    assert settings.gateway.admin[key] == value


@pytest.mark.parametrize(
    ["key", "value"],
    [
        ("amqp_uri", "amqp://localhost"),
        ("db_uri", "sqlite://cattle_grid.db"),
        ("enable_reporting", False),
    ],
)
def test_base_validators(settings, key, value):
    assert settings[key] == value


def test_plugins(settings):
    assert settings.plugins == []


@pytest.mark.parametrize(
    ["key", "value"],
    [
        ("base_urls", []),
    ],
)
def test_frontend_validators(settings, key, value):
    assert settings.frontend[key] == value


def test_frontend_validations(settings):
    settings.update({"frontend.base_urls": ["http://abel"]}, validate=True)
    settings.update({"frontend.base_urls": ["https://abel"]}, validate=True)

    with pytest.raises(dynaconf.validator.ValidationError):
        settings.update({"frontend.base_urls": ["abel"]}, validate=True)
