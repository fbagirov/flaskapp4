#!flask/bin/python
# from migrate.versioning import api
# from config import SQLALCHEMY_DATABASE_URI
#from config import SQLALCHEMY_MIGRATE_REPO

import config
from app2 import db
# import os.path
db.create_all()
