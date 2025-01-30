from ucampostgresvro.tests.utils import tables


def test_user_insertion(user_db_fixture):
    db = user_db_fixture
    result = db.insert_vrauser("im530", "Ishan", tables.get("user"))
    info = db.get_vrauser(None, None, tables.get("user"))
    assert len(info) == 1
    assert result


def test_user_update(user_db_fixture):
    db = user_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    result = db.update_vrauser("im530", "ll220", "Len", tables.get("user"))
    info = db.get_vrauser(None, None, tables.get("user"))
    assert len(info) == 1
    assert result
    assert info[0][1] == "ll220"


def test_user_remove(user_db_fixture):
    db = user_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    result = db.remove_vrauser("im530", tables.get("user"))
    info = db.get_vrauser(None, None, tables.get("user"))
    assert len(info) == 0
    assert result


def test_user_fetchall(user_db_fixture):
    db = user_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    db.insert_vrauser("im532", "Ishan", tables.get("user"))
    info = db.get_vrauser(None, None, tables.get("user"))
    assert len(info) == 2
    assert info[0][1] == "im530"
    assert info[1][1] == "im532"


def test_user_fetch_by_id(user_db_fixture):
    db = user_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    db.insert_vrauser("im532", "Ishan", tables.get("user"))
    info = db.get_vrauser_by_id(2, tables.get("user"))
    assert info[1] == "im532"


def test_user_fetch_one(user_db_fixture):
    db = user_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    db.insert_vrauser("im532", "Ishan", tables.get("user"))
    info = db.get_vrauser("im530", None, tables.get("user"))
    assert len(info) == 1
    assert info[0][1] == "im530"


def test_user_fetch_primary_key_crsid(user_db_fixture):
    db = user_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    db.insert_vrauser("im532", "Ishan", tables.get("user"))
    info = db.get_vrauser_primary_key("im532", tables.get("user"))
    assert info == 2


def test_deployment_insertion(deploymentid_db_fixture):
    db = deploymentid_db_fixture
    result = db.insert_deployment_id("121212", tables.get("deploymentid"))
    info = db.get_deployment_id(None, tables.get("deploymentid"))
    assert len(info) == 1
    assert result


def test_deployment_update(deploymentid_db_fixture):
    db = deploymentid_db_fixture
    db.insert_deployment_id("12345", tables.get("deploymentid"))
    result = db.update_deployment_id("12345", "9876", tables.get("deploymentid"))
    info = db.get_deployment_id(None, tables.get("deploymentid"))
    assert len(info) == 1
    assert result
    assert info[0][1] == "9876"


def test_deployment_remove(deploymentid_db_fixture):
    db = deploymentid_db_fixture
    db.insert_deployment_id("121212", tables.get("deploymentid"))
    result = db.remove_deployment_id("121212", tables.get("deploymentid"))
    info = db.get_deployment_id(None, tables.get("deploymentid"))
    assert len(info) == 0
    assert result


def test_deployment_fetchall(deploymentid_db_fixture):
    db = deploymentid_db_fixture
    db.insert_deployment_id("1212", tables.get("deploymentid"))
    db.insert_deployment_id("1256", tables.get("deploymentid"))
    info = db.get_deployment_id(None, tables.get("deploymentid"))
    assert len(info) == 2
    assert info[0][1] == "1212"
    assert info[1][1] == "1256"


def test_deployment_fetch_by_id(deploymentid_db_fixture):
    db = deploymentid_db_fixture
    db.insert_deployment_id("1212", tables.get("deploymentid"))
    db.insert_deployment_id("1256", tables.get("deploymentid"))
    info = db.get_deployment_id_by_id(2, tables.get("deploymentid"))
    assert info[1] == "1256"


def test_deployment_fetch_one(deploymentid_db_fixture):
    db = deploymentid_db_fixture
    db.insert_deployment_id("1212", tables.get("deploymentid"))
    db.insert_deployment_id("1256", tables.get("deploymentid"))
    info = db.get_deployment_id("1256", tables.get("deploymentid"))
    assert len(info) == 1
    assert info[0][1] == "1256"


