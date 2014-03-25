from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import sys

if not "config" in sys.modules:
    raise Exception(
        "run.py must import config, then from %s import *" % __name__)

app = Flask('app2')
app.config.from_object('config')
db=SQLAlchemy(app)

from app2 import views, models
