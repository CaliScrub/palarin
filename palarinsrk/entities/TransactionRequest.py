'''
Created on Feb 15, 2014

@author: noskillz
'''
from google.appengine.ext import ndb

class TransactionRequest(ndb.Model):
    '''
    classdocs
    '''
    email = ndb.StringProperty()
    from_currency = ndb.StringProperty()
    to_currency = ndb.StringProperty()
    amount = ndb.FloatProperty()
    notes = ndb.StringProperty()