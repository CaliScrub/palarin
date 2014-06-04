'''
Created on Feb 15, 2014

@author: noskillz
'''
from google.appengine.ext import ndb

class Person(ndb.Model):
    email = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    updated_date = ndb.DateTimeProperty(auto_now=True)

class TransactionRequest(ndb.Model):
    '''
    classdocs
    '''
    sender = ndb.KeyProperty(kind=Person)
    from_currency = ndb.StringProperty()
    to_currency = ndb.StringProperty()
    exchange_rate = ndb.FloatProperty()
    remittance_amount_from = ndb.FloatProperty()
    remittance_amount_to = ndb.FloatProperty()
    remittance_amount_needed = ndb.FloatProperty(default=0)
    remittance_amount_fee = ndb.FloatProperty(default=0)
    remittance_amount_discount = ndb.FloatProperty(default=0)
    recipient = ndb.KeyProperty(kind=Person)
    recipient_bank_name = ndb.StringProperty()
    recipient_bank_account_encrypted = ndb.BlobProperty()
    recipient_bank_account_iv = ndb.BlobProperty()
    notes = ndb.StringProperty()
    remittance_status = ndb.IntegerProperty(default=100)
    fund_replacement_status = ndb.IntegerProperty(default=200)
    incoming_money_status = ndb.IntegerProperty(default=400)
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    updated_date = ndb.DateTimeProperty(auto_now=True)
    autoid = ndb.IntegerProperty(default=0)

class EmailList(ndb.Model):
    listname = ndb.StringProperty()
    email = ndb.StringProperty()
    subscribed = ndb.BooleanProperty()

class DwollaPerson(ndb.Model):
    id = ndb.StringProperty()
    name = ndb.StringProperty()
    type = ndb.StringProperty()

class DwollaTransaction(ndb.Model):
    transaction_request = ndb.KeyProperty(kind=TransactionRequest)
    source = ndb.KeyProperty(kind=DwollaPerson)
    destination = ndb.KeyProperty(kind=DwollaPerson)
    id = ndb.IntegerProperty()
    type = ndb.StringProperty()
    status = ndb.StringProperty()
    amount = ndb.FloatProperty()
    sent_date = ndb.DateTimeProperty()
    clearing_date = ndb.DateTimeProperty()
    notes = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    updated_date = ndb.DateTimeProperty(auto_now=True)

class LocalBitCoinsAd(ndb.Model):
    transaction = ndb.KeyProperty(kind=TransactionRequest)
    lbc_ad_id = ndb.IntegerProperty()
    orig_currency = ndb.StringProperty()
    orig_curr_amount = ndb.FloatProperty()
    min_amount = ndb.FloatProperty() 
    max_amount = ndb.FloatProperty()
    currency = ndb.StringProperty()
    price_equation = ndb.StringProperty()
    lat = ndb.FloatProperty()
    lon = ndb.FloatProperty()
    city = ndb.StringProperty()
    location_string = ndb.StringProperty()
    ad_status = ndb.IntegerProperty(default=300)
    countrycode = ndb.StringProperty()
    account_info = ndb.StringProperty()
    bankname = ndb.StringProperty()
    sms_verification_required = ndb.BooleanProperty()
    track_max_amount = ndb.BooleanProperty()
    require_trusted_by_advertiser = ndb.BooleanProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    updated_date = ndb.DateTimeProperty(auto_now=True)

class EmailTemplate(ndb.Model):
    template_body = ndb.TextProperty()
    template_text_body = ndb.TextProperty()
    template_name = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    updated_date = ndb.DateTimeProperty(auto_now=True)

class IncrementCounter(ndb.Model):
    counter_name = ndb.StringProperty()
    increment_value = ndb.IntegerProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    updated_date = ndb.DateTimeProperty(auto_now=True)

class TestLog(ndb.Model):
    created_date = ndb.DateTimeProperty(auto_now=True)
    logtext = ndb.TextProperty()