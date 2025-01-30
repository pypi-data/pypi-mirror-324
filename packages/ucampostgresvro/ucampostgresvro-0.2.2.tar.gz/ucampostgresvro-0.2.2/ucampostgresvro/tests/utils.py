import psycopg2
import time

from ucampostgresvro import utils
from ucampostgresvro.DBA import DB
from ucampostgresvro.exceptions import DbException
from ucampostgresvro.tests.dbconnect import db_params

db_params = db_params

tables = {
    "user": "test_user",
    "deploymentid": "test_deployment",
    "grant": "test_grants",
    "proj": "test_projects",
    "costing": "test_costing",
}


def check_db_connection(data_params):
    retries = 3
    state = False
    while retries > 0:
        try:
            conn = psycopg2.connect(**db_params)
            state = True
            break
        except psycopg2.OperationalError:
            time.sleep(2)  # Wait for 2 seconds before retrying
            retries -= 1
    if state:
        conn.close()
    return state


def setup_user_table_func(data_params):
    utils.create_user_table(tables.get("user"), data_params)
    db = DB(db_params)
    return db


def teardown_user_table_func(data_params):
    return utils.drop_table(tables.get("user"), data_params)


def setup_deployment_table_func(data_params):
    utils.create_deployment_table(tables.get("deploymentid"), data_params)
    db = DB(db_params)
    return db


def teardown_deployment_table_func(data_params):
    return utils.drop_table(tables.get("deploymentid"), data_params)


def setup_grant_table_func(data_params):
    db = DB(db_params)
    if utils.create_user_table(tables.get("user"), data_params):
        if utils.create_grant_table(
            tables.get("grant"), tables.get("user"), data_params
        ):
            return db
    raise DbException("Creation of the grant DB failed.")


def teardown_grant_table_func(data_params):
    result = []
    result.append(utils.drop_table(tables.get("grant"), data_params))
    result.append(utils.drop_table(tables.get("user"), data_params))
    return False not in result


def setup_project_table_func(data_params):
    db = DB(db_params)
    if utils.create_user_table(tables.get("user"), data_params):
        utils.create_project_table(tables.get("proj"), tables.get("user"), data_params)
        return db
    raise DbException("Creation of the purchase order DB failed.")


def teardown_project_table_func(data_params):
    result = []
    result.append(utils.drop_table(tables.get("proj"), data_params))
    result.append(utils.drop_table(tables.get("user"), data_params))
    return False not in result


def setup_costing_table_func(data_params):
    db = DB(db_params)
    if utils.create_user_table(tables.get("user"), data_params):
        if utils.create_deployment_table(tables.get("deploymentid"), data_params):
            if utils.create_project_table(
                tables.get("proj"), tables.get("user"), data_params
            ):
                if utils.create_grant_table(
                    tables.get("grant"), tables.get("user"), data_params
                ):
                    if utils.create_costing_table(
                        tables.get("costing"),
                        tables.get("deploymentid"),
                        tables.get("proj"),
                        tables.get("grant"),
                        data_params,
                    ):
                        return db
    raise DbException("Creation of the costing DB failed.")


def teardown_costing_table_func(data_params):
    result = []
    result.append(utils.drop_table(tables.get("costing"), data_params))
    result.append(utils.drop_table(tables.get("proj"), data_params))
    result.append(utils.drop_table(tables.get("grant"), data_params))
    result.append(utils.drop_table(tables.get("user"), data_params))
    result.append(utils.drop_table(tables.get("deploymentid"), data_params))
    return False not in result
