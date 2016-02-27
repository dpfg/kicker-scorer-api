from app.resources import MatchBasedResource, CommunityBasedResource
from flask import jsonify, request
from app.decorators import json_content, team_resource
from app.service import TeamService, MatchService
from app.models import Match, Player
from app import db

# /matches/:id
class MatchResource(MatchBasedResource):

    def get(self, match):
        return jsonify(match.serialize)

# /communities/:name/matches
class CommunityMatchesResource(CommunityBasedResource):

    def get(self, community):
        return {"matches": [m.serialize for m in MatchService.get_all(community)]}

    @json_content
    def post(self, community):
        if 'teams' not in request.json:
            return { "message" : "missing required dict: teams"}, 400
        teams = request.json['teams']

        if not isinstance(teams, list):
            return { "message" : "missing required dict: teams"}, 400

        if len(teams) != 2:
            return { "message" : "incorrect number of teams"}, 400

        team0 = TeamService.find_or_create(community, teams[0])
        if team0 is None:
            return { "message" : "teams[0]: not found"}, 400

        team1 = TeamService.find_or_create(community, teams[1])
        if team1 is None:
            return { "message" : "teams[1]: not found"}, 400

        if team0.id == team1.id:
            return { "message" : "teams are the same"}, 400

        match = Match.create(community, team0, team1)
        db.session.add(match)
        db.session.commit()

        return match.serialize

# /matches/:id/goals
class MatchGoalsResource(MatchBasedResource):

    @team_resource
    def post(self, match, team):
        if match.completed:
            return { 'message' : 'match is completed' }, 400

        goal = match.add_goal(team)
        db.session.add(goal)
        db.session.add(match)

        player_id = request.args.get('player')
        if player_id is not None:
            player = Player.query.get(player_id)
            if player is not None:
                goal.player_id = player_id

        db.session.commit()

        return goal.serialize
