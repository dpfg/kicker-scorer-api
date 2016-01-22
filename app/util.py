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

from random import randint

creatures = ['ants', 'bats', 'bears', 'bees', 'birds', 'buffalo', 'cats', 'chickens', 'cattle', 'dogs', 'dolphins', 'ducks', 'elephants', 'fishes', 'foxes', 'frogs', 'geese', 'goats', 'horses', 'kangaroos', 'lions', 'monkeys', 'owls', 'oxen', 'penguins', 'people', 'pigs', 'rabbits', 'sheep', 'tigers', 'whales', 'wolves', 'zebras', 'banshees', 'crows', 'black cats', 'chimeras', 'ghosts', 'conspirators', 'dragons', 'dwarves', 'elves', 'enchanters', 'exorcists', 'sons', 'foes', 'giants', 'gnomes', 'goblins', 'gooses', 'griffins', 'lycanthropes', 'nemesis', 'ogres', 'oracles', 'prophets', 'sorcerors', 'spiders', 'spirits', 'vampires', 'warlocks', 'vixens', 'werewolves', 'witches', 'worshipers', 'zombies', 'druids']
creatures_num = len(creatures)
colors = ["red", "green", "blue", "yellow", "purple", "mint green", "teal", "white", "black", "orange", "pink", "grey", "maroon", "violet", "turquoise", "tan", "sky blue", "salmon", "plum", "orchid", "olive", "magenta", "lime", "ivory", "indigo", "gold", "fuchsia", "cyan", "azure", "lavender", "silver"]
colors_num = len(colors)

def generate_team_name():
    random_color = colors[randint(0, colors_num)]
    random_creature = creatures[randint(0, creatures_num)]
    return  "{:s} {:s}".format(random_color, random_creature)
