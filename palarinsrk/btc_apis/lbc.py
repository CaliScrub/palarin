'''
Created on Feb 10, 2014

@author: noskillz
'''
import urllib
import urllib2
import json

class lbcAccessToken:
    token = ''
    scope = ''
    refresh_token = ''
    expires_in = 0
    token_type = ''
    expire_date = None
    
    def __init__(self, jsonToken=None):
        if (jsonToken != None):
            tokenDict = json.loads(jsonToken)
            self.token = tokenDict['access_token']
            self.scope= tokenDict['scope']
            self.expires_in = tokenDict['expires_in']
            self.refresh_token = tokenDict['refresh_token']
            self.token_type = tokenDict['token_type'] 
    
    

class LocalBitCoinsAPI:
    code = ''
    access_token = None
    refresh_token = ''
    client_id = 'e4e8fb526928511765fd'
    client_secret = '053068c373a7f4f2b61fb447bc66d972b9d065a6'
    base_url = 'https://localbitcoins.com/'
    base_public_charts_url = 'https://localbitcoins.com/bitcoincharts/'
    
    def get_new_access_token(self, code=None):
        url = self.base_url + 'oauth2/access_token/'
        if code == None:
            code = self.code
        params = urllib.urlencode({
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': self.code,
            'grant_type': 'authorization_code'
        })
        request = urllib2.Request(url, params)
        try:
            data = urllib2.urlopen(request).read()
            self.access_token = lbcAccessToken(jsonToken=data) 
        except urllib2.HTTPError, e:
            data3 = e.read()
            print data3
    
    def api_myself(self, access_token=None):
        url = self.base_url + 'api/myself/'
        if access_token == None:
            access_token = self.access_token.token
        params = urllib.urlencode({
            'access_token': access_token
        })
        request = urllib2.Request(url, params)
        try:
            data = urllib2.urlopen(request).read()
            return data
            #dataDict = json.loads(data)
            #return dataDict
        except urllib2.HTTPError, e:
            data3 = e.read()
            print data3
            return None
    
    def api_wallet(self, access_token=None):
        url = self.base_url + 'api/wallet/?%s'
        if access_token == None:
            access_token = self.access_token.token
        params = urllib.urlencode({
            'access_token': access_token
        })
        try:
            data = urllib.urlopen(url % params).read()
            return data
            #dataDict = json.loads(data)
            #return dataDict
        except urllib2.HTTPError, e:
            data3 = e.read()
            print data3
            return None
    
    def public_api_orderbook(self, currency='USD'):
        url = self.base_public_charts_url + ('%s/orderbook.json' % currency)
        try:
            data = urllib.urlopen(url).read()
            return data
            #dataDict = json.loads(data)
            #return dataDict
        except urllib2.HTTPError, e:
            data3 = e.read()
            print data3
            return None
    
    def get_lowest_ask_price(self, currency='USD'):
        data = self.public_api_orderbook(currency)
        try:
            if data != None:
                dataDict = json.loads(data)
                return float(dataDict['asks'][0][0])
            else:
                return 0
        except:
            return -1
    
    def list_ads(self, access_token=None):
        url = self.base_url + 'api/ads/?%s'
        if access_token == None:
            access_token = self.access_token.token
        params = urllib.urlencode({
            'access_token': access_token
        })
        try:
            data = urllib.urlopen(url % params).read()
            return data
        except urllib2.HTTPError, e:
            data3 = e.read()
            print data3
            return None
    
    def create_ad(self, min_amount, max_amount,
                  price_equation, lat, lon, city, location_string,
                  countrycode, account_info, bankname,
                  sms_verification_required, track_max_amount,
                  require_trusted_by_advertiser, currency,
                  access_token=None):
        url = self.base_url + 'api/ad-create/'
        if access_token == None:
            access_token = self.access_token.token
        params = urllib.urlencode({
            'access_token': access_token
        })
        request = urllib2.Request(url, params)
        try:
            data = urllib2.urlopen(request).read()
            return data
            #dataDict = json.loads(data)
            #return dataDict
        except urllib2.HTTPError, e:
            data3 = e.read()
            print data3
            return None

def test_only_lapi():
    lapi = LocalBitCoinsAPI()
    lapi.access_token = lbcAccessToken()
    lapi.access_token.token = '9fb58446c594ab2f5f0373d0f01cc371905bd415'
    return lapi

if __name__ == '__main__':
    lapi = LocalBitCoinsAPI()
    lapi.access_token = lbcAccessToken()
    lapi.access_token.token = '9fb58446c594ab2f5f0373d0f01cc371905bd415'
    print lapi.api_myself()