def test_deployment_fetch_primary_key_deployment(deploymentid_db_fixture):
    db = deploymentid_db_fixture
    db.insert_deployment_id("1212", tables.get("deploymentid"))
    db.insert_deployment_id("1256", tables.get("deploymentid"))
    info = db.get_deployment_id_primary_key("1256", tables.get("deploymentid"))
    assert info == 2


def test_proj_insertion(project_db_fixture):
    db = project_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    users = db.get_vrauser(None, None, tables.get("user"))
    result = db.insert_project("123abc", users[0][0], 100.0, tables.get("proj"))
    info = db.get_project(None, tables.get("proj"))
    assert len(info) == 1
    assert result


def test_proj_update(project_db_fixture):
    db = project_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    users = db.get_vrauser(None, None, tables.get("user"))
    db.insert_project("123abc", users[0][0], 100.0, tables.get("proj"))
    result = db.update_project(
        1, "9876xyz", users[0][0], 220.0, tables.get("proj")
    )
    info = db.get_project(None, tables.get("proj"))
    assert len(info) == 1
    assert result
    assert info[0][2] == "9876xyz"
    assert info[0][4] == 220.0


def test_proj_remove(project_db_fixture):
    db = project_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    users = db.get_vrauser(None, None, tables.get("user"))
    db.insert_project("123abc", users[0][0], 100.0, tables.get("proj"))
    prj = db.get_project(None, tables.get("proj"))
    result = db.remove_project(prj[0][0], tables.get("proj"))
    info = db.get_project(None, tables.get("proj"))
    assert result
    assert len(info) == 0


def test_proj_fetchall(project_db_fixture):
    db = project_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    users = db.get_vrauser(None, None, tables.get("user"))
    db.insert_project("123abc", users[0][0], 100.0, tables.get("proj"))
    db.insert_project("123xyz", users[0][0], 200.0, tables.get("proj"))
    info = db.get_project(None, tables.get("proj"))
    assert len(info) == 2
    assert info[0][2] == "123abc"
    assert info[1][2] == "123xyz"


def test_proj_fetch_one(project_db_fixture):
    db = project_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    users = db.get_vrauser(None, None, tables.get("user"))
    db.insert_project("123abc", users[0][0], 100.0, tables.get("proj"))
    db.insert_project("123xyz", users[0][0], 200.0, tables.get("proj"))
    info = db.get_project("123xyz", tables.get("proj"))
    assert len(info) == 1
    assert info[0][2] == "123xyz"


def test_proj_fetch_by_id(project_db_fixture):
    db = project_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    users = db.get_vrauser(None, None, tables.get("user"))
    db.insert_project("123abc", users[0][0], 100.0, tables.get("proj"))
    db.insert_project("123xyz", users[0][0], 200.0, tables.get("proj"))
    info = db.get_project_by_id(2, tables.get("proj"))
    assert info[2] == "123xyz"


def test_proj_fetch_primary_key(project_db_fixture):
    db = project_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    users = db.get_vrauser(None, None, tables.get("user"))
    db.insert_project("123abc", users[0][0], 100.0, tables.get("proj"))
    db.insert_project("123xyz", users[0][0], 200.0, tables.get("proj"))
    info = db.get_project_primary_key("123xyz", None, tables.get("proj"))
    assert info == 2


def test_grant_insertion(grant_db_fixture):
    db = grant_db_fixture
    result = db.insert_vrauser("im530", "Ishan", "test_user")
    users = db.get_vrauser(None, None, tables.get("user"))
    result = db.insert_grant("123zyx", users[0][0], 200.0, tables.get("grant"))
    info = db.get_grant(None, tables.get("grant"))
    assert len(info) == 1
    assert result


def test_grant_update(grant_db_fixture):
    db = grant_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    users = db.get_vrauser(None, None, tables.get("user"))
    db.insert_grant("123abc", users[0][0], 100.0, tables.get("grant"))
    result = db.update_grant(
        1, "9876xyz", users[0][0], 220.0, tables.get("grant")
    )
    info = db.get_grant(None, tables.get("grant"))
    assert len(info) == 1
    assert result
    assert info[0][2] == "9876xyz"
    assert info[0][4] == 220.0


