"""
This file just contains the blocklist of JWT tokens.
It will be imported by app and the logout resource,
so that the tokens can be added to the blocklist 
when the users log out.

Since python' set does not persist upon application restarts
one can use alternative way to store block such as :
db or redis for extensive performance.
"""

BLOCKLIST = set()