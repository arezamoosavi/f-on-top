import asyncio
import pytest
from unittest.mock import Mock, patch

from datetime import datetime

from mongoengine import connect, disconnect
from faust_app import app as f_app


@pytest.fixture(name="mock_mongo", scope="session")
def fixture_mock_db():
    disconnect()
    db = connect("mongoenginetest", host="mongomock://localhost")
    print("\n test_mongo: connected!\n")
    yield db
    db.drop_database("mongoenginetest")
    db.close()
    print("\n test_mongo: disconnected!")


@pytest.yield_fixture(name="event_loop", scope="session")
def fixture_event_loop(request):
    """passing in event_loop helps avoid 'attached to a different loop' error"""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(name="mock_faust", scope="session")
def fixture_faust_app(event_loop):
    """passing in event_loop helps avoid 'attached to a different loop' error"""
    f_app.app.finalize()
    f_app.app.conf.store = "memory://"
    f_app.app.flow_control.resume()
    return f_app.app
