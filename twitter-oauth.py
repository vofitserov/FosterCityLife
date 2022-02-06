import os
import time

from config import *
from tweepy import *

auth = OAuthHandler(APP_TOKEN, APP_SECRET)
redirect_url = auth.get_authorization_url()
print(redirect_url)

# Example w/o callback (desktop)
verifier = input('Verifier:')

# auth.request_token["oauth_token_secret"] = verifier
auth.get_access_token(verifier)

print(auth.access_token)
print(auth.access_token_secret)