import os

import tweepy
from dotenv import load_dotenv

from arsenal.pout.models import TwitterUser

load_dotenv()

CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')


class Twitter:

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, bearer_token):
        self.tkinvt_client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        self.users_client = tweepy.Client(bearer_token)

    # Database functions exposed to all instances of class, since my twitter account will be the only one creating
    # instances!
    def add_avoidant(self, username):
        twitter_user = self.users_client.get_user(username=username)
        twitter_id = twitter_user.data.id

        avoidant = TwitterUser(twitter_id=twitter_id, name=username)
        avoidant.save()

    def get_avoidants(self):
        avoidants = TwitterUser.objects
        return avoidants

    def remove_avoidant(self, username):
        avoidant = TwitterUser.objects(name=username).first()
        avoidant.delete()

    def pout(self):
        avoidants = self.get_avoidants()

        for avoidant in avoidants:
            self.tkinvt_client.mute(avoidant['twitter_id'])

    def un_pout(self):
        avoidants = self.get_avoidants()

        for avoidant in avoidants:
            self.tkinvt_client.unmute(avoidant['twitter_id'])


tkinvt = Twitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN)
