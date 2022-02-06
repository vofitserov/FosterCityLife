import sys
import logging
import logging.handlers

# daemon log and lock
LOGFILE = "/Users/vladimir/FosterCityLife/fostercitylife.log"
PIDFILE = "/Users/vladimir/FosterCityLife/fostercitylife.pid"

# http host and port to start http server
HTTP_HOST = ""  # "garage.local"
HTTP_PORT = 80

# FosterCityLife twitter app
APP_KEY = "zpeVuouVxk258coZ2lGCDsYZG"
APP_SECRET = "6TQ8TQ8ypiBmmMV8Jltj6Ex46qr8k3ikVp7zo5GGKlQMfZmrZ1"
APP_TOKEN = "AAAAAAAAAAAAAAAAAAAAAP1ZKAEAAAAAI0Mjv9E54lhA%2B5QV0LyE%2BCIUHHE%3DQz4gv35R48huuLXGkUBlG4GikNHTaVqBiDmrnJ19uqIt3Fkfr4"

# produced by twitter-oauth.py
TWITTER_CREDS = "/Users/vladimir/FosterCityLife/fostercitylife.oauth"
TWITTER_ACCOUNT = "fostercitylife"
TWITTER_DB = "/Users/vladimir/FosterCityLife/db"
INSTA_DB = "/Users/vladimir/FosterCityLife/idb"

IMAGE_TOKENS = ["lakeside", "dock", "breakwater", "seashore"]
IMAGE_CONF = 0.02
IMAGE_TEXT_CONF = 0.15

logger = logging.getLogger("fostercitylife")
logger.setLevel(logging.INFO)

#handler = logging.FileHandler(LOGFILE)
#handler = logging.handlers.RotatingFileHandler(
#    LOGFILE, maxBytes=100000, backupCount=5)

handler = logging.StreamHandler()
#formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#handler.setFormatter(formatter)
logger.addHandler(handler)
