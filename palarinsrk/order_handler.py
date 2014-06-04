'''
Created on Feb 16, 2014

@author: noskillz
'''
import webapp2
import urllib
import urllib2

from google.appengine.api import taskqueue

from businesslayer import transaction
from businesslayer import lbc_ad
from businesslayer import dwolla
from datalayer.entities import TransactionRequest
from datalayer.entities import Person
from datalayer import ndb_operations
from utilities import emailutil
from businesslayer.lbc_ad import create_lbc_ad_from_trans_key



class OrderPage(webapp2.RequestHandler):
    def get(self, operation):
        respData = None
        if operation == 'dwolla_submitted':
            self.redirect('http://www.palarin.com/#!remit-funds-now-step-3/c8jw')
        elif operation == 'prepare_lbc_ad':
            urlsafekey=self.request.get('tkey')
            lbc = lbc_ad.create_lbc_ad_from_trans_key(urlsafekey)
            if lbc != None:
                respData = 'guess it worked?'
            else:
                respData = 'ERROR, ERROR'            
        else:
            respData = 'operation does not exist for GET: "' + operation + '"'
        self.response.out.write(respData)
        
    def post(self, operation):
        respData = None
        if operation == 'order1':
            respData = 'starting out'
            r_firstname = self.request.get('recipientFirstName')
            r_lastname = self.request.get('recipientLastName')
            r_email = self.request.get('recipientEmail')
            receiver = ndb_operations.create_person(r_firstname, r_lastname, r_email)
            respData = 'saved recipient'
            s_firstname = self.request.get('senderFirstName')
            s_lastname = self.request.get('senderLastName')
            s_email = self.request.get('yourEmail')
            sender = ndb_operations.create_person(s_firstname, s_lastname, s_email)
            respData = 'saved sender'
            from_curr = 'USD'
            to_curr = 'PHP'
            from_amount = self.request.get('remittanceAmount')
            bankname = self.request.get('Philippine Banks')
            bankaccount = self.request.get('accountNumber')
            exchange_rate = self.request.get('exchangeRate')
            fee = self.request.get('serviceFee')
            discount = self.request.get('discount')
            t = transaction.create_transaction(receiver, sender, from_curr, to_curr, from_amount,
                                               exchange_rate, fee, discount, bankname, bankaccount)
            emailutil.send_palarin_transaction_email(t, sender, receiver)
            self.redirect('http://www.palarin.com/#!remit-funds-now-step-2/c1ps')
        elif operation == 'dwolla_submitted':
            self.redirect('http://www.palarin.com/#!remit-funds-now-step-3/c8jw')
        elif operation == 'dwolla_callback':
            if dwolla.handle_dwolla_callback(self.request.body):
                respData = 'callback from dwolla succeeded'
                self.response.status = 200
            else:
                respData = 'callback from dwolla failed'
                self.response.status = 500
        else:
            respData = 'operation does not exist for POST: "' + operation + '"'
        self.response.out.write(respData)