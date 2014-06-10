#!flask/bin/python
from sys import argv, stderr

import config
from app2 import app
app.stderr = stderr
if argv[1:] and argv[1] == "--public":
    app.run(host="0.0.0.0")
else:
    app.run(debug=True)
