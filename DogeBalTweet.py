

# TEST NET
# https://block.io/api/v2/get_balance/?api_key=c562-fd68-d1b9-b1a5

# import urllib library
from urllib.request import urlopen
import json
from twython import Twython
from datetime import datetime


#KEYS FROM THE TWITTER DEV PORTAL
consumer_key        = 'ABCDEFGHIJKLKMNOPQRSTUVWXYZ'
consumer_secret     = '1234567890ABCDEFGHIJKLMNOPQRSTUVXYZ'
access_token        = 'ZYXWVUTSRQPONMLKJIHFEDCBA'
access_token_secret = '0987654321ZYXWVUTSRQPONMLKJIHFEDCBA'




def getDogeBal():
      
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
    blockCountUrl = 'https://dogechain.info/chain/Dogecoin/q/getblockcount'
    blockCountResponse = urlopen(blockCountUrl)
    data_json = json.loads(blockCountResponse.read())
    str_data_json = str(data_json)
    return "\n" + "Block Count: " + str_data_json

def totalMined():
    totalMinedUrl = "http://dogechain.info/chain/Dogecoin/q/totalbc"
    totalMinedResponse = urlopen(totalMinedUrl)
    data_json = json.loads(totalMinedResponse.read())
    str_data_json = str(data_json)
    return "\n" + "Total Amount of Doge Mined: " + str_data_json


def tweetDogeBal():
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

tweetDogeBal()




