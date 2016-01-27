from app.resources import ProtectedResource
from flask import jsonify
from app.models import Community
from app.util import is_not_valid_entity_name
from app.decorators import json_content
from app import db, app

class CommunityResource(ProtectedResource):

    def get(self):
        communities = Community.query.all()
        return { 'communities' : [i.serialize for i in communities] }

    @json_content
    def post(self):
        if 'name' not in request.json:
            return { 'message' : "missed required name field"}, 400

        community_name = request.json['name']
        if is_not_valid_entity_name(community_name):
            return { 'message' : "invalid name" }

        q = Community.query.filter_by(name=community_name)

        if q.count() != 0:
            return { 'message' : "name already used" }

        db.session.add(Community(name=community_name, owner=User.query.first()))
        db.session.commit()
        return ""
