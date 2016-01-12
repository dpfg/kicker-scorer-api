"""Application config."""


# DB settings
SQLALCHEMY_DATABASE_URI = 'mysql://root:test@dbserver:3306/kicker_db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
APPLICATION_ROOT = '/api'

DEBUG_MODE = True
