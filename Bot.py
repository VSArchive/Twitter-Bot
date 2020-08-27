import tweepy
import time
import json
import os
from dotenv import load_dotenv

print('Starting Twitter bot...')

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

me = api.me()

print('Hello', me.screen_name)

FILE_NAME = 'last_mention.txt'

def retrieve_last_mention_id(file_name):
    f_read = open(file_name, 'r')
    last_mention_id = int(f_read.read().strip())
    f_read.close()
    return last_mention_id

def store_last_mention_id(last_mention_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_mention_id))
    f_write.close()
    return

def reply_to_tweets(repeat):
    print('retrieving tweets...')
    last_mention_id = retrieve_last_mention_id(FILE_NAME)
    mentions = api.mentions_timeline(
        last_mention_id,
        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_mention_id = mention.id
        store_last_mention_id(last_mention_id, FILE_NAME)
        if 'hi' or 'hello' or 'hey' or 'hii' or 'heyy' in mention.full_text.lower():
            print('found a match')
            print('responding back...')
            api.update_status('@' + mention.user.screen_name +
                              ' Hello', mention.id)
            mention.user.screen_name
        else:
            time.sleep(15)
            print('No tweet to reply')
    if repeat:
        reply_to_tweets(True)

def tweet():
    tweet_content = input('What should I tweet : ')
    api.update_status(tweet_content)

option = 1
loop = True

while loop:
    print('1.Reply to tweets containing Hi,Hello,etc..')
    print('2.Reply to tweets containing Hi,Hello,etc.. recursively')
    print('3.Make a Tweet')
    option = int(input('Choose option : '))
    if option == 1:
        reply_to_tweets(False)
    elif option == 2:
        reply_to_tweets(True)
    elif option == 3:
        tweet()
    else:
        print('Exiting...')
        loop = False
