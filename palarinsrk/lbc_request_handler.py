'''
Created on Feb 13, 2014

@author: noskillz
'''
import webapp2
from google.appengine.ext import ndb

from btc_apis.lbc import LocalBitCoinsAPI
from btc_apis.lbc import lbcAccessToken
from btc_apis.bitstamp import get_last_bitstamp_btc_price
from btc_apis.coinbase import CoinBaseAPI
from datalayer.entities import TransactionRequest
from utilities import exchange_rate 


class LbcApiPage(webapp2.RequestHandler):
    def get(self, operation):
        lapi = LocalBitCoinsAPI()
        capi = CoinBaseAPI()
        lapi.access_token = lbcAccessToken()
        lapi.access_token.token = '9fb58446c594ab2f5f0373d0f01cc371905bd415'
        respData = None
        if operation == 'self':
            #respData = lapi.api_myself()
            respData = 'closed for maintenance'
        elif operation == 'wallet':
            #respData = lapi.api_wallet()
            respData = 'closed for maintenance'
        elif operation == 'post_ad':
            dollars = self.request.get('dollars')
            pesos = exchange_rate.get_pesos_from_usd(dollars)
            lowest_ask = lapi.get_lowest_ask_price('PHP')
            parameters = 'dollars: %s, pesos: %s' % (dollars, pesos)
            bitcoins_needed = pesos * 1.0 / lowest_ask
            btc_params = 'at lowest bitcoins ask of %s you need %s bitcoins' % (lowest_ask, bitcoins_needed)
            bitstampusd = get_last_bitstamp_btc_price()
            price_from_bitstamp = bitcoins_needed * bitstampusd
            bitstamp_params = 'at bitstamp rate %s it would cost %s dollars' % (bitstampusd, price_from_bitstamp)
            coinbase_vals = capi.get_usd_pricedata_for_bitcoin_purchase(bitcoins_needed)
            coinbase_params = 'at coinbase rate %s it would cost %s total dollars - %s for the bitcoins and %s for fees' % \
                (coinbase_vals['rate'], coinbase_vals['total_price'], coinbase_vals['btc_value'], coinbase_vals['fee'])
            keystring = self.request.get('ndbkey')
            #if keystring != None:
            #    ndbkey = ndb.Key(urlsafe=keystring)
            #    tItem = ndbkey.get()
            #    tItem.notes = '%s -- %s -- %s' % (parameters, btc_params, bitstamp_params)
            #    tItem.put()
            respData = '%s\n%s\n%s\n%s' % (parameters, btc_params, bitstamp_params, coinbase_params)
        else:
            respData = 'failed operation: "' + operation + '"'
        self.response.headers['Content-Type'] = 'text/json'
        self.response.out.write(respData)
