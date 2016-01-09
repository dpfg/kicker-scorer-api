import re

"""Collection of utils."""


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%dT%H:%M:%S.000Z")


community_name_regex = re.compile('^[0-9a-zA-Z_-]+$')


def is_not_valid_entity_name(community_name):
    """Check is string valid to be used in url path."""
    return community_name_regex.match(community_name) is None
