from typing import Optional, AsyncIterable

import pytest
from fastapi import Depends
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine as Database
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database, drop_database

from main import api
from sql_app.database import Base
from sql_app.sql_access import get_db

URL = "sqlite:///tests/test.db"
ENGINE = create_engine(
    URL, connect_args={"check_same_thread": False}
)

def get_test_db_conn() -> Database:
    assert ENGINE is not None
    return ENGINE


def get_test_db() -> AsyncIterable[Session]:
    sess = Session(bind=ENGINE)
    try:
        yield sess
    finally:
        sess.close()


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """
  Create a clean database on every test case.

  We use the `sqlalchemy_utils` package here for a few helpers in consistently
  creating and dropping the database.
  """
    if database_exists(URL):
        drop_database(URL)
    create_database(URL)  # Create the test database.
    Base.metadata.create_all(ENGINE)  # Create the tables.
    api.dependency_overrides[get_db] = get_test_db  # Mock the Database Dependency
    yield  # Run the tests.
    drop_database(URL)  # Drop the test database.


@pytest.yield_fixture
def test_db_session():
    """Returns an sqlalchemy session, and after the test tears down everything properly."""

    session = Session(bind=ENGINE)

    yield session
    # Drop all data after each test
    for tbl in reversed(Base.metadata.sorted_tables):
        ENGINE.execute(tbl.delete())
    # put back the connection to the connection pool
    session.close()


@pytest.fixture()
def client():
    """
    When using the 'client' fixture in test cases, we'll get full database
    rollbacks between test cases:
    """
    with TestClient(api) as client:
        yield client

