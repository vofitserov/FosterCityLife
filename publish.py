#!/usr/bin/env python3

import sys
import argparse

from config import *
from twitterpublisher import *

# Named global logger from config
logger = logging.getLogger("fostercitylife")


def do_publish(t_pub, num):
    if len(t_pub.tweets) == 0:
        t_pub.get_tweets()
    if len(t_pub.tweets) == 0:
        return -1
    if t_pub.post_tweet(num) > 0:
        return 0
    return -2


def do_get(t_pub):
    tweets = t_pub.get_tweets()
    if len(tweets) > 0:
        return 0
    return -1


def do_getone(t_pub, tweetid):
    tweet = t_pub.get_one(tweetid)
    if tweet:
        return 0
    return -1


def main(argv):
    logger.info("staring main runtime")
    publisher = TwitterPublisher()
    err = -5
    skip_arg = 0
    num = 1
    for i in range(len(argv)):
        if argv[i] == "--dryrun":
            publisher.dry_run = True
        elif argv[i] == "--prompt":
            publisher.ask_prompt = True
        elif argv[i] == "--noprompt":
            publisher.ask_prompt = False
        elif argv[i] == "--all":
            publisher.ask_prompt = True
            publisher.ask_all = True
        elif argv[i] == "--get":
            err = do_get(publisher)
        elif argv[i] == "--num" and i + 1 < len(argv):
            num = int(argv[i + 1])
            skip_arg = i + 1
        elif argv[i] == "--getone" and i + 1 < len(argv):
            tweetid = argv[i + 1]
            skip_arg = i + 1
            err = do_getone(publisher, tweetid)
        elif i == skip_arg:
            continue
        else:
            logger.error("Invalid arguments: %s" % argv[i])
            return -3
        pass

    return do_publish(publisher, num)

# Press the green button in the gutter to run the script.
sys.exit(main(sys.argv))

