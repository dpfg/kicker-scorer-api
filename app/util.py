
from flask import g, request, redirect, url_for,jsonify

def dump_datetime(value):
	"""Deserialize datetime object into string form for JSON processing."""
	if value is None:
		return None
	return value.strftime("%Y-%m-%dT%H:%M:%S")

import re
community_name_regex = re.compile('^[0-9a-zA-Z_-]+$')
def is_not_valid_entity_name(community_name):
	return community_name_regex.match(community_name) is None