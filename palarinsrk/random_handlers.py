'''
Created on Feb 15, 2014

@author: noskillz
'''
'''
Created on Feb 13, 2014

@author: noskillz
'''
import webapp2
import string
import logging
from google.appengine.api import taskqueue

from businesslayer import transaction
from datalayer.entities import TransactionRequest
from datalayer.entities import Person
from datalayer import ndb_operations

from utilities import tempconstants
from datalayer.entities import TestLog

from btc_apis import bitstamp

class EmailListPage(webapp2.RequestHandler):
    def post(self, operation):
        respData = None
        if operation == 'subscribe':
            listname = 'NotificationList'
            email = self.request.get('emailAddress')
            ndb_operations.insert_or_update_email_subscription(listname, email, True)
            respData = 'subscription call'
            self.response.status = 200
            self.redirect('http://www.palarin.com/')
        elif operation == 'unsubscribe':
            listname = 'NotificationList'
            email = self.request.get('emailAddress')
            ndb_operations.insert_or_update_email_subscription(listname, email, False)
            respData = 'unsubscription call'
            self.response.status = 200
        else:
            respData = 'operation not found: %s' % operation
            self.response.status = 500
        self.response.out.write(respData)



class NdbTestPage(webapp2.RequestHandler):
    def get(self, operation):
        respData = None
        self.response.headers['Content-Type'] = 'text/html'
        if operation == 'testdwollacallback':
            paramlist = []
            for key in self.request.params.keys():
                paramlist.append('[%s: %s]' % (key, self.request.params[key]))
            t = TestLog()
            t.logtext = 'dwolla callback get params passed were: %s' % string.join(paramlist, ',')
            t.put()
            respData = 'hey, this worked, and the get params passed were: %s' % string.join(paramlist, ',')
        elif operation == 'store_and_note':
            dollars = self.request.get('dollars')
            testEntity = TransactionRequest()
            testEntity.email = ''
            testEntity.amount = float(dollars)
            key = testEntity.put()
            keystring = key.urlsafe()
            taskqueue.add(url='/lapi/post_ad', params={'ndbkey': keystring, 'dollars': dollars})
            respData = 'entity entered: %s' % keystring
        elif operation == 'store_person':
            firstname = self.request.get('firstname')
            lastname = self.request.get('lastname')
            email = self.request.get('email')
            ndb_operations.create_person(firstname, lastname, email)
            respData = 'guess it worked?'
        elif operation == 'get_person':
            firstname = self.request.get('firstname')
            lastname = self.request.get('lastname')
            email = self.request.get('email')
            p = ndb_operations.get_person(firstname, lastname, email)
            if p != None:
                respData = 'person found with firstname: %s, lastname: %s, email: %s' % (firstname, lastname, email)
            else:
                respData = 'person not found'
        elif operation == 'store_transaction':
            r_firstname = self.request.get('r_firstname')
            r_lastname = self.request.get('r_lastname')
            r_email = self.request.get('r_email')
            receiver = ndb_operations.create_person(r_firstname, r_lastname, r_email)
            s_firstname = self.request.get('s_firstname')
            s_lastname = self.request.get('s_lastname')
            s_email = self.request.get('s_email')
            sender = ndb_operations.create_person(s_firstname, s_lastname, s_email)
            from_curr = self.request.get('from_curr')
            to_curr = self.request.get('to_curr')
            from_amount = self.request.get('amount')
            bankname = self.request.get('bankname')
            bankaccount = self.request.get('bankaccount')
            t = transaction.create_transaction(receiver, sender, from_curr, to_curr, from_amount, bankname, bankaccount)
            if t != None:
                respData = 'transaction urlsafe key is: %s' % t.key.urlsafe()
            else:
                respData = 'did not work'
        elif operation == 'decode_bank':
            urlsafekey = self.request.get('key')
            t = ndb_operations.get_transaction_request_from_urlsafekey(urlsafekey)
            account = transaction.get_bank_account_from_transaction(t)
            respData = 'is your account number... %s?' % account
        elif operation == 'form_test':
            firstname = self.request.get('firstName')
            lastname = self.request.get('lastName')
            email = self.request.get('yourEmail')
            ndb_operations.create_person(firstname, lastname, email)
            respData = 'attempted to create person with first name: %s, last name: %s, email: %s' % (firstname, lastname, email)
            self.redirect('http://projectshoryuken.wix.com/palarin#!remit-funds-now-step-2/c1ps')
        elif operation == 'create_email_template_kind':
            e = ndb_operations.insert_or_update_email_template('remittance_submission_notification',
                                                               tempconstants.remittance_substance_confirmation_html_body,
                                                               tempconstants.remittance_substance_confirmation_text_body)
            respData = 'check if this worked'
        elif operation == 'update_email_template_complete':
            e = ndb_operations.insert_or_update_email_template('remittance_completion_sender_notification',
                                                               tempconstants.remittance_completion_sender_body,
                                                               tempconstants.remittance_completion_sender_text_body)
            e = ndb_operations.insert_or_update_email_template('remittance_completion_recipient_notification',
                                                               tempconstants.remittance_completion_recipient_body,
                                                               tempconstants.remittance_completion_recipient_text_body)
            respData = 'check if these two worked'
        elif operation == 'bitstamp_ticker_passthrough':
            self.response.headers.add_header("Access-Control-Allow-Origin", "*")
            respData = bitstamp.pass_through_bitstamp_ticker()
            self.response.headers['Content-Type'] = 'text/json'    
        elif operation == 'view_email_template':
            e = ndb_operations.get_email_template('remittance_submission_notification')
            params = {}
            params['sender_first_name'] = 'test_first'
            params['sender_last_name'] = 'test_last'
            params['sender_email'] = 'a@a.com'
            params['recipient_first_name'] = 'r_first'
            params['recipient_last_name'] = 'r_last'
            params['recipient_email'] = 'b@b.com'
            params['bank'] = 'bopa'
            params['masked_account'] = 'xxxxxxxx1234'
            params['from_amount'] = 10
            params['exchange_rate'] = 35
            params['to_amount'] = 3500
            params['total_from_amount'] = 10.5
            params['discount'] = 0
            params['fee'] = 0.5
            params['reference_number'] = 23432423424
            params['status'] = 'Pending'
            params['funds_available_date'] = '4/1/2014' 
            respData = e.template_body % params
        else:
            respData = 'failed operation: "' + operation + '"'
        self.response.out.write(respData)

    def post(self, operation):
        respData = None
        if operation == 'testdwollacallback':
            paramlist = []
            for key in self.request.params.keys():
                paramlist.append('[%s: %s]' % (key, self.request.params[key]))
            t = TestLog()
            t.logtext = 'dwolla callback post params passed were: %s' % string.join(paramlist, ',')
            t.put()
            t2 = TestLog()
            t2.logtext = 'dwolla callback post body is: %s ' % self.request.body
            t2.put()
            respData = 'hey, this worked, and the post params passed were: %s' % string.join(paramlist, ',')
            self.response.status = 200
        else:
            respData = 'failed operation "%s"' % operation
        self.response.headers['Content-Type'] = 'text/json'
        self.response.out.write(respData)