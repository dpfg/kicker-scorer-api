import os


# DB settings
db_host = os.getenv('DB_HOST', 'localhost')
db_user = os.getenv('DB_USER', 'root')
db_pwd = os.getenv('DB_PWD', '')
SQLALCHEMY_DATABASE_URI = "mysql://{:s}:{:s}@{:s}:3306/kicker_db".format(db_user, db_pwd, db_host)
SQLALCHEMY_TRACK_MODIFICATIONS = True

# App settings
APPLICATION_ROOT = '/api'
DEBUG = True

# JWT settings
JWT_AUTH_URL_RULE = APPLICATION_ROOT + "/auth"
