#!/usr/bin/env python
import os
import sys

# Read in properties file
# if db location is set the use: if not existing create and copy empty db file
# if not set


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Jupiter.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
