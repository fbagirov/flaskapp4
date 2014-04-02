from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.social import Social, SQLAlchemyConnectionDatastore

import sys

if not "config" in sys.modules:
    raise Exception(
        "run.py must import config, then import %s" % __name__)

app = Flask('app2')
app.config.from_object('config')
# The 'config' module contains the database configuration, so 
#     app.config.from_object('config')
# must happen before
#     db = SQLAlchemy(app)
# or else SQLAlchemy will create a default in-memory-only db.
db = SQLAlchemy(app)

from . import models, views 

# views contains an @route('/login), and must be imported before 
#     app.security = Security(app, user_datastore)
# or else Security will supply its own /login route.
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
app.security = Security(app, user_datastore)

conn_datastore = SQLAlchemyConnectionDatastore(db, models.Connection)
app.social = Social(app, conn_datastore)

# app.config['SECURITY_POST_LOGIN'] = '/profile'

