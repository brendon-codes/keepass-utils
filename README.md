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

