from app import db
from app.util import dump_datetime

class Community(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), index = True, unique = True)
	owner_id = db.Column(db.Integer, nullable = False)
	created = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

	players = db.relationship('Player', backref = 'Community', 
		lazy = 'dynamic',
		primaryjoin="Player.community_id==Community.id",
		foreign_keys="Player.community_id",
		passive_deletes='all')

	teams = db.relationship('Team', backref = 'Community', 
		lazy = 'dynamic',
		primaryjoin="Team.community_id==Community.id",
		foreign_keys="Team.community_id",
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
	communities = db.relationship('Community', backref = 'User', 
		lazy = 'dynamic',
		primaryjoin="User.id==Community.owner_id",
		foreign_keys=[Community.__table__.c.owner_id],
		passive_deletes='all')
	
	created = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

	def __init__(self, email):
		self.email = email

class Player(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	community_id = db.Column(db.Integer, nullable = False, index = True)
	username = db.Column(db.String(100), nullable = False)
	created = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

	def __init__(self, community, username):
		self.username = username
		self.community_id = community.id

	@property
	def serialize(self):
		return {
			'id'		: self.id,
			'username' 	: self.username,
			'created'	: dump_datetime(self.created)
		}

class Team(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	community_id = db.Column(db.Integer, nullable = False, index = True)
	name = db.Column(db.String(200), nullable = False)
	forward_id = db.Column(db.Integer, nullable = False)
	goalkeeper_id = db.Column(db.Integer, nullable = False)
	created = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

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
			'forward'  		: Player.query.get(self.forward_id).username, # change to join and single query
			'goalkeeper'	: Player.query.get(self.goalkeeper_id).username # change to join and single query
		}

class Match(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	community_id = db.Column(db.Integer, nullable = False, index = True)
	match_datetime = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
	team0_id = db.Column(db.Integer, nullable = False)
	team1_id = db.Column(db.Integer, nullable = False)
	team0_score = db.Column(db.Integer, default = 0)
	team1_score = db.Column(db.Integer, default = 0)

	def __init__(self, community, team0, team1):
		self.community_id = community.id
		self.team0_id = team0.id
		self.team1_id = team1.id

	@property
	def serialize(self):
		teams = Team.query.filter_by(Team.id.in_(self.team0_id, self.team1_id))
		return {
			'id'			: self.id,
			'date'			: dump_datetime(self.match_datetime),
			'teams'			: ([t.serialize for t in teams]),
			'score'			: (self.team0_score, self.team1_score)
		}		

class MatchGoal(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	community_id = db.Column(db.Integer, nullable = False, index = True)	
	match_id = db.Column(db.Integer, nullable = False)
	player_id = db.Column(db.Integer, nullable = False)

	created = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))	


