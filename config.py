import sys
import logging
import logging.handlers

# daemon log and lock
LOGFILE = "/Users/vladimir/FosterCityLife/fostercitylife.log"

logger = logging.getLogger("fostercitylife")
logger.setLevel(logging.INFO)

#handler = logging.FileHandler(LOGFILE)
#handler = logging.handlers.RotatingFileHandler(
#    LOGFILE, maxBytes=100000, backupCount=5)

handler = logging.StreamHandler()
#formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#handler.setFormatter(formatter)
logger.addHandler(handler)

# FosterCityLife twitter app
APP_KEY = ""
APP_SECRET = ""
APP_TOKEN = ""

# produced by twitter-oauth.py
TWITTER_TOKEN = ""
TWITTER_SECRET = ""
TWITTER_ACCOUNT = "fostercitylife"
TWITTER_DB = "/Users/vladimir/FosterCityLife/db"

# instaloader allows more requests with login
INSTA_LOGIN = ""
INSTA_PASSWORD = ""

IMAGE_TOKENS = ["lakeside", "dock", "breakwater", "seashore"]
IMAGE_CONF = 0.02
IMAGE_TEXT_CONF = 0.15

from secrets import *
