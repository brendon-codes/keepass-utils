#!/usr/bin/env python3

"""
Assigns an entry to a group.

This is needed because KeePassXC does not allow for an
easy way to assign entries to groups if many groups exist.

USE THIS SCRIPT AT YOUR OWN RISK!
It is entirely possible that this script could destroy your
KeePass DB, or leak the contents to memory, or leak it to
somewhere else.  No gaurantees are made about the safety or
reliability of this script.

Tested on Fedora 26+ / Python 3.6+

Only dependency is PyKeePass
See: https://github.com/pschmitt/pykeepass
To install dependency:

  pip install --user pykeepass

"""

import os
import sys
import argparse
from getpass import getpass

from pykeepass import PyKeePass as KP


def get_args():
    aparser = (
        argparse.ArgumentParser(description="Assign KeePass2 entry to a group")
    )
    aparser.add_argument(
        "dbpath",
        metavar="DBPATH",
        action="store",
        type=str,
        help="Path to DB file"
    )
    aparser.add_argument(
        "entrytitle",
        metavar="ENTRY_TITLE",
        action="store",
        type=str,
        help="Entry title"
    )
    aparser.add_argument(
        "groupname",
        metavar="GROUP_NAME",
        action="store",
        type=str,
        help="Group name"
    )
    args = aparser.parse_args()
    return args


def main():
    try:
        process()
    except KeyboardInterrupt:
        print("\nQuitting", file=sys.stderr)
        sys.exit(1)
    print("Success", file=sys.stdout)
    sys.exit(0)


def process():
    args = get_args()
    print(args.dbpath)
    if not os.path.exists(args.dbpath):
        print("DB file path does not exist", file=sys.stderr)
        sys.exit(1)
    password = getpass()
    try:
        db = KP(args.dbpath, password=password)
    except FileNotFoundError:
        print("DB file path does not exist", file=sys.stderr)
        sys.exit(1)
    except OSError:
        print("Invalid password", file=sys.stderr)
        sys.exit(1)
    except Exception:
        print("Misc error", file=sys.stderr)
        sys.exit(1)
    groups = db.find_groups_by_name(args.groupname)
    if len(groups) == 0:
        print("Group does not exist", file=sys.stderr)
        sys.exit(1)
    if len(groups) > 1:
        print(
            "Multiple groups of that name exist. Cannot continue",
            file=sys.stderr
        )
        sys.exit(1)
    group = groups[0]
    ## Only grab from root
    path = "".join([db.root_group.path, args.entrytitle])
    entries = db.find_entries_by_path(path)
    if len(entries) == 0:
        print("Entry by that title does not exist", file=sys.stderr)
    for entry in entries:
        group.append(entry)
    db.save()


if __name__ == "__main__":
    main()
