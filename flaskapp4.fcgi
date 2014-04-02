#!/home3/fbagirov/.virtualenvs/linkup/bin/python

from flup.server.fcgi import WSGIServer
import config
from app2 import app as application

WSGIServer(application).run()
