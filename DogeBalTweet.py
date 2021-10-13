

# TEST NET
# https://block.io/api/v2/get_balance/?api_key=c562-fd68-d1b9-b1a5

# import urllib library
from urllib.request import urlopen
import json
from twython import Twython

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
    now = datetime.now()
    return "Tyler's Doge Balance: " + k[76:89] + '\n' + str(now)

def tweetDogeBal():
    twitter = Twython(
    consumer_key, consumer_secret, access_token, access_token_secret)
    message = str(getDogeBal())
    twitter.update_status(status=message)
    print("Tweeted: %s" % message)

getDogeBal()
tweetDogeBal()





