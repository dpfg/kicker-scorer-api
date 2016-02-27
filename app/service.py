"""Set of services to do not trivial db operations."""

from app.models import Team, Player, Match
from app import db
from app.util import generate_team_name


class TeamService(object):
    """docstring for TeamService."""

    def find_or_create(community, teamJSON):
        """Find team using provided team json: by name or by players."""
        if 'name' in teamJSON:
            return TeamService.find_by_name(community, teamJSON['name'])
        elif 'goalkeeper' in teamJSON and 'forward' in teamJSON:
            gk_id = teamJSON['goalkeeper']
            fw_id = teamJSON['forward']
            return TeamService.find_by_player_ids(community, gk_id, fw_id)

        return None

    @staticmethod
    def find_by_name(community, name):
        return Team.query.filter_by(community_id=community.id,name=name).first()

    @staticmethod
    def find_by_player_ids(community, gk_id, fw_id):
        team = Team.query \
                    .filter_by(community_id=community.id, goalkeeper_id=gk_id,forward_id=fw_id) \
                    .first()

        if team is not None:
            return team

        gk = PlayerService.find_by_id(gk_id)
        fw = PlayerService.find_by_id(fw_id)

        if gk is None or fw is None:
            return None

        team_name = TeamService.generate_team_name(community)
        return TeamService.create(community, team_name, gk, fw)

    @staticmethod
    def generate_team_name(community):
        rand_name = generate_team_name()
        existed_team = Team.query.filter_by(community_id=community.id, name=rand_name).first()
        if existed_team is None:
            return rand_name
        else:
            generate_team_name(community)

    @staticmethod
    def create(community, name, gk, fw):
        if gk is None or fw is None:
            return None

        team = Team(community, name, fw, gk)
        db.session.add(team)
        db.session.commit()

        return team


class MatchService(object):
    """Layer to access the match's data"""

    @staticmethod
    def get_all(community):
        return Match.query.filter_by(community_id = community.id).order_by(Match.match_datetime.desc())


class PlayerService(object):
    """docstring for PlayerService"""

    @staticmethod
    def find_by_id(player_id):
        return Player.query.filter_by(id=player_id).first()

    def find_by_username(community, name):
        name = name.lower()
        return Player.query.filter_by(community_id=community.id, username=name).first()
