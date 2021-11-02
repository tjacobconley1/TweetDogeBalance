#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 00:28:53 2021

@author: fieldemployee
"""


from datetime import datetime
from datetime import timedelta
import tweepy as tw
from twython import Twython


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

# create Twython object with your Twitter dev portal credentials
twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)

# create a Tweepy object with Twitter dev keys
auth = tw.OAuthHandler(consumer_key, consumer_secret)
# set the access token attributes to your provided tokens 
# from Twitter dev portal
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

def quoteMorningTweet():
 
    # This variable holds the URL of the most recent
    # Morning Tweet 
    # base Url: https://twitter.com/T_Conley1/status/
    lastMornID = findLastMorningTweet()

    #print(lastMornID)
    api.update_status("good night to everyone except for the people its not night for", attachment_url=lastMornID)

 
 

def findLastMorningTweet():
    """ 
    This function is used to find and return
    the ID of the most recent morning tweet
    that I have scheduled in Postman
    """
    # set a start and end time values to contain 
    # only the prior 24 hours
    endDate = datetime.today() 
    startDate= endDate - timedelta(days = 1)
     
    # search for tweet from my account containing
    # the string in this variable
    search_words = "T_Conley1 good morning to everyone even the people its not morning for"
    # this variable is used as a RESTFUL search parameter
    # that filters out retweets
    new_search = search_words + " -filter:retweets"
    # pulls in all tweets within the specified parameters
    # into a variable that acts like a json object
    # 
    tweets = tw.Cursor(api.search_tweets, q=new_search, lang="en").items(1)
     
    # set the variable for previous ID to 0 
    lastID = 0
    # iterate through the json object variable
    for t in tweets:
        # check to see if that tweet object's text value
        # matches my automated morning tweet
        if t.text == "good morning to everyone even the people its not morning for":
            # if the text value matches compare the tweet object's
            # ID, the greater the value the more recent the tweet
            if t.id > lastID:
                lastID = t.id
    
    # print the URL found to the console
    print("Last Morning Tweet ID: ", "https://twitter.com/T_Conley1/status/" + str(lastID))
    # return the URL to be used by the quote tweet function
    return "https://twitter.com/T_Conley1/status/" + str(lastID)


#findLastMorningTweet()
quoteMorningTweet()

 
