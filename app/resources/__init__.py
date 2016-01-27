from flask_restful import Resource, Api
from flask_jwt import jwt_required
from app.decorators import json_content, community_resource, match_resource

class ProtectedResource(Resource):
    method_decorators = [jwt_required()]

class CommunityBasedResource(ProtectedResource):
    method_decorators = [jwt_required(), community_resource]

class MatchBasedResource(ProtectedResource):
    method_decorators = [jwt_required(), match_resource]
