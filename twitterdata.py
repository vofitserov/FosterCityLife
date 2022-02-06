import os
import json
from urllib.parse import urlparse

import requests

from instaloader import *
from imageanalyzer import *

# Named global logger from config
logger = logging.getLogger("fostercitylife")


class ImageData:
    analyzer = ImageAnalyser()

    def __init__(self, url, image_file):
        self.url = url
        self.image_file = image_file
        self.pred = None
        return

    def find_prob(self, name):
        for (c, n, p) in self.pred:
            if n in name:
                return p
        return 0.0

    def do_prediction(self):
        logger.info("analyzing %s" % self.url)
        self.pred = ImageData.analyzer.predict(self.image_file)
        return self.pred

    def prediction_prob(self, name):
        if not self.pred:
            self.pred = self.do_prediction()
            pass
        return self.find_prob(name)

    def prediction_text(self, name):
        text = ""
        for (c, n, p) in self.pred:
            if n.find("_") == -1 and p > IMAGE_TEXT_CONF:
                if len(text) == 0:
                    text = n
                else:
                    text = text + " and " + n
                    break
        if len(text) == 0:
            text = "picture"
        return text


class TweetData:
    loader = Instaloader()
    loader.login("vofitserov", "lenina186")

    def __init__(self, tweet, db_directory):
        self.tweet = tweet
        self.images = []
        self.db = db_directory
        return

    def url(self):
        return "https://twitter.com/%s/status/%s" % \
               (self.tweet.user.screen_name, self.tweet.id_str)

    def fetch_images(self):
        self.images = []
        for u in self.tweet.entities["urls"]:
            url = u["expanded_url"]
            parts = url.split("/")
            if len(parts) < 5:
                logger.info("skipping non enough parts in url %s", url)
                continue
            host = parts[2]
            if host != "www.instagram.com" and host != "instagram.com" and host != "instagr.am":
                logger.info("skippig non instagram host %s", host)
                continue
            shortcode = parts[4]
            logger.info("fetching instagram post %s", url)
            try:
                post = Post.from_shortcode(TweetData.loader.context, shortcode)
                self.images.append(self.fetch_image(post.url))
                for spost in post.get_sidecar_nodes():
                    self.images.append(self.fetch_image(spost.display_url))
                    pass
                pass
            except Exception as err:
                logger.info("failed to fetch %s: %s" % (shortcode, str(err)))
                pass
            pass
        for m in self.tweet.entities.get("media", []):
            url = m["media_url"]
            try:
                self.images.append(self.fetch_image(url))
            except Exception as err:
                logger.info("failed to fetch %s: %s" % (shortcode, str(err)))
                pass
            pass
        return

    def fetch_image(self, url):
        logger.info("fetching image %s", url)
        o = urlparse(url)
        image_name = os.path.join(self.db, self.tweet.id_str + "_" + o.path.split("/")[-1])
        image_data = requests.get(url).content
        with open(image_name, "wb") as image_file:
            image_file.write(image_data)
        logger.info("saved image to %s" % image_name)
        return ImageData(url, image_name)

    def get_images(self):
        if len(self.images) > 0:
            return self.images
        self.fetch_images()
        return self.images

    # "lakeside"
    def find_image_with_prediction(self, name):
        for image in self.get_images():
            if image.prediction_prob("face") > 0.5:
                logger.info("skipping image because of the face")
                continue
            prob = image.prediction_prob(name)
            if prob > IMAGE_CONF:
                return image
            pass
        return None

