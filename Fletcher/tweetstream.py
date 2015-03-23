#!/usr/bin/env/python

import tweepy
import sys
import pymongo
import datetime

hashtag = ''  # your topic of interest

date = datetime.datetime.now()

consumer_key =""
consumer_secret= ""
access_token =""
access_token_secret=""


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api

        super(tweepy.StreamListener, self).__init__()

        self.db = pymongo.MongoClient().elclassico

    def on_status(self, status):
        print status.text , "\n"
        
        data ={}

        # Tweet
        data['text'] = status.text

        # Metadata
        data['created_at'] = status.created_at
        data['replyto'] = status.in_reply_to_screen_name
        data['geo'] = status.geo
        data['source'] = status.source

        # Userdata
        data['user'] = status.user.screen_name
        data['userfriends'] = status.user.friends_count
        data['follower'] = status.user.followers_count


        self.db.Tweets.insert(data)

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

print('Listening to Twitter for #%s...' % hashtag)

sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
sapi.filter(track=[hashtag])
