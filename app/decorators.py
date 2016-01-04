
from functools import wraps
from flask import g, request, redirect, url_for, jsonify

from app.models import Community, Team, Match
from app import app


def json_content(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.json is None:
            return "", 415, {'Content-Type': 'application/json; charset=utf-8'}
        return f(*args, **kwargs)
    return decorated_function


def community_resource(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        community_name = kwargs['community_name']
        community = Community.query.filter_by(name=community_name).first()
        if community is None:
            return "", 404

        kwargs['community'] = community
        kwargs.pop('community_name')
        return f(*args, **kwargs)
    return decorated_function


def team_resource(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        team_id = kwargs['team_id']
        team = Team.query.get(team_id)
        if team is None:
            return "", 404

        kwargs['team'] = team
        kwargs.pop('team_id')

        return f(*args, **kwargs)
    return decorated_function


def match_resource(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        match_id = kwargs['match_id']
        match = Match.query.get(match_id)
        if match is None:
            return "", 404

        kwargs['match'] = match
        kwargs.pop('match_id')

        return f(*args, **kwargs)
    return decorated_function
