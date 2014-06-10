import os.path

SOCIAL_FACEBOOK = {
    'consumer_key': '443393489126475',
    'consumer_secret': 'f91df0b6ad15fc36d3c7c5716333d5c7'
}

SOCIAL_TWITTER = {
    'consumer_key': '4VztQEWr7t2wrXTt2QrA',
    'consumer_secret': 'w98NYd9SfxNkSLYbDejdUjtj4cS0VrfL9nBehiQS9NU'
}


basedir = os.path.abspath(os.path.dirname(__file__))

if basedir.startswith("/Users/steve"):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flaskapp4:flaskapp4@localhost/linkup_db'



