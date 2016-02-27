from elo import WIN, DRAW, LOSS, rate
import operator

INITIAL_RATNG = 1000;

def calc_teams_rating(matches):
	team_ratings = {}
	for match in matches:
		blue_team = match.team0_id
		red_team  = match.team1_id

		blue_rating = INITIAL_RATNG
		red_rating  = INITIAL_RATNG

		if blue_team in team_ratings:
			blue_rating = team_ratings[blue_team]

		if red_team in team_ratings:
			red_rating = team_ratings[red_team]

		team_ratings[blue_team] = rate(blue_rating, [(team_match_result(blue_team, match) , red_rating)])
		team_ratings[red_team] = rate(red_rating, [(team_match_result(red_rating, match) , blue_rating)])

	sorted_rating = sorted(team_ratings.items(), key=operator.itemgetter(1))
	sorted_rating.reverse()

	return sorted_rating

def team_match_result(team, match):
	if match.team0_score == match.team1_score:
		return DRAW

	if match.team0_id == team:
		return WIN if match.team0_score > match.team1_score else LOSS
	else:
		return WIN if match.team0_score < match.team1_score else LOSS