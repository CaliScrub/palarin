'''
Created on Feb 15, 2014

@author: noskillz
'''
import urllib
import urllib2
import json

class CoinBaseAPI():
    baseUrl = 'https://coinbase.com/api/v1/'
    
    def get_exchange_rates(self):
        url = self.baseUrl + 'currencies/exchange_rates/'
        try:
            data = urllib.urlopen(url).read()
            dataDict = json.loads(data)        
            return dataDict
        except urllib2.HTTPError, e:
            data3 = e.read()
            print data3
            return None
    
    def get_exchange_rate(self, from_curr, to_curr):
        dataDict = self.get_exchange_rates()
        if dataDict != None:
            from_l = from_curr.lower()
            to_l = to_curr.lower()
            rate = float(dataDict['%s_to_%s' % (from_l, to_l)])
            return rate
        else:
            return 0
    
    def get_usd_pricedata_for_bitcoin_purchase(self, bitcoins):
        rate = self.get_exchange_rate('btc', 'usd')
        btc_value = rate * bitcoins
        fee = (btc_value * 0.01) + 0.15
        total_price = btc_value + fee
        retDict = {'rate': rate, 'btc_value': btc_value,
                   'fee': fee, 'total_price': total_price}
        return retDict