from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.social import Social, SQLAlchemyConnectionDatastore

import sys

if not "config" in sys.modules:
    raise Exception(
        "run.py must import config, then from %s import *" % __name__)

app = Flask('app2')
app.config.from_object('config')
db=SQLAlchemy(app)

print >>sys.stderr, "Am I here before importing or not?"
from . import models, views 
print >>sys.stderr, "Am I here after importing or not?-2"

user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
app.security = Security(app, user_datastore)

conn_datastore = SQLAlchemyConnectionDatastore(db, models.Connection)
app.social = Social(app, conn_datastore)

# app.config['SECURITY_POST_LOGIN'] = '/profile'

