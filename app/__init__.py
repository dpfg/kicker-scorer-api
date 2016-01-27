from flask import Flask, jsonify, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from flask.ext.cors import CORS, cross_origin

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config.from_object('config')
app.secret_key = 'some_secret2'

cors = CORS(app)

db = SQLAlchemy(app)


def make_json_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response

for code in default_exceptions.keys():
    app.error_handler_spec[None][code] = make_json_error


from flask_restful import Api
from app.resources.checks import HealthCheck
from app.resources.communities import CommunityResource
from app.resources.matches import MatchResource, CommunityMatchesResource, MatchGoalsResource
from app.resources.players import PlayersResource
from app.resources.teams import TeamsResource
from app.resources.goals import GoalResource

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint)
api.add_resource(HealthCheck, '/health')

api.add_resource(CommunityResource, '/communities')
api.add_resource(PlayersResource, '/communities/<community_name>/players')
api.add_resource(TeamsResource, '/communities/<community_name>/teams')
api.add_resource(CommunityMatchesResource, '/communities/<community_name>/matches')

api.add_resource(MatchResource, '/matches/<match_id>')
api.add_resource(MatchGoalsResource, '/matches/<match_id>/<team_id>/goals')
api.add_resource(GoalResource, '/goals/<goal_id>')

app.register_blueprint(api_blueprint)

from app import models, auth
