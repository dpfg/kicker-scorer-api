from app.resources import CommunityBasedResource
from flask import jsonify
from app.decorators import json_content
from app.util import is_not_valid_entity_name
from app.models import Player
from app import db

class PlayersResource(CommunityBasedResource):

    def get(self, community):
        return { "players": [p.serialize for p in community.players]}

    @json_content
    def post(self, community):
        if 'name' not in request.json:
            return { "message" : "missing required field: name"}

        name = request.json['name'].lower()
        if is_not_valid_entity_name(name):
            return { "message" : "invalid name"}

        q = Player.query.filter_by(username=name)
        if q.count() != 0:
            return { "message" : "player with this name already exists" }, 400

        player = Player(community=community, username=name)
        db.session.add(player)
        db.session.commit()

        return {"username": player.username}
