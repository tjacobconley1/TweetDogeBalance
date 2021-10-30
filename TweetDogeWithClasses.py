#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
import numpy as np

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

secretPin = "abcdefghij123456"

dogeApiKey = "a123-b456-c789-d000" 
dogeAddress = "abcdefghijklmnopqrstuvwxyz012345678"



# perform API authorizations 
block_io = BlockIo(dogeApiKey, secretPin, version)
twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
    
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)




    

class TwitterAPI(object):
    def __init__(self, twitter, api):
        self.twitter = twitter
        self.api = api        

    def atMeTweets(self):
    
        base_url = "https://twitter.com/T_Conley1/status/"
    
        # Define the search term and the date_since date as variables
        #search_words = "@greg16676935420"
        search_words = "DOGE"
        new_search = search_words + " -filter:retweets"    
        #date_since = "2021-10-24"
        date = datetime.today() -1
        # collect most recent morning tweet 
        tweets = tw.Cursor(self.api.search_tweets, q=new_search, lang="en", since=date)

    
        T = [str(tweet.id) + tweet.user.screen_name + ' '  + tweet.text  for tweet in tweets]    
        for el in T:
            print(el)
        
        message = base_url + str(T[0]) + ' ' + "good night to everyone except for the people its not night for" 
        print(message)
        #twitter.update_status(status=message)
  
        
    def get_past_24hour_tweets(self, username):
        """
        This function is used to return the total number
        of tweets created by a certain user during the
        past 24 hour period
        """ 
        endDate = datetime.today() 
        startDate= endDate - timedelta(days = 1)
        
        tweets = self.api.user_timeline(screen_name=username)
        
        Tlist =[]
        
        for t in tweets:
            if str(t.created_at)[0:19] > str(startDate)[0:19]:
                Tlist.append(t.text)
                #print(len(Tlist))
                return len(Tlist)    
        
        
    def graphGregAndTyler(self):
        """
        This function tweets a graph comparing the 
        total number of tweets Greg and Tyler have
        made in the past 24hrs 
        """
        
        # time period (24hrs)
        startDate = date.today() 
        endDate = startDate - timedelta(days = 1)
    
        # Usernames from which the number 
        # of tweets will be counted
        search_tyler = "@T_Conley1"
        search_greg = "@greg16676935420"
        
        # Pulls in the total number of tweets 
        # of each user into a variable
        total24HourTweetsTyler = self.get_past_24hour_tweets(search_tyler)
        total24HourTweetsGreg = self.get_past_24hour_tweets(search_greg)
        
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
        
        
        photo = 'chart.png'
        tweet_text = "tweets in past 24 hours from these two accounts from morning and night time @greg16676935420"
        
        photo = open('chart.png', 'rb')
        response = twitter.upload_media(media=photo)
        self.twitter.update_status(status=tweet_text, media_ids=[response['media_id']])
        
        
    



    def quoteMorningTweet(self):
    
        # This variable holds the URL of the most recent
        # Morning Tweet 
        # base Url: https://twitter.com/T_Conley1/status/
        lastMornID = self.findLastMorningTweet()

        #print(lastMornID)
        self.api.update_status("good night to everyone except for the people its not night for", attachment_url=lastMornID)

    
    

    def findLastMorningTweet(self):
        """ 
        This function is used to find and return
        the ID of the most recent morning tweet
        that I have scheduled in Postman
        """
        endDate = datetime.today() 
        startDate= endDate - timedelta(days = 1)
        
        search_words = "T_Conley1 good morning to everyone even the people its not morning for"
        new_search = search_words + " -filter:retweets"
        tweets = tw.Cursor(self.api.search_tweets, q=new_search, lang="en").items(1)
        
        
        lastID = 0
        for t in tweets:
            if t.text == "good morning to everyone even the people its not morning for":
                if t.id > lastID:
                    lastID = t.id
                
        print("Last Morning Tweet ID: ", "https://twitter.com/T_Conley1/status/" + str(lastID))
        return "https://twitter.com/T_Conley1/status/" + str(lastID)
    
            
    
    
    
    
    
    
    def getUserTweetsContainingDOGE(self, user):
        """
        This function take a username and returns
        the total number of times that user has
        tweeted containing the word DOGE
        """
        search_words = "DOGE"
        tweets = self.api.user_timeline(screen_name=user,
                                         include_rts = False,
                                         count = 200,
                                         tweet_mode = 'extended')
    
        DOGEresult = 0
        dogecoinresult = 0
        Bitcoinresult = 0
        BB = 0
        for info in tweets[:]:
            if "DOGE" in info.full_text:
                DOGEresult +=1
                if "#dogecoin" in info.full_text:
                    dogecoinresult += 1
                if "#Bitcoin" in info.full_text:
                    Bitcoinresult += 1
                if "#BandanaBanana" in info.full_text:
                    BB +=1
            
        return [DOGEresult, dogecoinresult, Bitcoinresult, BB]


 
    def graphAndTweetDogeMentions(self):
        """
        This function uses the helper function getUserTweetsContainingDOGE()
        to pull back the number of times someone has tweeted about DOGE or
        Bitcoin 
        It then plots the results on a graph and tweets it at @greg16676935420
        """ 
        # time period (24hrs)
        startDate = date.today() 
        endDate = startDate - timedelta(days = 1)
        
        # Usernames from which the number 
        # of tweets will be counted
        search_tyler = "T_Conley1"
        search_greg = "greg16676935420"
        search_bret = "bretmichaels"
        
        # get results
        TyList = self.getUserTweetsContainingDOGE(search_tyler)
        GList = self.getUserTweetsContainingDOGE(search_greg)
        BMList = self.getUserTweetsContainingDOGE(search_bret)
        
        # print results to console
        print("TYLER\n", 
              "DOGE     :", TyList[0], '\n',
              "#dogecoin:", TyList[1], '\n',
              "#Bitcoin :", TyList[2], '\n',
              "#BandanaBanana:", TyList[3], '\n')
        print("GREG\n", 
              "DOGE     :", GList[0], '\n',
              "#dogecoin:", GList[1], '\n',
              "#Bitcoin :", GList[2], '\n',
              "#BandanaBanana:", GList[3], '\n')
        print("Bret Michaels\n", 
              "DOGE     :", BMList[0], '\n',
              "#dogecoin:", BMList[1], '\n',
              "#Bitcoin :", BMList[2], '\n',
              "#BandanaBanana:", BMList[3], '\n')    
        
        # create the plot
        fig = plt.figure()
        plt.style.use('ggplot')
        
        # the labels for the X axis
        X = ["DOGE", "#dogecoin", "#Bitcoin", "#BandanaBanana"]
        # values for each
        YTyler = TyList
        YGreg = GList
        YBret = BMList
        
        # to arange into ascending order
        X_axis = np.arange(len(X))
        
        # plot the bar graphs
        plt.bar(X_axis -0.2, YTyler, 0.4, label= "Tyler")
        plt.bar(X_axis +0.2, YGreg, 0.4, label = "Greg")
        plt.bar(X_axis, YBret, 0.4, label="Bret Michaels")
        
        # label them axi
        plt.xticks(X_axis, X)
        plt.xlabel("WORDS MENTIONED")
        plt.ylabel("NUMBER OF TIMES")
        plt.title("Number of times either Tyler or Greg mentioned either Bitcoin or Dogecoin on Twitter")
        plt.legend()
        plt.show()
        plt.savefig('GTDBchart.png')
        
        # generate a tweet with media (chart image)
        # chart name
        photo = 'GTDBchart.png'
        
        # text that will be tweeted with chart
        text_tweet = "number of mentions of crypto things and also bananas  @greg16676935420 @bretmichaels"
        
        # open photo file
        photo = open('GTDBchart.png', 'rb')
        
        # tweet it 
        response = twitter.upload_media(media=photo)
        self.twitter.update_status(status=text_tweet, media_ids=[response['media_id']])
        
        
        
        
        