def test_grant_remove(grant_db_fixture):
    db = grant_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    users = db.get_vrauser(None, None, tables.get("user"))
    db.insert_grant("123abc", users[0][0], 100.0, tables.get("grant"))
    result = db.remove_grant(1, tables.get("grant"))
    info = db.get_grant(None, tables.get("grant"))
    assert len(info) == 0
    assert result


def test_grant_fetchall(grant_db_fixture):
    db = grant_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    users = db.get_vrauser(None, None, tables.get("user"))
    db.insert_grant("123abc", users[0][0], 100.0, tables.get("grant"))
    db.insert_grant("123xyz", users[0][0], 200.0, tables.get("grant"))
    info = db.get_grant(None, tables.get("grant"))
    assert len(info) == 2
    assert info[0][2] == "123abc"
    assert info[1][2] == "123xyz"


def test_grant_fetch_one(grant_db_fixture):
    db = grant_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    users = db.get_vrauser(None, None, tables.get("user"))
    db.insert_grant("123abc", users[0][0], 100.0, tables.get("grant"))
    db.insert_grant("123xyz", users[0][0], 200.0, tables.get("grant"))
    info = db.get_grant("123xyz", tables.get("grant"))
    assert len(info) == 1
    assert info[0][2] == "123xyz"


def test_grant_fetch_by_id(grant_db_fixture):
    db = grant_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    users = db.get_vrauser(None, None, tables.get("user"))
    db.insert_grant("123abc", users[0][0], 100.0, tables.get("grant"))
    db.insert_grant("123xyz", users[0][0], 200.0, tables.get("grant"))
    info = db.get_grant_by_id(2, tables.get("grant"))
    assert info[2] == "123xyz"


def test_grant_primary_key(grant_db_fixture):
    db = grant_db_fixture
    db.insert_vrauser("im530", "Ishan", tables.get("user"))
    users = db.get_vrauser(None, None, tables.get("user"))
    db.insert_grant("123abc", users[0][0], 100.0, tables.get("grant"))
    db.insert_grant("123xyz", users[0][0], 200.0, tables.get("grant"))
    info = db.get_grant_primary_key("123xyz", None, tables.get("grant"))
    assert info == 2


def test_costing_insertion(costing_db_fixture):
    db = costing_db_fixture
    db.insert_vrauser("im530", "Ishan", "test_user")
    users = db.get_vrauser(None, None, tables.get("user"))

    db.insert_deployment_id("121212", tables.get("deploymentid"))
    deploy = db.get_deployment_id(None, tables.get("deploymentid"))

    db.insert_project("123abc", users[0][0], 100.0, tables.get("proj"))
    proj = db.get_project(None, tables.get("proj"))

    result = db.insert_costing(
        deploy[0][0], "Resource Expansion", proj[0][0], None, tables.get("costing")
    )
    info = db.get_costing(None, None, None, None, tables.get("costing"))
    assert len(info) == 1
    assert result


def test_costing_update(costing_db_fixture):
    db = costing_db_fixture
    db.insert_vrauser("im530", "Ishan", "test_user")
    users = db.get_vrauser(None, None, tables.get("user"))

    db.insert_deployment_id("121212", tables.get("deploymentid"))
    deploy = db.get_deployment_id(None, tables.get("deploymentid"))

    db.insert_project("123abc", users[0][0], 100.0, tables.get("proj"))
    proj = db.get_project(None, tables.get("proj"))

    db.insert_grant("998zxc", users[0][0], 100.0, tables.get("grant"))
    grant = db.get_grant(None, tables.get("grant"))

    db.insert_costing(
        deploy[0][0], "Resource Expansion", proj[0][0], None, tables.get("costing")
    )

    result = db.update_costing(
        1,
        deploy[0][0],
        "Resource Expansion",
        grant[0][0],
        None,
        tables.get("costing"),
    )

    info = db.get_costing(None, None, None, None, tables.get("costing"))
    assert len(info) == 1
    assert result
    assert info[0][4] == 1


