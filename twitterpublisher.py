import os
import json
import requests
import random
import tweepy.error

from config import *
from twittersearch import *
from twitterdata import *

# Named global logger from config
logger = logging.getLogger("fostercitylife")


class TwitterPublisher:
    def __init__(self):
        self.tweets = []
        self.dry_run = False
        self.skip_face = True
        self.ask_prompt = True
        self.ask_all = False
        self.favorite = True
        self.twitter = TwitterSearch(TWITTER_DB)
        return

    def get_tweets(self):
        for tweet in self.twitter.get_tweets():
            self.tweets.append(TweetData(tweet, TWITTER_DB))
            pass
        return self.tweets

    def get_one(self, tweetid):
        tweet = self.twitter.fetch_tweet(tweetid)
        if tweet:
            self.tweets.append(TweetData(tweet, TWITTER_DB))
            pass
        return self.tweets

    def tweet_text(self, tweet_data, image_data):
        screen_name = tweet_data.tweet.user.screen_name
        adjective = random.choice(["beautiful", "pretty", "magnificent", "spectacular"])
        quote_url = "https://twitter.com/%s/status/%s" % (screen_name, tweet_data.tweet.id_str)
        text = "Foster City %s %s, thanks @%s!\n%s" % \
               (adjective, image_data.prediction_text("lakeside"),
                screen_name, quote_url)
        return text

    def quote_tweet(self, quote_text, image_file):
        if self.dry_run:
            logger.info("dryrun: %s" % quote_text.replace("\n", " "))
            return
        self.twitter.quote_tweet(quote_text, image_file)
        return

    def done_tweet(self, tweet_data):
        if self.dry_run:
            logger.info("drydone: %s" % tweet_data.tweet.id_str)
            return
        if self.favorite:
            try:
                self.twitter.api.create_favorite(id=tweet_data.tweet.id_str)
            except tweepy.error.TweepError as e:
                logger.info("error create_favorite: %s" % str(e))
                pass
            pass
        self.twitter.done(tweet_data.tweet)
        return

    def post_tweet(self, num=1):
        posted = 0
        for tweet_data in self.tweets:
            screen_name = tweet_data.tweet.user.screen_name.lower()
            if screen_name in ["fostercitylife", "fostercitypatch", "cityoffc"]:
                logger.info("skipping tweet from: %s" % screen_name)
                self.done_tweet(tweet_data)
                continue
            logger.info("---------------------")
            logger.info("%s" % tweet_data.url())
            logger.info("%s" % tweet_data.tweet.full_text)
            for image_data in tweet_data.get_images():
                if image_data.prediction_prob("face") > 0.5 and self.skip_face:
                    logger.info("skipping image because of the face.")
                    continue
                if image_data.prediction_prob(IMAGE_TOKENS) < IMAGE_CONF and not self.ask_all:
                    logger.info("skipping image no good tokens.")
                    continue
                logger.info("found image %s" % image_data.url)
                quote_text = self.tweet_text(tweet_data, image_data)
                should_skip = False
                if self.ask_prompt:
                    print(quote_text)
                    answer = input("keep, skip, or text:")
                    if answer == "skip":
                        should_skip = True
                    elif answer == "keep":
                        pass
                    else:
                        quote_text = answer + quote_text[quote_text.find(","):]
                        pass
                    pass

                if not should_skip:
                    self.quote_tweet(quote_text, image_data.image_file)
                    posted += 1
                else:
                    logger.info("skipping image due to prompt")
                    pass
                pass
            # mark tweet as done for processing
            self.done_tweet(tweet_data)
            if posted >= num: break
            pass
        return posted