class DOGEAPI(object):
    def __init__(self, dogeApiKey, secretPin, block_io, dogeAddress):
        self.dogeApiKey = dogeApiKey
        self.secretPin = secretPin
        self.block_io = block_io
        self.dogeAddress = dogeAddress
        
    def getDogeBal(self):
        """
        This function pulls in my current Testnet
        Doge balance as a json file, casts it as 
        a String and returns a String containing
        my current Balance 
        
        """
        url = "https://block.io/api/v2/get_balance/?api_key=" + self.dogeApiKey
        
        #store the response of URL
        response = urlopen(url)
        
        # storing the JSON response 
        # from url in data
        data_json = json.loads(response.read())
        #print(data_json)
        k = str(data_json)
        return "Tyler's Doge Balance: " + k[76:88] + '\n'
    
    def getEachAddressBal(self):
        """
        This function pulls back the balance of each of my
        current test doge addresses
        """
        address1 = '\n' + str(self.block_io.get_my_addresses(page=1))[95:130]
        address1Bal = "\nBalance: " + str(self.block_io.get_my_addresses(page=1))[217:229] + '\n'
        
        address2 = '\n' + str(self.block_io.get_my_addresses(page=1))[280:315]
        address2Bal = "\nBalance: " + str(self.block_io.get_my_addresses(page=1))[401:412] + '\n'
        
        return address1 + address1Bal + address2 + address2Bal

    
    
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
    
    
    
    
    def prepareDogeTransaction(self, amount, toAddress):
        
        res = self.block_io.prepare_transaction(amounts=amount, to_addresses=toAddress)
        print(res)
        
        signedres = self.block_io.create_and_sign_transaction(res)
        print(signedres)
        
        submitres = self.block_io.submit_transaction(transaction_data=signedres)
        print(submitres)
        #prepaddressUrl = "https://block.io/api/v2/prepare_transaction/?api_key=" + dogeApiKey + "&amounts=" + str(amount) + "&to_addresses=" + toAddress
        #prepareTransResponse = urlopen(prepaddressUrl)
        #data_json = json.loads(prepareTransResponse.read())
        #data_json
        #str_data_json = str(data_json)
        #return str_data_json
        
        
        
    def submitDogeTransaction(self):
        submitUrl = "https://block.io/api/v2/submit_transaction/?api_key=" + self.dogeApiKey
        os.system("curl https://block.io/api/v2/submit_transaction/?api_key=c562-fd68-d1b9-b1a5 -d 'transaction_data=" + self.prepareDogeTransaction(25, self.dogeAddress) + "' -H 'Content-Type: application/json'")
            
            
    def tweetDogeBal(self):
        """
        This function is used to tweet my Testnet
        Doge balance as well as some Doge chain 
        statistics 
        """
        now = "\n\nCurrent Time: " + str(datetime.today())[0:19] + "\n"
        message = self.getDogeBal() + self.getEachAddressBal() +  now + "\n @dogecoin"
        twitter.update_status(status=message)
        print("Tweeted: %s" % message)


  


#graphAndTweetDogeMentions()
#print(getEachAddressBal())           
#findLastMorningTweet()   
#def tweetPhoto():  
#prepareDogeTransaction(str(25), dogeAddress)
#print(block_io.get_balance())
#atMeTweets()
#get_past_24hour_tweets("@greg16676935420")
#get_past_24hour_tweets("@t_conley1")
#graphGregAndTyler()
#tweetDogeBal()
#quoteMorningTweet()
D = DOGEAPI(dogeApiKey, secretPin, block_io, dogeAddress)
print(D.getEachAddressBal())
D.tweetDogeBal()


