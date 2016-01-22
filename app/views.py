from app import app, db
from app.models import *
from app.util import *
from app.decorators import *
from app.service import TeamService, PlayerService, MatchService

from flask import jsonify, request, Blueprint
from flask_jwt import jwt_required, current_identity


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/')
@jwt_required()
def init():
    return jsonify(message='service has been initialized')


@api.route('/communities', methods=['GET'])
@jwt_required()
def get_communities():
    communities = Community.query.all()
    return jsonify(communities=[i.serialize for i in communities])


@api.route('/communities', methods=['POST'])
@jwt_required()
@json_content
def create_community():
    if 'name' not in request.json:
        return jsonify(message="missed required name field"), 400

    community_name = request.json['name']
    if is_not_valid_entity_name(community_name):
        return jsonify(message="invalid name")

    q = Community.query.filter_by(name=community_name)

    if q.count() != 0:
        return jsonify(message="name already used")

    db.session.add(Community(name=community_name, owner=User.query.first()))
    db.session.commit()
    return ""


@api.route('/communities/<community_name>/players', methods=['POST'])
@jwt_required()
@json_content
@community_resource
def create_player(community):
    if 'name' not in request.json:
        return jsonify(message="missing required field: name")

    name = request.json['name'].lower()
    if is_not_valid_entity_name(name):
        return jsonify(message="invalid name")

    q = Player.query.filter_by(username=name)
    if q.count() != 0:
        return jsonify(message="player with this name already exists"), 400

    player = Player(community=community, username=name)
    db.session.add(player)
    db.session.commit()

    return jsonify(username=player.username)


@api.route('/communities/<community_name>/players', methods=['GET'])
@jwt_required()
@community_resource
def get_community_players(community):
    return jsonify(players=[p.serialize for p in community.players])


@api.route('/communities/<community_name>/teams', methods=['GET'])
@jwt_required()
@community_resource
def get_community_teams(community):
    return jsonify(teams=[t.serialize for t in community.teams])


@api.route('/communities/<community_name>/teams', methods=['POST'])
@jwt_required()
@json_content
@community_resource
def create_team(community):
    """Method to create new team in the community.

    Required data:
    - team name ('name')
    - forward username ('forward')
    - goalkeeper username ('goalkeeper')

    If one of those fields is missed error will be returned.
    """
    if 'name' not in request.json:
        return jsonify(message="missing required field: name")

    name = request.json['name'].lower()
    if is_not_valid_entity_name(name):
        return jsonify(message="invalid name")

    q = Team.query.filter_by(community_id=community.id, name=name)
    if q.count() != 0:
        return jsonify(message="team with this name already exists"), 400

    if 'forward' not in request.json:
        return jsonify(message="missing required field: forward")

    forward = PlayerService.find_by_username(community, request.json['forward'])
    if forward is None:
        return jsonify(message="forward not found")

    if 'goalkeeper' not in request.json:
        return jsonify(message="missing required field: forward")

    goalkeeper = PlayerService.find_by_username(community, request.json['goalkeeper'])
    if goalkeeper is None:
        return jsonify(message="goalkeeper not found")

    team = TeamService.create(community, name, goalkeeper, forward)

    return jsonify(team.serialize)


@api.route('/communities/<community_name>/matches', methods=['POST'])
@jwt_required()
@json_content
@community_resource
def create_match(community):
    if 'teams' not in request.json:
        return jsonify(message="missing required dict: teams"), 400
    teams = request.json['teams']

    if not isinstance(teams, list):
        return jsonify(message="missing required dict: teams"), 400

    if len(teams) != 2:
        return jsonify(message="incorrect number of teams"), 400

    team0 = TeamService.find_or_create(community, teams[0])
    if team0 is None:
        return jsonify(message="teams[0]: not found"), 400

    team1 = TeamService.find_or_create(community, teams[1])
    if team1 is None:
        return jsonify(message="teams[1]: not found"), 400

    if team0.id == team1.id:
        return jsonify(message="teams are the same"), 400

    match = Match(community, team0, team1)
    db.session.add(match)
    db.session.commit()

    return jsonify(match.serialize)


@api.route('/communities/<community_name>/matches', methods=['GET'])
@jwt_required()
@community_resource
def get_matches(community):
    # add filtering
    return jsonify(matches=[m.serialize for m in MatchService.get_all(community)])


@api.route('/matches/<match_id>', methods=['GET'])
@jwt_required()
@match_resource
def get_matche_detailes(match):
    # add filtering
    return jsonify(match.serialize)


@api.route('/matches/<match_id>/<team_id>/goal', methods=['POST'])
@jwt_required()
@match_resource
@team_resource
def push_goal(match, team):
    if match.completed:
        return jsonify(message='match is completed'), 400

    goal = match.add_goal(team)
    db.session.add(goal)
    db.session.add(match)

    player_id = request.args.get('player')
    if player_id is not None:
        player = Player.query.get(player_id)
        if player is not None:
            goal.player_id = player_id

    db.session.commit()

    return jsonify(goal.serialize)


@api.route('/goals/<goal_id>', methods=['DELETE'])
@jwt_required()
def delete_goal(goal_id):
    goal = MatchGoal.query.get(goal_id)
    if goal is None:
        return jsonify(message="could not find goal"), 400

    if goal.get_match().completed:
        return jsonify(message='match is completed'), 400

    db.session.delete(goal)
    db.session.commit()

    return ""
