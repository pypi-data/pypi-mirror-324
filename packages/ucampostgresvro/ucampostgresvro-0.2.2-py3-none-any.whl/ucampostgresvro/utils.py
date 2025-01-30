import logging
from typing import Callable, Dict

from ucampostgresvro.DBA import DB
from ucampostgresvro.exceptions import DbException
from ucampostgresvro.tools import DEFAULT_TABLES

LOG = logging.getLogger(__name__)


def pre_setupconfig(db_params: Dict[str, str]) -> bool:
    """Create the Database

    Args:
        db_params (Dict[str, str]): provide parameters for DB connection.

    Returns:
        bool: True if creation of database is suceess else False
    """
    result = []
    if not check_table_exists(DEFAULT_TABLES.get("user"), db_params):
        result.append(create_user_table(DEFAULT_TABLES.get("user"), db_params))
    if not check_table_exists(DEFAULT_TABLES.get("deploymentid"), db_params):
        result.append(
            create_deployment_table(DEFAULT_TABLES.get("deploymentid"), db_params)
        )
    if not check_table_exists(DEFAULT_TABLES.get("proj"), db_params):
        result.append(
            create_project_table(
                DEFAULT_TABLES.get("proj"), DEFAULT_TABLES.get("user"), db_params
            )
        )
    if not check_table_exists(DEFAULT_TABLES.get("grant"), db_params):
        result.append(
            create_grant_table(
                DEFAULT_TABLES.get("grant"), DEFAULT_TABLES.get("user"), db_params
            )
        )
    if not check_table_exists(DEFAULT_TABLES.get("costing"), db_params):
        result.append(
            create_costing_table(
                DEFAULT_TABLES.get("costing"),
                DEFAULT_TABLES.get("deploymentid"),
                DEFAULT_TABLES.get("proj"),
                DEFAULT_TABLES.get("grant"),
                db_params,
            )
        )
    return False not in result


def create_table(tablename: str, db_params: Dict[str, str], design: str) -> bool:
    """Creation of table with provided design

    Args:
        tablename (str): Name of the table to be created.
        db_params (Dict[str, str]): provide parameters for DB connection
        design (str): design to be created.

    Raises:
        DbException: Exception for the provided inputs.

    Returns:
        bool: True for the success and False for the failure.
    """
    db = DB(db_params)
    conn = db.db_connection()
    cursor = db.db_cursor()
    with conn:
        try:
            cursor.execute(design)
            LOG.info(f"Creation of the table '{tablename}' has been successful.")
            return True
        except Exception as e:
            LOG.error(f"Error: Creation of table '{tablename}' failed: \n {e}")
            raise DbException(f"Error: Creation of table '{tablename}' failed: \n {e}")


def drop_table(tablename: str, db_params: Dict[str, str]) -> bool:
    """Drop the table.

    Args:
        tablename (str): Name of the table to be created.
        db_params (Dict[str, str]): provide parameters for DB connection.

    Raises:
        DbException: Exception for the provided inputs.

    Returns:
        bool: True for the success and False for the failure.
    """
    db = DB(db_params)
    conn = db.db_connection()
    cursor = db.db_cursor()
    with conn:
        try:
            cursor.execute(f'DROP TABLE "{tablename}";')
            LOG.info(f"Drop of the table '{tablename}' has been successful.")
            return True
        except Exception as e:
            LOG.error(f"Error: Drop of table {tablename} failed: \n {e}")
            raise DbException(f"Error: Drop of table {tablename} failed: \n {e}")


def create_user_table(
    tablename: str, db_params: Dict[str, str]
) -> Callable[[str, Dict[str, str], str], bool]:
    """create the user table.

    Args:
        tablename (str): Name of the table to be created.
        db_params (Dict[str, str]): provide parameters for DB connection.

    Returns:
        Callable[[str, Dict[str, str], str], bool]: Invoke the create table function.
    """
    design = f"CREATE TABLE {tablename} (\
        id SERIAL PRIMARY KEY, \
        crsid VARCHAR(255) UNIQUE, \
        name VARCHAR(255)\
        );"
    return create_table(tablename, db_params, design)


