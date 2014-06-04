'''
Created on Feb 15, 2014

@author: noskillz
'''
import urllib
import urllib2
import json

def yahoo_exchange_from(from_curr, to_curr, amt):
    url = 'http://query.yahooapis.com/v1/public/yql?%s'
    params = urllib.urlencode({
                'q': 'select * from yahoo.finance.xchange where pair in ("%s%s")' % (from_curr.upper(), to_curr.upper()),
                'format': 'json',
                'env': 'store://datatables.org/alltableswithkeys'
            })
    try:
        data = urllib.urlopen(url % params).read()
        exchangeDict = json.loads(data)['query']
        result = exchangeDict['results']['rate']['Rate']
        return float(result) * amt
    except urllib2.HTTPError, e:
        data3 = e.read()
        print data3
        return None

def rateexchangegae_exchange_from(from_curr, to_curr, amt):
    url = 'http://rate-exchange.appspot.com/currency?%s'
    params = urllib.urlencode({
                'from': from_curr,
                'to': to_curr,
                'q': amt
            })
    try:
        data = urllib.urlopen(url % params).read()
        exchangeDict = json.loads(data)        
        return exchangeDict['v']
    except urllib2.HTTPError, e:
        data3 = e.read()
        print data3
        return None

def exchange_from(from_curr, to_curr, amt):
    retryLimit = 5
    numRetries = 0
    while True:
        try:
            return yahoo_exchange_from(from_curr, to_curr, amt)
        except urllib2.HTTPError, e:
            if numRetries > retryLimit:
                raise e
            else:
                numRetries += 1
            

def get_pesos_from_usd(dollars):
    return exchange_from('USD', 'PHP', dollars)