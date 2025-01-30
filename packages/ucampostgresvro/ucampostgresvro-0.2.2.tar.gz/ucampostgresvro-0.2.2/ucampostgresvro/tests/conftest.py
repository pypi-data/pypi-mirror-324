import pytest

from ucampostgresvro.tests import utils as tools
from ucampostgresvro.exceptions import DbException


data_params = tools.db_params


@pytest.fixture
def user_db_fixture():
    # Setup
    if tools.check_db_connection(data_params):
        db = tools.setup_user_table_func(data_params)
        yield db
        # tear_down
        tools.teardown_user_table_func(data_params)
    else:
        raise DbException("Could not connect to the database after several retries.")


@pytest.fixture
def deploymentid_db_fixture():
    # Setup
    if tools.check_db_connection(data_params):
        db = tools.setup_deployment_table_func(data_params)
        yield db
        tools.teardown_deployment_table_func(data_params)
    else:
        raise DbException("Could not connect to the database after several retries.")


@pytest.fixture
def project_db_fixture():
    # Setup
    if tools.check_db_connection(data_params):
        db = tools.setup_project_table_func(data_params)
        yield db
        tools.teardown_project_table_func(data_params)
    else:
        raise DbException("Could not connect to the database after several retries.")


@pytest.fixture
def grant_db_fixture():
    # Setup
    if tools.check_db_connection(data_params):
        db = tools.setup_grant_table_func(data_params)
        yield db
        tools.teardown_grant_table_func(data_params)
    else:
        raise DbException("Could not connect to the database after several retries.")


@pytest.fixture
def costing_db_fixture():
    # Setup
    if tools.check_db_connection(data_params):
        db = tools.setup_costing_table_func(data_params)
        yield db
        tools.teardown_costing_table_func(data_params)
    else:
        raise DbException("Could not connect to the database after several retries.")
