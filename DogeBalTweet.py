

# TEST NET

# import urllib library
from urllib.request import urlopen
import json
from twython import Twython
from datetime import datetime
from datetime import date
from datetime import timedelta
import os
import tweepy as tw
import pandas as pd
from block_io import BlockIo
import matplotlib.pyplot as plt

version = 2

#KEYS FROM THE TWITTER DEV PORTAL
# These Keys should not be coded explicitly like this
# ideally they should be stored in a separate encrypted file
# and there should be a decryption function within this 
# python script in order to read them in
consumer_key        = 'ABCDEFGHIJKLKMNOPQRSTUVWXYZ'
consumer_secret     = '1234567890ABCDEFGHIJKLMNOPQRSTUVXYZ'
access_token        = 'ZYXWVUTSRQPONMLKJIHFEDCBA'
access_token_secret = '0987654321ZYXWVUTSRQPONMLKJIHFEDCBA'




def getDogeBal():
     """
    This function pulls in my current Testnet
    Doge balance as a json file, casts it as 
    a String and returns a String containing
    my current Balance 
    
    """
    url = "https://block.io/api/v2/get_balance/?api_key=c562-fd68-d1b9-b1a5"
    
    #store the response of URL
    response = urlopen(url)
    
    # storing the JSON response 
    # from url in data
    data_json = json.loads(response.read())
    #print(data_json)
    k = str(data_json)
    return "Tyler's Doge Balance: " + k[76:89] 

def getBlockCount():
    """
    This function returns the total Doge 
    blockcount as a String
    """
    blockCountUrl = 'https://dogechain.info/chain/Dogecoin/q/getblockcount'
    blockCountResponse = urlopen(blockCountUrl)
    data_json = json.loads(blockCountResponse.read())
    str_data_json = str(data_json)
    return "\n" + "Block Count: " + str_data_json

def totalMined():
    """
    This function returns the total amount of 
    Dofe mined as a String
    """
    totalMinedUrl = "http://dogechain.info/chain/Dogecoin/q/totalbc"
    totalMinedResponse = urlopen(totalMinedUrl)
    data_json = json.loads(totalMinedResponse.read())
    str_data_json = str(data_json)
    return "\n" + "Total Amount of Doge Mined: " + str_data_json


def tweetDogeBal():
    """
    This function is used to tweet my Testnet
    Doge balance as well as some Doge chain 
    statistics 
    """  
    twitter = Twython(
    consumer_key, consumer_secret, access_token, access_token_secret)
    now = str(datetime.now()) + "\n"
    message = now + getDogeBal() + getBlockCount() + totalMined() + "\n @dogecoin"
    twitter.update_status(status=message)
    print("Tweeted: %s" % message)

def tweetBlockCount():
    twitter = Twython(
    consumer_key, consumer_secret, access_token, access_token_secret)
    count = getBlockCount()
    twitter.update_status(status=count)

"""
def atMeTweets():
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    
    base_url = "https://twitter.com/T_Conley1/status/"
    
    # Define the search term and the date_since date as variables
    #search_words = "@greg16676935420"
    search_words = "T_Conley1 good morning to everyone even the people its not morning for"
    new_search = search_words + " -filter:retweets"    
    date_since = "2021-10-24"
    date = datetime.today()
    # collect most recent morning tweet 
    
    tweets = tw.Cursor(api.search_tweets, q=new_search, lang="en", since=date_since).items(1)

    
    T = [str(tweet.id) + tweet.user.screen_name + ' '  + tweet.text  for tweet in tweets]    
    for el in T:
        print(el)
        
    # authenticate through Twython
    twitter = Twython(consumer_key, 
                      consumer_secret, 
                      access_token, 
                      access_token_secret)
    message = base_url + str(T[0]) + ' ' + "good night to everyone except for the people its not night for" 
    print(message)
    #twitter.update_status(status=message)
"""


def graphGregAndTyler():
    """
    This function tweets a graph comparing the 
    total number of tweets Greg and Tyler have
    made in the past 24hrs 
    """
    # authenticate 
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth)
        
    startDate = date.today() 
    endDate = startDate - timedelta(days = 1)
    
    search_tyler = "@T_Conley1"
    search_greg = "@greg16676935420"
    
    total24HourTweetsTyler = get_past_24hour_tweets(search_tyler)
    total24HourTweetsGreg = get_past_24hour_tweets(search_greg)
    
    print("Tyler Total Tweets(past 24hrs):", total24HourTweetsTyler)
    print("Greg Total Tweets(past 24hrs):", total24HourTweetsGreg) 
    
    

    fig = plt.figure()
    plt.style.use('ggplot')
    
    x = ['@greg16676935420', '@T_Conley1']
    y = [total24HourTweetsGreg, total24HourTweetsTyler]
    
    x_pos = [i for i, _ in enumerate(x)]
    
    plt.bar(x_pos, y, color='green')
    plt.xlabel("PERSON", fontsize=20)
    plt.ylabel("NUMBER OF TWEETS", fontsize=20)
    plt.title("TWEETS IN PAST 24HRS")
    plt.xticks(x_pos, x)

    plt.show()
    plt.savefig('chart.png')
    
    #Generate text tweet with media (image)
    
    twitter = Twython(
    consumer_key, consumer_secret, access_token, access_token_secret)
 
    photo = 'chart.png'
    tweet_text = "tweets in past 24 hours from these two accounts from morning and night time @greg16676935420"
    
    photo = open('chart.png', 'rb')
    response = twitter.upload_media(media=photo)
    twitter.update_status(status=tweet_text, media_ids=[response['media_id']])

def get_past_24hour_tweets(username):
    """
    This function is used to return the total number
    of tweets created by a certain user during the
    past 24 hour period
    """
    # authenticate 
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
        
    endDate = datetime.today() 
    startDate= endDate - timedelta(days = 1)
    
    tweets = api.user_timeline(screen_name=username)
    
    Tlist =[]

    for t in tweets:
        if str(t.created_at)[0:19] > str(startDate)[0:19]:
            Tlist.append(t.text)
    #print(len(Tlist))
    return len(Tlist)


def findLastMorningTweet():
    """ 
    This function is used to find and return
    the ID of the most recent morning tweet
    that I have scheduled in Postman
    """
    # authenticate 
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    
    twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)

    endDate = datetime.today() 
    startDate= endDate - timedelta(days = 1)
    
    search_words = "T_Conley1 good morning to everyone even the people its not morning for"
    new_search = search_words + " -filter:retweets"
    tweets = tw.Cursor(api.search_tweets, q=new_search, lang="en").items(1)

    
    lastID = 0
    for t in tweets:
        if t.text == "good morning to everyone even the people its not morning for":
            if t.id > lastID:
                lastID = t.id
    print("Last Morning Tweet ID: ",lastID)
    return lastID


tweetDogeBal()




