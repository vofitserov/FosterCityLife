import logging
import time
import os
import sys
import requests
import json

import re

from tweepy import *
from config import *

# Named global logger from config
logger = logging.getLogger("fostercitylife")


def read_token_file(filename):
    access_file = open(filename, "r")
    access_token = access_file.readline().strip("\n")
    access_secret = access_file.readline().strip("\n")
    access_file.close()
    return (access_token, access_secret)


class TwitterSearch:
    def __init__(self, db_directory):
        logger.info("searcher using %s" % TWITTER_CREDS)
        (self.oauth_token, self.oauth_secret) = read_token_file(TWITTER_CREDS)
        self.auth = OAuthHandler(APP_KEY, APP_SECRET)
        self.auth.set_access_token(self.oauth_token, self.oauth_secret)
        self.api = API(self.auth)
        self.db = db_directory
        return

    def save_tweet(self, t):
        filename = os.path.join(self.db, t.id_str + ".json")
        with open(filename, "w") as outfile:
            json.dump(t._json, outfile)
        logger.info("saved tweet in %s", filename)
        return

    def fetch_timeline(self):
        logger.info("fetching @%s timeline..." % TWITTER_ACCOUNT)
        ts = self.api.user_timeline(screen_name=TWITTER_ACCOUNT,
                                    tweet_mode="extended",
                                    exclude_replies=True,
                                    include_rts=False, count=200)
        logger.info("fetched %d tweets" % len(ts))
        for t in ts:
            self.save_tweet(t)
            pass
        return ts

    def fetch_tweets(self):
        logger.info("executing \"foster city\" instagram search...")
        ts = self.api.search(q="(\"foster city\" OR fostercity OR #fostercity OR philothewisp) instagram.com",
                             tweet_mode="extended", count=200)
        logger.info("fetched %d tweets" % len(ts))
        for t in ts:
            self.save_tweet(t)
            pass

        logger.info("executing geocode search...")
        ts = self.api.search(q="instagram.com", geocode="37.5585465,-122.2710788,10km",
                                tweet_mode="extended", count=200)
        logger.info("fetched %d tweets" % len(ts))
        for t in ts:
            self.save_tweet(t)
            pass

        max_id = ""
        while True:
            logger.info("executing \"#fostercity\" recent search...")
            ts = self.api.search(q="(\"foster city\" OR fostercity OR #fostercity OR philothewisp) -instagram",
                                 result_type="recent", tweet_mode="extended", count=200, max_id=max_id)
            logger.info("fetched %d tweets" % len(ts))
            if len(ts) < 10:
                logger.info("...done. exiting max_id loop.")
                break
            for t in ts:
                max_id = t.id_str
                self.save_tweet(t)
                pass
            logger.info("sleeping 10 seconds...")
            time.sleep(10)
            pass

        return ts

    def fetch_tweet(self, tweetid):
        logger.info("fetching one tweet by id %s" %tweetid)
        t = self.api.get_status(tweetid, tweet_mode="extended")
        if t:
            self.save_tweet(t)
            pass
        return t

    def load_tweets(self):
        logger.info("loading unprocessed tweets...")
        tweets = {}
        done = {}
        ts = []
        for entry in os.scandir(self.db):
            if entry.name.find(".json") and entry.is_file():
                tweets[entry.name] = 1
            if entry.name.find(".done") and entry.is_file():
                done[entry.name] = 1
            pass
        for filename in tweets.keys():
            donename = filename.replace(".json", ".done")
            if donename in done:
                continue
            fullname = os.path.join(self.db, filename)
            with open(fullname, "r") as infile:
                logger.info("loading tweet from %s", filename)
                t = Status.parse(self.api, json.load(infile))
                ts.append(t)
                pass
            pass
        logger.info("found %d unprocessed tweets" % len(ts))
        return ts

    def get_tweets(self):
        self.fetch_tweets()
        return self.load_tweets()

    def get_timeline(self):
        self.fetch_timeline()
        return self.load_tweets()

    def done(self, t):
        donename = os.path.join(self.db, t.id_str + ".done")
        open(donename, "w").close()
        return

    def quote_tweet(self, quote_text, imagefile):
        logger.info("posting tweet: %s" % quote_text.replace("\n", " "))
        media = self.api.media_upload(imagefile)
        self.api.update_status(quote_text, media_ids=[media.media_id_string])
        return

def dump_main(argv):
    twitter = TwitterSearch(TWITTER_DB)
    tweets = twitter.api.user_timeline(screen_name=TWITTER_ACCOUNT,
                            count=200, include_rts=False,
                            exclude_replies = True, tweet_mode="extended")
    print("<html><body>")
    for tweet in tweets:
        print("<!------------------------------------------------>")
        #print("<!--\n%s\n-->" % tweet._json)
        tweet_url = "https://twitter.com/%s/status/%s" % (tweet.user.screen_name, tweet.id_str)
        print("<a href=\"%s\">\n%s</a><br>" % (tweet_url, tweet_url))
        text = re.sub(r'https://t.co/[a-z0-9A-Z]+', ' ', tweet.full_text).strip()
        print(text + "<br>")
        for url in tweet.entities.get("urls", []):
            link_url = url["expanded_url"]
            print("<a href=\"%s\">%s</a><br>" % (link_url, link_url))
        for image in getattr(tweet,'extended_entities',{}).get("media", []):
            media_url = image["media_url"]
            print("<image src=\"%s\" width=\"200\">" % media_url)
            pass
        print("<hr>")
        pass
    print("</body></html>")
    return

def twitter_main(argv):
    twitter = TwitterSearch(TWITTER_DB)
    logger.info("executing twitter search...")
    ts = twitter.api.search(q="instagram.com", geocode="37.5585465,-122.2710788,10km",
                             tweet_mode="extended", count=100)
    logger.info("fetched %d tweets" % len(ts))
    for t in ts:
        print(t.full_text)
        pass
    return

def main(argv):
    twitter = TwitterSearch(INSTA_DB)
    ts = twitter.fetch_timeline()
    for t in ts:
        print(t.full_text)
        if len(t.entities)>0:
            print(t.entities)
        pass
    return

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main(sys.argv)

