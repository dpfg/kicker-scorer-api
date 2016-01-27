from app.resources import CommunityBasedResource
from flask import jsonify
from app.decorators import json_content
from app.util import is_not_valid_entity_name
from app.models import Team, Player
from app.service import PlayerService, TeamService
from app import db

class TeamsResource(CommunityBasedResource):

    def get(self, community):
        return { "teams": [t.serialize for t in community.teams] }

    @json_content
    def post(self, community):
        """Method to create new team in the community.

        Required data:
        - team name ('name')
        - forward username ('forward')
        - goalkeeper username ('goalkeeper')

        If one of those fields is missed error will be returned.
        """
        if 'name' not in request.json:
            return { "message": "missing required field: name" }

        name = request.json['name'].lower()
        if is_not_valid_entity_name(name):
            return { "message": "invalid name" }

        q = Team.query.filter_by(community_id=community.id, name=name)
        if q.count() != 0:
            return { "message": "team with this name already exists" }, 400

        if 'forward' not in request.json:
            return { "message" : "missing required field: forward" }

        forward = PlayerService.find_by_username(community, request.json['forward'])
        if forward is None:
            return { "message": "forward not found" }

        if 'goalkeeper' not in request.json:
            return { "message" : "missing required field: forward" }

        goalkeeper = PlayerService.find_by_username(community, request.json['goalkeeper'])
        if goalkeeper is None:
            return { "message": "goalkeeper not found" }

        team = TeamService.create(community, name, goalkeeper, forward)

        return team.serialize
