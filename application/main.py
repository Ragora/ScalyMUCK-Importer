"""
    main.py

    Copyright (c) 2016 Robert MacGregor
    This software is licensed under the MIT license. Refer to LICENSE.txt for
    more information.
"""

import sys

import database

class Application(object):
    def _print_usage(self):
        print("Usage: %s <database type> <input file>" % sys.argv[0])

    def main(self):
        if (len(sys.argv) != 3):
            print("ERROR: Incorrect number of parameters.")
            self._print_usage()
            return

        # For now, we just init the tmuck DB
        tmuck = database.TinyMuck(sys.argv[2])

if __name__ == "__main__":
    Application().main()
