"""Set of services to do not trivial db operations."""

from app.models import Team, Player
from app import db


class TeamService(object):
    """docstring for TeamService."""

    def findOrCreate(community, teamJSON):
        """Find team using provided team json: by name or by players."""
        if 'name' in teamJSON:
            return TeamService.findByName(community, teamJSON['name'])
        elif 'goalkeeper' in teamJSON and 'forward' in teamJSON:
            gk_id = teamJSON['goalkeeper']
            fw_id = teamJSON['forward']
            return TeamService.findByPlayerIds(community, gk_id, fw_id)

        return None

    @staticmethod
    def findByName(community, name):
        return Team.query.filter_by(
                        community_id=community.id,
                        name=name).first()

    @staticmethod
    def findByPlayerIds(community, gk_id, fw_id):
        team = Team.query.filter_by(
            community_id=community.id,
            goalkeeper_id=gk_id,
            forward_id=fw_id).first()

        if team is not None:
            return team

        gk = PlayerService.findById(gk_id)
        fw = PlayerService.findById(fw_id)

        if gk is None or fw is None:
            return None

        return TeamService.create(community, "ag:", gk, fw)

    @staticmethod
    def create(community, name, gk, fw):
        if gk is None or fw is None:
            return None

        team = Team(community, name, fw, gk)
        db.session.add(team)
        db.session.commit()

        return team


class PlayerService(object):
    """docstring for PlayerService"""

    @staticmethod
    def findById(player_id):
        return Player.query.filter_by(id=player_id).first()

    def findByUsername(community, name):
        name = name.lower()
        return Player.query.filter_by(community_id=community.id, username=name).first()
