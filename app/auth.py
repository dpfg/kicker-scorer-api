from app import app
from app import models
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import generate_password_hash, check_password_hash


def authenticate(username, password):
    user = models.User.query.filter_by(email=username).first()
    if user and user.check_password(password):
        return user

def identity(payload):
    user_id = payload['identity']
    return models.User.query.get(user_id)

jwt = JWT(app, authenticate, identity)
