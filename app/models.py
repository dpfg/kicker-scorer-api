from app import db, app
from app.util import dump_datetime


class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    owner_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.TIMESTAMP, server_default=db.text(
        'UTC_TIMESTAMP ON UPDATE UTC_TIMESTAMP'))

    players = db.relationship('Player', backref='Community',
                              lazy='dynamic',
                              primaryjoin="Player.community_id==Community.id",
                              foreign_keys="Player.community_id",
                              passive_deletes='all')

    teams = db.relationship('Team', backref='Community',
                            lazy='dynamic',
                            primaryjoin="Team.community_id==Community.id",
                            foreign_keys="Team.community_id",
                            passive_deletes='all')

    matches = db.relationship('Match', backref='Community',
                              lazy='dynamic',
                              primaryjoin="Match.community_id==Community.id",
                              foreign_keys="Match.community_id",
                              passive_deletes='all')

    def __init__(self, name, owner):
        self.name = name
        self.owner_id = owner.id

    @property
    def serialize(self):
        return {
            'id'		: self.id,
            'name'  	: self.name,
            'created'	: dump_datetime(self.created)
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    communities = db.relationship('Community', backref='User',
                                  lazy='dynamic',
                                  primaryjoin="User.id==Community.owner_id",
                                  foreign_keys=[
                                      Community.__table__.c.owner_id],
                                  passive_deletes='all')

    created = db.Column(db.TIMESTAMP, server_default=db.text(
        'UTC_TIMESTAMP ON UPDATE UTC_TIMESTAMP'))

    def __init__(self, email):
        self.email = email


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, nullable=False, index=True)
    username = db.Column(db.String(100), nullable=False)
    created = db.Column(db.TIMESTAMP, server_default=db.text(
        'UTC_TIMESTAMP ON UPDATE UTC_TIMESTAMP'))

    def __init__(self, community, username):
        self.username = username
        self.community_id = community.id

    @property
    def serialize(self):
        return {
            'id'		: self.id,
            'username' 	: self.username
        }


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    forward_id = db.Column(db.Integer, nullable=False)
    goalkeeper_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.TIMESTAMP, server_default=db.text(
        'UTC_TIMESTAMP ON UPDATE UTC_TIMESTAMP'))

    def __init__(self, community, name, forward, goalkeeper):
        self.community_id = community.id
        self.name = name
        self.forward_id = forward.id
        self.goalkeeper_id = goalkeeper.id

    @property
    def serialize(self):
        return {
            'id'			: self.id,
            'name'			: self.name,
            # change to join and single query
            'forward'  		: Player.query.get(self.forward_id).serialize,
            # change to join and single query
            'goalkeeper'	: Player.query.get(self.goalkeeper_id).serialize
        }


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, nullable=False, index=True)
    match_datetime = db.Column(db.TIMESTAMP, server_default=db.text(
        'UTC_TIMESTAMP ON UPDATE UTC_TIMESTAMP'))
    team0_id = db.Column(db.Integer, nullable=False)
    team1_id = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    goals = db.relationship('MatchGoal', backref='Match',
                            lazy='dynamic',
                            primaryjoin="MatchGoal.match_id==Match.id",
                            foreign_keys="MatchGoal.match_id",
                            passive_deletes='all')

    def __init__(self, community, team0, team1):
        self.community_id = community.id
        self.team0_id = team0.id
        self.team1_id = team1.id

    def add_goal(self, team):
        goals = db.session \
                    .query(MatchGoal.match_id, 'team_id', db.func.count(MatchGoal.id)) \
                    .filter_by(match_id=self.id).group_by('team_id').all()

        for team_goals in goals:
            if team_goals[2] == 9 and team_goals[1] == team.id:
                self.completed = True
        return MatchGoal(self.community_id, self.id, team.id)

    @property
    def serialize(self):
        teams = Team.query.filter(Team.id.in_(
            [self.team0_id, self.team1_id])).all()
        goals = self.goals.all()
        team0_goals = [g for g in goals if g.team_id == self.team0_id]
        team1_goals = [g for g in goals if g.team_id == self.team1_id]

        return {
            'id': self.id,
            'date': dump_datetime(self.match_datetime),
            'teams': ([t.serialize for t in teams]),
            'score': {
                teams[0].id: len(team0_goals),
                teams[1].id: len(team1_goals)
                },
            'goals': ([g.serialize for g in goals]),
            'completed': self.completed
        }


class MatchGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, nullable=False, index=True)
    match_id = db.Column(db.Integer, nullable=False)
    team_id = db.Column(db.Integer, nullable=False)
    player_id = db.Column(db.Integer, nullable=True)

    created = db.Column(db.TIMESTAMP, server_default=db.text(
        'UTC_TIMESTAMP ON UPDATE UTC_TIMESTAMP'))

    def __init__(self, community, match, team, player):
        self.community_id = community.id
        self.match_id = match.id
        self.team_id = team.id
        if player is not None:
            self.player_id = player.id

    def __init__(self, community_id, match_id, team_id):
        self.community_id = community_id
        self.match_id = match_id
        self.team_id = team_id

    def get_player(self):
        return Player.query.get(self.player_id)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'team_id': self.team_id,
            'player_id': self.player_id,
            'match_id': self.match_id,
            'created': dump_datetime(self.created)
        }
