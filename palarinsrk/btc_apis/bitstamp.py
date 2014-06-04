'''
Created on Feb 15, 2014

@author: noskillz
'''
import urllib
import urllib2
import json

def get_last_bitstamp_btc_price():
    url = 'https://www.bitstamp.net/api/ticker/'
    try:
        data = urllib.urlopen(url).read()
        dataDict = json.loads(data)        
        return float(dataDict['last'])
    except urllib2.HTTPError, e:
        data3 = e.read()
        print data3
        return None

def pass_through_bitstamp_ticker():
    url = 'https://www.bitstamp.net/api/ticker/'
    try:
        data = urllib.urlopen(url).read()      
        return data
    except urllib2.HTTPError, e:
        data3 = e.read()
        print data3
        return None