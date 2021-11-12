import tweepy
import time
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

print(api.verify_credentials().screen_name)


def reply_to_tweets(repeat):
    print('retrieving tweets...')
    mentions = api.mentions_timeline()
    for mention in reversed(mentions):
        if 'hi' or 'hello' or 'hey' or 'hii' or 'heyy' in mention.full_text.lower():
            print('found a match')
            print(
                str(mention.id) + ' - ' + mention.text
            )
            print('responding back...')
            try:
                api.update_status('@' + mention.user.screen_name + ' hi')
            except:
                print('Can`t reply back')
        else:
            time.sleep(15)
            print('No tweet to reply')
    if repeat:
        reply_to_tweets(True)


def tweet():
    tweet_content = input('What should I tweet : ')
    print('tweeting...')
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
