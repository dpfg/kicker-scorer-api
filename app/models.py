from app import db, app
from app.util import dump_datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    owner_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.TIMESTAMP, server_default=db.text(
        'UTC_TIMESTAMP ON UPDATE UTC_TIMESTAMP'))

    players = db.relationship('Player',
                                backref='Community',
                                lazy='dynamic',
                                primaryjoin="Player.community_id==Community.id",
                                foreign_keys="Player.community_id")

    teams = db.relationship('Team', backref='Community',
                                lazy='dynamic',
                                primaryjoin="Team.community_id==Community.id",
                                foreign_keys="Team.community_id")

    matches = db.relationship('Match', backref='Community',
                                lazy='dynamic',
                                primaryjoin="Match.community_id==Community.id",
                                foreign_keys="Match.community_id")

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
    password_hash = db.Column(db.String(300))
    communities = db.relationship('Community', backref='User',
                                  lazy='dynamic',
                                  primaryjoin="User.id==Community.owner_id",
                                  foreign_keys=[
                                      Community.__table__.c.owner_id],
                                  passive_deletes='all')

    created = db.Column(db.TIMESTAMP, server_default=db.text('UTC_TIMESTAMP ON UPDATE UTC_TIMESTAMP'))

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, nullable=False, index=True)
    username = db.Column(db.String(100), nullable=False)
    created = db.Column(db.TIMESTAMP, server_default=db.text('UTC_TIMESTAMP ON UPDATE UTC_TIMESTAMP'))

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

    forward = db.relationship('Player',
                            lazy='joined',
                            primaryjoin="Player.id==Team.forward_id",
                            foreign_keys="Player.id",
                            uselist=False)

    goalkeeper = db.relationship('Player',
                            lazy='joined',
                            primaryjoin="Player.id==Team.goalkeeper_id",
                            foreign_keys="Player.id",
                            uselist=False)

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
            'forward'  		: self.forward.serialize,
            'goalkeeper'	: self.goalkeeper.serialize
        }


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, nullable=False, index=True)
    match_datetime = db.Column(db.TIMESTAMP, server_default=db.text(
        'UTC_TIMESTAMP ON UPDATE UTC_TIMESTAMP'))
    team0_id = db.Column(db.Integer, nullable=False)
    team1_id = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    goals = db.relationship('MatchGoal', backref='Match', lazy='joined', primaryjoin="MatchGoal.match_id==Match.id",foreign_keys="MatchGoal.match_id", order_by="MatchGoal.id")
    team0 = db.relationship('Team', lazy='joined', primaryjoin='Team.id==Match.team0_id', foreign_keys='Team.id', uselist=False)
    team1 = db.relationship('Team', lazy='joined', primaryjoin='Team.id==Match.team1_id', foreign_keys='Team.id', uselist=False)

    @classmethod
    def create(cls, community, team0, team1):
        match = cls()
        match.community_id = community.id
        match.team0_id = team0.id
        match.team1_id = team1.id
        return match

    def add_goal(self, team):
        goals = db.session \
                    .query(MatchGoal.match_id, 'team_id', db.func.count(MatchGoal.id)) \
                    .filter_by(match_id=self.id) \
					.group_by('team_id').all()

        for team_goals in goals:
            if team_goals[2] == 9 and team_goals[1] == team.id:
                self.completed = True
        return MatchGoal(self.community_id, self.id, team.id)

    @property
    def team0_score(self):
        return len(self.team0_goals)

    @property
    def team1_score(self):
        return len(self.team1_goals)

    @property
    def	team0_goals(self):
        return [g for g in self.goals if g.team_id == self.team0_id]

    @property
    def	team1_goals(self):
        return [g for g in self.goals if g.team_id == self.team1_id]

    @property
    def serialize(self):
        goals = self.goals

        return {
            'id': self.id,
            'date': dump_datetime(self.match_datetime),
            'teams': [self.team0.serialize, self.team1.serialize],
            'score': {
                self.team0.id: self.team0_score,
                self.team1.id: self.team1_score
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

    created = db.Column(db.TIMESTAMP, server_default=db.text('UTC_TIMESTAMP ON UPDATE UTC_TIMESTAMP'))

    def __init__(self, community_id, match_id, team_id):
        self.community_id = community_id
        self.match_id = match_id
        self.team_id = team_id

    def get_player(self):
        return Player.query.get(self.player_id)

    def get_match(self):
        return Match.query.get(self.match_id)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'team_id': self.team_id,
            'player_id': self.player_id,
            'match_id': self.match_id,
            'created': dump_datetime(self.created)
        }

    def	__str__(self):
        return str(self.id) + ' ' + str(self.created)