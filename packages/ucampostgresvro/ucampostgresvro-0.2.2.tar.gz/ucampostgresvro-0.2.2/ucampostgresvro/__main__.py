import logging
import sys

# from datetime import datetime
from ucampostgresvro import VERSION, utils
from ucampostgresvro.DBA import DB
from ucampostgresvro.exceptions import DbException
from ucampostgresvro.secrets import password


def setloggerdetail():
    LOG = logging.getLogger(__name__)
    stdout_handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        handlers=[stdout_handler],
    )
    return LOG


def main():
    LOG = setloggerdetail()
    LOG.info(f"VERSION : {VERSION}")
    db_params = {
        "dbname": "vrapricing",
        "user": "postgres",
        "password": password,
        "host": "infra-db.srv.uis.cam.ac.uk",  # or your database host
        "port": "5432",  # default PostgreSQL port
        "sslmode": "require",  # or 'verify-ca' or 'verify-full' based on your needs
        "sslrootcert": "./ca.crt",  # path to your client certificate
    }
    db = DB(db_params)

    if not utils.pre_setupconfig(db_params):
        raise DbException("ERROR: Tables are not created successfully")

    # print(db.insert_vrauser("ll221", "leny"))
    # print(db.get_vrauser("ll220"))
    # print(db.get_vrauser_primary_key("ll220"))
    # db.update_vrauser("ll220", "bda20", 'Ben Argyle')
    # print(db.get_vrauser())
    # db.remove_vrauser('bda20')
    # print(db.get_vrauser_by_id(2))
    # print(db.get_vrauser())

    # db.insert_deployment_id("1231ee112ad11212")
    # print(db.get_deployment_id("1231ee112ad11212"))
    # print(db.get_deployment_id_primary_key("1231ee112ad11212"))
    # db.update_deployment_id("1231ee112ad11212", "1231a")
    # print(db.get_deployment_id("1231a"))
    # db.remove_deployment_id('1231a')
    # print(db.get_deployment_id())
    # db.insert_deployment_id("123")
    # print(db.get_deployment_id())
    # print(db.get_deployment_id_by_id(2))
    # print(db.get_deployment_id_primary_key("123"))

    # db.insert_project("0101",2,100.0)
    # db.insert_project("0001",2,100.0)
    # print(db.get_project())
    # db.update_project(2, "0002", 2, 200)
    # print(db.get_project())
    # db.remove_project(1)
    # print(db.get_project())
    # db.insert_project("2001",2,100.0)
    # db.insert_project("2003",2,200.0)
    # db.insert_project("2001",2,100.0)
    # print(db.get_project("2001"))
    # print(db.get_project_by_id(6))
    # print(db.get_project_primary_key("2001"))
    # print(db.get_project_primary_key("2001",  datetime(2025, 1, 22, 15, 55, 25, 95698)))
    # print(db.get_project())

    # print(db.get_grant())
    # db.insert_grant("0001",2,100.0)
    # print(db.get_grant())
    # db.update_grant(2, "0002", 2, 200)
    # print(db.get_grant())
    # db.insert_grant("2001",2,100.0)
    # db.insert_grant("2003",2,200.0)
    # db.insert_grant("2001",2,100.0)
    # print(db.get_grant())
    # print(db.get_grant())
    # print(db.get_grant("2001"))
    # print(db.get_grant_primary_key("2001"))
    # print(db.get_grant_by_id(5))
    # print(db.get_grant_primary_key("2001",
    #                                datetime(2025, 1, 22, 18, 17, 25, 95698)
    #                                )
    #       )
    # print(db.get_project())
    # db.remove_grant(1)

    # db.insert_costing(2, "Initial Resource", project_id=2, grant_id=None)
    # db.insert_costing(2, "Initial Resource", project_id=None, grant_id=2)
    # print(db.get_costing())
    # print(db.get_costing())
    # print(db.get_costing(2, "Initial Resource", 2)) # project
    # print(db.get_costing(2, "Initial Resource", None, 2)) # Grant
    # print(db.get_costing(3, "Duration Expansion", None, 2)) # Grant
    # # print(db.get_costing_primary_key(2, "Initial Resource", 2)) # project
    # print(db.get_costing_primary_key(2, "Initial Resource", None, 2)) #Grant
    # db.update_costing(3, 2, "Duration Expansion", new_grant_id=None, new_project_id=2)
    # print(db.get_costing())
    # print(db.get_costing_by_id(3))
    # db.remove_costing(4)
    # print(db.get_costing())

    db.closedb()


if __name__ == "__main__":
    main()
