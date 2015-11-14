from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config.from_object('config')

app.secret_key = 'some_secret'

db = SQLAlchemy(app)


def make_json_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response

for code in default_exceptions.keys():
    app.logger.debug("register" + str(code))
    app.error_handler_spec[None][code] = make_json_error

from app import views, models
