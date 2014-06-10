import sys, os
from sys import stderr

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.social import Social, SQLAlchemyConnectionDatastore
from flask.ext.openid import OpenID
from flask.ext.login import LoginManager

if not "config" in sys.modules:
    raise Exception(
        "run.py must import config, then import %s" % __name__)

import config

app = Flask('app2')

# config.from_object only loads capitalized variables.  It's only meant to load the
# defaults.  
app.config.from_object('config')
# But, we have put actual values in ours, in particular, basedir:
app.config["basedir"] = config.basedir
app.config.basedir = config.basedir

# from
# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(app.config.basedir, 'tmp'))

# The 'config' module contains the database configuration, so 
#     app.config.from_object('config')
# must happen before
#     db = SQLAlchemy(app)
# or else SQLAlchemy will create a default in-memory-only db.
db = SQLAlchemy(app)

from . import models

user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
conn_datastore = SQLAlchemyConnectionDatastore(db, models.Connection)


# views contains an @route('/login), and must be imported before ...
from . import views
#     ... before app.security = Security(app, user_datastore)
# or else Security will supply its own /login route.
app.security = Security(app, user_datastore)


app.social = Social(app, conn_datastore)

# app.config['SECURITY_POST_LOGIN'] = '/profile'


