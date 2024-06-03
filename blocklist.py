BLOCKLIST = set()    # use database or better use Reddis to store your BLOCKLIST


# when a user/client sent the logout request, the user's access token is stored in the "BLOCKLIST",
# so when a user try to use that same JWT, we will check if it's in the "BLOCKLIST" terminate and send the error message