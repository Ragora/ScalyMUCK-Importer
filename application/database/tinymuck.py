"""
    tinymuck.py

    Copyright (c) 2016 Robert MacGregor
    This software is licensed under the MIT license. Refer to LICENSE.txt for
    more information.
"""

import re

import abstraction
import errors

class Importer(abstraction.Database):
    _header_regex = re.compile("([A-z]| )+: \S+")
    _property_regex = re.compile("([A-z]| )+:[i|\\^|&]+:\S*")

    _entry_regex = re.compile("#[0-9]+.+?\n\n", re.DOTALL)

    _property_delineator = ":"
    # Other delineator types: i = internal, ^ = integer, # = dbref, & = boolexp

    _rooms = None
    _players = None
    _exits = None
    _things = None

    _type_lookups = None

    def __init__(self, target):
        print("TinyMUCK INFO: Importing from file '%s' ... " % target)

        self._type_lookups = {
            "player": self._read_player,
            "room": self._read_room,
            "thing": self._read_thing,
        }

        with open(target, "r") as handle:
            payload_string = handle.read()
            payload = payload_string.split("\n")

            # First line should read this
            if (payload[0] != "***Firiss TinyMUCK 2.3 DUMP Format v1***"):
                raise errors.ImporterError("Failed to read database header!")

            self._rooms = { }
            self._players = { }
            self._exits = { }
            self._things = { }

            self._read_objects(payload_string)
            self._finalize_objects()

            print("")
            print("----------------------------------")
            print("TinyMUCK: Import Stats")
            print("----------------------------------")
            print("Rooms: %u" % len(self._rooms))
            print("Things: %u" % len(self._things))
            print("Players: %u" % len(self._players))
            print("Exits: %u" % len(self._exits))
            print("----------------------------------")

    def _read_null(self, entry):
        pass

    def _read_properties(self, payload):
        result = { }

        for property in payload:
            if (re.match(self._property_regex, property) is None):
                raise errors.ImporterError("Failed to read object property!")

            first_delineator = property.find(":")
            second_delineator = property.find(":", first_delineator + 1)

            key = property[0:first_delineator].lower()
            flags = property[first_delineator:second_delineator]
            value = property[second_delineator + 1:len(property)]

            result[key] = value

        return result

    def _read_player(self, entry):
        properties = self._read_properties(entry[10:])
        name = entry[2]
        description = properties["desc"]

        # Some players may not have a password -- this is the case for the minimal DB Guest account
        password = None
        if ("pass" not in properties):
            print("TinyMUCK WARNING: Found player '%s' without a password field." % name)
        else:
            password = properties["pass"]

        result = abstraction.Player(name=name, password=password, description=description)

        # Attach internal importer information
        result._identifier = int(entry[0].split("#")[1])
        result._room_identifier =  int(entry[3])

        # Now stick them in our temporary ID lookup
        self._players[result._identifier] = result

        return result

    def _read_room(self, entry):
        properties = self._read_properties(entry[9:])
        name = entry[2]

        description = None

        # Some Rooms may not have a description, which is normal.
        if ("desc" in properties):
            description = properties["desc"]

        result = abstraction.Room(name=name, description=description)

        # Attach internal importer information
        result._owner_identifier = int(entry[4])
        result._identifier = int(entry[0].split("#")[1])

        # Now stick them in our temporary ID lookup
        self._rooms[result._identifier] = result

    def _read_thing(self, entry):
        #properties = self._read_properties(entry[9:])
        name = entry[2]

        description = None

        result = abstraction.Thing(name=name)

        # Attach internal importer information
        result._room_identifier = int(entry[3])
        result._owner_identifier = int(entry[4])
        result._identifier = int(entry[0].split("#")[1])

        # Now stick them in our temporary ID lookup
        self._things[result._identifier] = result

    # TODO: Perhaps compact this a little bit.
    def _finalize_objects(self):
        # Loop foreach player and assign their location reference
        for player_identifier in self._players:
            player = self._players[player_identifier]

            if (player._room_identifier not in self._rooms):
                print("TinyMUCK WARNING: Player '%s' has an unknown room!" % player.name)
            else:
                player.room = self._rooms[player._room_identifier]

        # Loop foreach room and assign owner reference
        for room_identifier in self._rooms:
            room = self._rooms[room_identifier]

            if (room._owner_identifier not in self._players):
                print("TinyMUCK WARNING: Room '%s' has an unknown owner!" % room.name)
            else:
                room.owner = self._players[room._owner_identifier]

        # Loop foreach thing and assign location + owner reference
        for thing_identifier in self._things:
            thing = self._things[thing_identifier]

            if (thing._owner_identifier not in self._players):
                print("TinyMUCK WARNING: Thing '%s' has an unknown owner!" % thing.name)
            else:
                thing.owner = self._players[thing._owner_identifier]

            if (thing._room_identifier not in self._rooms):
                print("TinyMUCK WARNING: Thing '%s' has an unknown room!" % thing.name)
            else:
                thing.room = self._rooms[thing._room_identifier]

        print("TinyMUCK INFO: Database Finalization OK!")


    def _read_objects(self, payload):
        for match in re.finditer(self._entry_regex, payload):
            entry_payload = match.group(0).rstrip().split("\n")

            entry_type = entry_payload[1].lower().split()[0]

            if (entry_type not in self._type_lookups):
                print("TinyMUCK WARNING: Unknown object type '%s'!" % entry_type)
                self._type_lookups[entry_type] = self._read_null
            else:
                self._type_lookups[entry_type](entry_payload)

        print("TinyMUCK INFO: Database Read OK!")
