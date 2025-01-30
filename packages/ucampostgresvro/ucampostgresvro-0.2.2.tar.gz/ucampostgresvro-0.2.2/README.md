# Script for VRA database for Costing

# Developing
1. [Install docker-compose](https://docs.docker.com/compose/install/).
2. Docker will run the postgres on port 5455 so, ensure the system has the port available

```
# run pytest testing 
./developer.sh pytest start

# run flake8 testing 
./developer.sh flake8 start 

# delete the testing environment
./developer.sh pytest stop

# delete the flake8 environment
./developer.sh flake8 stop
```


## Package usage

- To setup database 
```
from ucampostgresvro.utils import pre_setupconfig
from ucampostgresvro.DBA import DB
db_params = {
    "dbname": "vrapricing",
    "user": "postgres",
    "password": <1Password: vrapricingpostgres>,
    "host": "infra-db.srv.uis.cam.ac.uk", 
    "port": "5432",
    "sslmode": "require",
    "sslrootcert": "./ca.crt",  # path to your client certificate
}
db = DB(db_params)
pre_setupconfig(db_params)
```
- To perform CRUD operation 
```
from ucampostgresvro.DBA import DB
from datetime import datetime

db_params = {
    "dbname": "vrapricing",
    "user": "postgres",
    "password": <1Password: vrapricingpostgres>,
    "host": "infra-db.srv.uis.cam.ac.uk", 
    "port": "5432",
    "sslmode": "require",
    "sslrootcert": "./ca.crt",  # path to your client certificate
}
db = DB(db_params)

# CRUD on user DB./

# create user
db.insert_vrauser("ll220", "Ling-Yan Lau")

# read user
print(db.get_vrauser())

# read user specific user by crsid
print(db.get_vrauser("ll220"))

# read user specific user by user id
print(db.get_vrauser_by_id(1))

# get the primary key of user using crsid
print(db.get_vrauser_primary_key("ll220"))

# update user
db.update_vrauser("ll220", "bda20", 'Ben Argyle')

# delete user
db.remove_vrauser('bda20')

# create vra deploymentid 
db.insert_deployment_id("1231ee112ad11212")

# read all the vra deployment ids
print(db.get_deployment_id())

# read specific specific deploymentid by deploymentid
print(db.get_deployment_id("1231a"))

# read specific deploymentid by primary key
print(db.get_deployment_id_by_id(1))

# read primary key of specific deploymentid
print(db.get_deployment_id_primary_key("1231a"))

# update vra deployment id
db.update_deployment_id("1231ee112ad1", "1231a")

# delete vra deployment id
db.remove_deployment_id('1231a')

# create project 
db.insert_project("0001",1,100.0)

# read all the projects 
print(db.get_project())

# read specific project
print(db.get_project("0001"))

# read project from the ID
print(db.get_project_by_id(1))

# get the primary key of the project
print(db.get_project_primary_key("001"))

# get the primary key of the project if more than 1 entites using date of insertion.
print(db.get_project_primary_key("001", datetime(2025, 1, 22, 15, 55, 25, 95698)))

# update project with new information 1 is the primary key
db.update_project(1, "0002", 4, 200)

# delete project using primary key of project
# db.remove_project(1)

# create grant 
db.insert_grant("0001",1,100.0)

# read all the grants
print(db.get_grant())

# read specific grant
print(db.get_grant("0001"))

# read grant from the ID
print(db.get_grant_by_id(1))

# get the primary key of the grant
print(db.get_grant_primary_key("001"))

# get the primary key of the grant if more than 1 entites using date of insertion.
print(db.get_grant_primary_key("001", datetime(2025, 1, 22, 15, 55, 25, 95698)))

# update grant with new information 1 is the primary key of grant
db.update_grant(1, "2002", 4, 200)

# delete grant 1 is the primary key of the grant
db.remove_grant(1)

# create costing 
db.insert_costing(2, "Initial Resource", project_id=4, grant_id=None)

# read all the costing 
print(db.get_costing())

# read specific costing using primary key of the costing
print(db.get_costing_by_id(1))

# read specific costing for the project 
print(db.get_costing(2, "Initial Resource", 2))

# read specific costing for the grant 
print(db.get_costing(2, "Initial Resource", None, 2))

# get primary key for the specific costing for the project
print(db.get_costing_primary_key(2, "Initial Resource", 2))

# get primary key for the specific costing for the grant
print(db.get_costing_primary_key(2, "Initial Resource", None, 2))

# update costing where 3 is the primary key of the costing.
db.update_costing(3, 2, "Duration Expansion", new_grant_id=None, new_project_id=2)

# delete costing where 3 is the primary key
db.remove_costing(3)

# to close db connection
db.closedb()
```

---
### Design

![DB Design](./db.jpg "DB design")

## - VRAUSER table 
```
vrapricing=# \d vrauser;
                                    Table "public.vrauser"
 Column |          Type          | Collation | Nullable |               Default
--------+------------------------+-----------+----------+-------------------------------------
 id     | integer                |           | not null | nextval('vrauser_id_seq'::regclass)
 crsid  | character varying(255) |           |          |
 name   | character varying(255) |           |          |
Indexes:
    "vrauser_pkey" PRIMARY KEY, btree (id)
    "vrauser_crsid_key" UNIQUE CONSTRAINT, btree (crsid)
Referenced by:
    TABLE "purchaseorder" CONSTRAINT "purchaseorder_paid_by_fkey" FOREIGN KEY (paid_by) REFERENCES vrauser(id)
    TABLE "grant" CONSTRAINT "grant_paid_by_fkey" FOREIGN KEY (paid_by) REFERENCES vrauser(id)

```

## - VRA Deployment ID tabel 
```
vrapricing=# \d deploymentid;
                                      Table "public.deploymentid"
    Column    |         Type          | Collation | Nullable |                 Default
--------------+-----------------------+-----------+----------+------------------------------------------
 id           | integer               |           | not null | nextval('deploymentid_id_seq'::regclass)
 deploymentid | character varying(50) |           |          |
Indexes:
    "deploymentid_pkey" PRIMARY KEY, btree (id)
    "deploymentid_deploymentid_key" UNIQUE CONSTRAINT, btree (deploymentid)
Referenced by:
    TABLE "costing" CONSTRAINT "costing_deployment_id_fkey" FOREIGN KEY (deployment_id) REFERENCES deploymentid(id)

```

## - project table 
```
vrapricing=# \d projects
                                          Table "public.projects"
     Column     |            Type             | Collation | Nullable |               Default
----------------+-----------------------------+-----------+----------+--------------------------------------
 id             | integer                     |           | not null | nextval('projects_id_seq'::regclass)
 date           | timestamp without time zone |           |          | CURRENT_TIMESTAMP
 project_number | character varying(255)      |           |          |
 paid_by        | integer                     |           |          |
 amount         | double precision            |           | not null |
Indexes:
    "projects_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "projects_paid_by_fkey" FOREIGN KEY (paid_by) REFERENCES vrauser(id)
Referenced by:
    TABLE "costing" CONSTRAINT "costing_project_id_fkey" FOREIGN KEY (project_id) REFERENCES projects(id)
```

## - grants table 
```
vrapricing=# \d grants
                                         Table "public.grants"
    Column    |            Type             | Collation | Nullable |              Default
--------------+-----------------------------+-----------+----------+------------------------------------
 id           | integer                     |           | not null | nextval('grants_id_seq'::regclass)
 date         | timestamp without time zone |           |          | CURRENT_TIMESTAMP
 grant_number | character varying(255)      |           |          |
 paid_by      | integer                     |           |          |
 amount       | double precision            |           | not null |
Indexes:
    "grants_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "grants_paid_by_fkey" FOREIGN KEY (paid_by) REFERENCES vrauser(id)
Referenced by:
    TABLE "costing" CONSTRAINT "costing_grant_id_fkey" FOREIGN KEY (grant_id) REFERENCES grants(id)
```

## - Costing table 
```
vrapricing=# \d costing;
                                       Table "public.costing"
    Column     |          Type          | Collation | Nullable |               Default
---------------+------------------------+-----------+----------+-------------------------------------
 id            | integer                |           | not null | nextval('costing_id_seq'::regclass)
 deployment_id | integer                |           |          |
 type          | character varying(100) |           |          |
 po_number_id  | integer                |           |          |
 voucher_id    | integer                |           |          |
Indexes:
    "costing_pkey" PRIMARY KEY, btree (id)
Check constraints:
    "costing_type_check" CHECK (type::text = ANY (ARRAY['Resource Expansion'::character varying, 'Duration Expansion'::character varying, 'Initial Resource'::character varying]::text[]))
Foreign-key constraints:
    "costing_deployment_id_fkey" FOREIGN KEY (deployment_id) REFERENCES deploymentid(id)
    "costing_po_number_id_fkey" FOREIGN KEY (po_number_id) REFERENCES purchaseorder(id)
    "costing_voucher_id_fkey" FOREIGN KEY (voucher_id) REFERENCES grant(id)

```