def create_deployment_table(tablename: str, db_params: Dict[str, str]) -> Callable:
    """create the deployment table.

    Args:
        tablename (str): Name of the table to be created.
        db_params (Dict[str, str]): provide parameters for DB connection.

    Returns:
        Callable[[str, Dict[str, str], str], bool]: Invoke the create table function.
    """
    design = f"CREATE TABLE {tablename} (id SERIAL PRIMARY KEY, deploymentId VARCHAR(50) UNIQUE);"
    return create_table(tablename, db_params, design)


def create_project_table(
    proj_tablename: str, user_tablename: str, db_params: Dict[str, str]
) -> Callable[[str, Dict[str, str], str], bool]:
    """create the project table.

    Args:
        proj_tablename (str): Name of the project table to be created.
        user_tablename (str): Name of the user table to be referred.
        db_params (Dict[str, str]): provide parameters for DB connection.

    Returns:
        Callable[[str, Dict[str, str], str], bool]: Invoke the create table function.
    """
    design = f"CREATE TABLE {proj_tablename} (\
        id SERIAL PRIMARY KEY, \
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \
        project_number VARCHAR(255), \
        paid_by INTEGER REFERENCES {user_tablename}(id), \
        amount FLOAT NOT NULL \
        );"
    return create_table(proj_tablename, db_params, design)


def create_grant_table(
    grant_tablename: str, user_tablename: str, db_params: Dict[str, str]
) -> Callable[[str, Dict[str, str], str], bool]:
    """create the grant table.

    Args:
        grant_tablename (str): Name of the grant table to be created.
        user_tablename (str): Name of the user table to be referred.
        db_params (Dict[str, str]): provide parameters for DB connection.

    Returns:
        Callable[[str, Dict[str, str], str], bool]: Invoke the create table function.
    """
    design = f"CREATE TABLE {grant_tablename} (\
        id SERIAL PRIMARY KEY,\
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \
        grant_number VARCHAR(255),\
        paid_by INTEGER REFERENCES {user_tablename}(id),\
        amount FLOAT NOT NULL\
        );"
    return create_table(grant_tablename, db_params, design)


def create_costing_table(
    costing_tablename: str,
    deploy_tablename: str,
    proj_tablename: str,
    grant_tablename: str,
    db_params: Dict[str, str],
) -> Callable[[str, Dict[str, str], str], bool]:
    """create the grant table.

    Args:
        costing_tablename (str): Name of the costing table to be created.
        deploy_tablename (str): Name of the deploy table to be referred.
        proj_tablename (str): Name of the project table to be referred.
        grant_tablename (str): Name of the grant table to be referred.
        db_params (Dict[str, str]): provide parameters for DB connection.

    Returns:
        Callable[[str, Dict[str, str], str], bool]: Invoke the create table function.
    """
    design = f"CREATE TABLE {costing_tablename} (\
        id SERIAL PRIMARY KEY,\
        deployment_id INTEGER REFERENCES {deploy_tablename}(id),\
        type VARCHAR(100) CHECK (type IN ('Resource Expansion', 'Duration Expansion', 'Initial Resource')),\
        project_id INTEGER REFERENCES {proj_tablename}(id),\
        grant_id INTEGER REFERENCES {grant_tablename}(id)\
        );"
    return create_table(costing_tablename, db_params, design)


def check_table_exists(table_name: str, db_params: Dict[str, str]) -> bool:
    """Check the status of the table.

    Args:
        table_name (str): Name of the table to be checked.
        db_params (Dict[str, str]): provide parameters for DB connection.

    Raises:
        DbException: Exception for the provided inputs.

    Returns:
        bool: True for the success of table search and False for the failing in table search.
    """
    db = DB(db_params)
    conn = db.db_connection()
    cursor = db.db_cursor()
    with conn:
        try:
            cursor.execute(
                f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}' \
                AND table_schema = 'public')"
            )
            exists = cursor.fetchone()[0]
            LOG.info(f"'{table_name}' status : {exists}")
            return exists
        except Exception as e:
            LOG.error(f"Error: checking of table {table_name} failed: \n {e}")
            raise DbException(f"Error: checking of table '{table_name}' failed: \n {e}")