def test_costing_remove(costing_db_fixture):
    db = costing_db_fixture
    db.insert_vrauser("im530", "Ishan", "test_user")
    users = db.get_vrauser(None, None, tables.get("user"))

    db.insert_deployment_id("121212", tables.get("deploymentid"))
    deploy = db.get_deployment_id(None, tables.get("deploymentid"))

    db.insert_project("123abc", users[0][0], 100.0, tables.get("proj"))
    proj = db.get_project(None, tables.get("proj"))

    db.insert_costing(
        deploy[0][0], "Resource Expansion", proj[0][0], None, tables.get("costing")
    )

    result = db.remove_costing(1, tables.get("costing"))

    info = db.get_costing(None, None, None, None, tables.get("costing"))
    assert len(info) == 0
    assert result


def test_costing_fetchall(costing_db_fixture):
    db = costing_db_fixture
    db.insert_vrauser("im530", "Ishan", "test_user")
    users = db.get_vrauser(None, None, tables.get("user"))

    db.insert_deployment_id("121212", tables.get("deploymentid"))
    deploy = db.get_deployment_id(None, tables.get("deploymentid"))

    db.insert_project("123abc", users[0][0], 100.0, tables.get("proj"))
    proj = db.get_project(None, tables.get("proj"))

    db.insert_costing(
        deploy[0][0], "Resource Expansion", proj[0][0], None, tables.get("costing")
    )
    db.insert_costing(
        deploy[0][0], "Duration Expansion", proj[0][0], None, tables.get("costing")
    )

    info = db.get_costing(None, None, None, None, tables.get("costing"))
    assert len(info) == 2
    assert info[0][2] == "Resource Expansion"
    assert info[1][2] == "Duration Expansion"


def test_costing_fetch_one(costing_db_fixture):
    db = costing_db_fixture
    db.insert_vrauser("im530", "Ishan", "test_user")
    users = db.get_vrauser(None, None, tables.get("user"))

    db.insert_deployment_id("121212", tables.get("deploymentid"))
    deploy = db.get_deployment_id(None, tables.get("deploymentid"))

    db.insert_project("123abc", users[0][0], 100.0, tables.get("proj"))
    proj = db.get_project(None, tables.get("proj"))

    db.insert_costing(
        deploy[0][0], "Resource Expansion", proj[0][0], None, tables.get("costing")
    )
    db.insert_costing(
        deploy[0][0], "Duration Expansion", proj[0][0], None, tables.get("costing")
    )

    info = db.get_costing(
        deploy[0][0], "Duration Expansion", proj[0][0], None, tables.get("costing")
    )
    assert len(info) == 1
    assert info[0][2] == "Duration Expansion"


def test_costing_fetch_by_id(costing_db_fixture):
    db = costing_db_fixture
    db.insert_vrauser("im530", "Ishan", "test_user")
    users = db.get_vrauser(None, None, tables.get("user"))

    db.insert_deployment_id("121212", tables.get("deploymentid"))
    deploy = db.get_deployment_id(None, tables.get("deploymentid"))

    db.insert_project("123abc", users[0][0], 100.0, tables.get("proj"))
    proj = db.get_project(None, tables.get("proj"))

    db.insert_costing(
        deploy[0][0], "Duration Expansion", proj[0][0], None, tables.get("costing")
    )

    info = db.get_costing_by_id(1, tables.get("costing"))
    assert info[1] == deploy[0][0]
    assert info[2] == "Duration Expansion"
    assert info[3] == proj[0][0]


def test_costing_fetch_primary_key(costing_db_fixture):
    db = costing_db_fixture
    db.insert_vrauser("im530", "Ishan", "test_user")
    users = db.get_vrauser(None, None, tables.get("user"))

    db.insert_deployment_id("121212", tables.get("deploymentid"))
    deploy = db.get_deployment_id(None, tables.get("deploymentid"))

    db.insert_project("123abc", users[0][0], 100.0, tables.get("proj"))
    proj = db.get_project(None, tables.get("proj"))

    db.insert_costing(
        deploy[0][0], "Duration Expansion", proj[0][0], None, tables.get("costing")
    )

    info = db.get_costing_primary_key(deploy[0][0], "Duration Expansion", proj[0][0], None, tables.get("costing"))
    assert info == 1
