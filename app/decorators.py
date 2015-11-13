
from functools import wraps

from app.models import Community
from app import app

def json_content(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if request.json is None:
			return "", 415, {'Content-Type': 'application/json; charset=utf-8'}
		return f(*args, **kwargs)
	return decorated_function    


def community_resource(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		community_name = kwargs['community_name']
		community = Community.query.filter_by(name=community_name).first()
		if community is None:
			return "", 404      

		kwargs['community'] = community
		kwargs.pop('community_name')
		return f(*args, **kwargs)
	return decorated_function

def team_resource(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		community_name = kwargs['community_name']
		community = Community.query.filter_by(name=community_name).first()
		if community is None:
			return "", 404      
			
		kwargs['community'] = community
		kwargs.pop('community_name')

		team_name = kwargs['team_name']
		team = Team.query.filter_by(name=team_name).first()
		if team is None:
			return "", 404      
			
		kwargs['team'] = team
		kwargs.pop('team_name')

		return f(*args, **kwargs)
	return decorated_function
