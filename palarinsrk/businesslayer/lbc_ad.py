'''
Created on Feb 17, 2014

@author: noskillz
'''
from google.appengine.ext import ndb

from datalayer.entities import TransactionRequest
from datalayer.entities import LocalBitCoinsAd
from btc_apis import lbc
from datalayer import ndb_operations
from utilities import exchange_rate
from utilities import constants

def create_lbc_ad_from_trans_key(tkeystring):
    t = ndb.Key(urlsafe=tkeystring).get()
    return create_lbc_ad_from_transaction_request(t)

def create_lbc_ad_from_transaction_request(transactionRequest):
    lbc = LocalBitCoinsAd()
    lbc.transaction = transactionRequest.key
    lbc.min_amount = transactionRequest.remittance_amount_to
    lbc.max_amount = lbc.min_amount * 1.5
    lbc.currency = transactionRequest.to_currency
    lbc.orig_currency = transactionRequest.from_currency
    lbc.orig_curr_amount = transactionRequest.remittance_amount_from
    lbc.put()
    return lbc

def post_lbc_ad(lbcKey):
    lbc = lbcKey.get()
    if (lbc != None):
        lapi = lbc.test_only_lapi()
        ad_result = lapi.create_ad(min_amount=lbc.min_amount,
                       max_amount=lbc.max_amount,
                       price_equation=lbc.price_equation,
                       lat=lbc.lat,
                       lon=lbc.lon,
                       city=lbc.city,
                       location_string=lbc.location_string,
                       countrycode=lbc.countrycode,
                       account_info=lbc.account_info,
                       bankname=lbc.bankname,
                       sms_verification_required=lbc.sms_verification_required,
                       track_max_amount=lbc.track_max_amount,
                       require_trusted_by_advertiser=lbc.require_trusted_by_advertiser,
                       currency=lbc.currency)
        lbc.ad_status = constants.LBC_AD_STATUS_POSTED
        lbc.put()
    else:
        raise Exception('LBC Ad does not exist in database')

def test_only_prepare_lbc_ad(lbcKey):
    lbc = lbcKey.get()
    if (lbc != None):
        lbc.price_equation='bitstampusd*USD_in_PHP*1.03'
    else:
        raise Exception('LBC Ad does not exist in database')