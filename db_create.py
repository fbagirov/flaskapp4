#!flask/bin/python
# from migrate.versioning import api
# from config import SQLALCHEMY_MIGRATE_REPO

import config
from app2 import db, user_datastore
db.create_all()
# user_datastore.create_user(email='student@school.edu', password='password')
# db.session.commit()
