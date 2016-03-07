"""
    abstraction.py

    Copyright (c) 2016 Robert MacGregor
    This software is licensed under the MIT license. Refer to LICENSE.txt for
    more information.
"""

class Database(object):
    rooms = None
    players = None
    items = None
    exits = None

    def __init__(self, rooms, players, items, exits):
        self.rooms = rooms
        self.players = players
        self.items = items
        self.exits = exits

class Entity(object):
    name = None
    description = None
    owner = None

    def __init__(self, name=None, description=None, owner=None):
        self.name = name
        self.description = description
        self.owner = owner

class Room(Entity):
    def __init__(self, name=None, owner=None, description=None, exits=None):
        Entity.__init__(self, name=name, description=description, owner=owner)

class Player(Entity):
    password = None

    def __init__(self, name=None, password=None, description=None):
        Entity.__init__(self, name, description)
        self.password = password

class Thing(Entity):
    def __init__(self, name=None, owner=None, description=None):
        Entity.__init__(self, name=name, owner=owner, description=description)

class Exit(Entity):
    def __init__(self, name=None, owner=None, description=None):
        Entitiy.__init__(self, name=name, owner=owner, description=description)
