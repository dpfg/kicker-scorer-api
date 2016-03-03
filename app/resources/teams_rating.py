from app.resources import CommunityBasedResource
from app.models import Match, Team
from app.statistic import calc_teams_rating
from app import app

class TeamsRatingResource(CommunityBasedResource):

	def get(self, community):
		matches = Match.query.filter_by(completed=True).order_by(Match.match_datetime).all()
		rating = calc_teams_rating(matches)
		team_ids = [m.team0_id for m in matches] + [m.team1_id for m in matches]
		teams = Team.query.filter(Team.id.in_(team_ids)).all()

		return {
			'rating' : [{
				'team' : [t for t in teams if t.id == r[0]][0].serialize,
				'rating': r[1]
			} for r in rating]
		}
