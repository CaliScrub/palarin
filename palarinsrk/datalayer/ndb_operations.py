'''
Created on Feb 16, 2014

@author: noskillz
'''
import string

from google.appengine.ext import ndb

from entities import TransactionRequest
from entities import Person
from entities import LocalBitCoinsAd
from entities import EmailTemplate
from entities import IncrementCounter
from entities import EmailList
from entities import DwollaPerson
from entities import DwollaTransaction

from utilities import constants

def create_person(firstname, lastname, email):
    p_key = ndb.Key(Person, string.join((firstname, lastname, email), '|'))
    p = Person(key=p_key)
    p.first_name = firstname
    p.last_name = lastname
    p.email = email
    p.put()
    return p

def get_person(firstname, lastname, email):
    p_key = ndb.Key(Person, string.join((firstname, lastname, email), '|'))
    p = p_key.get()
    return p

def get_person_from_key(p_key):
    p = p_key.get()
    return p

def create_transaction_request(receiver_key, sender_key, from_curr, to_curr,
                               needed_amount, from_amount, to_amount, exchange_rate, bankname, account_enc, account_iv,
                               fee=0, discount=0, autoid=0):
    t = TransactionRequest()
    t.recipient = receiver_key
    t.sender = sender_key
    t.from_currency = from_curr
    t.exchange_rate = exchange_rate
    t.to_currency = to_curr
    t.remittance_amount_needed = needed_amount
    t.remittance_amount_from = from_amount
    t.remittance_amount_to = to_amount
    t.recipient_bank_name = bankname
    t.recipient_bank_account_encrypted = account_enc
    t.recipient_bank_account_iv = account_iv
    t.remittance_amount_fee = fee
    t.remittance_amount_discount = discount
    if autoid > 0:
        t.autoid = autoid
        t.key = ndb.Key(TransactionRequest, str(autoid))
    t.put()
    return t

def update_transaction(transaction):
    transaction.put()
    return transaction

def insert_or_update_email_template(template_name, template_body, template_text_body):
    e_key = ndb.Key(EmailTemplate, template_name)
    e = e_key.get()
    if e == None:
        e = EmailTemplate(key=e_key)
        e.template_name = template_name
    e.template_body = template_body
    e.template_text_body = template_text_body
    e.put()
    return e

def get_email_template(template_name):
    e_key = ndb.Key(EmailTemplate, template_name)
    e = e_key.get()
    return e    

def get_transaction_request_from_urlsafekey(urlsafekey):
    t = ndb.Key(urlsafe=urlsafekey).get()
    return t

def get_transaction_request_from_id(trans_id):
    t = ndb.Key(TransactionRequest, str(trans_id)).get()
    return t

def get_unpaid_transactions():
    return TransactionRequest.query(TransactionRequest.incoming_money_status.IN([constants.INCOMING_MONEY_STATUS_START,
                                                                                 constants.INCOMING_MONEY_STATUS_PARTIAL])).fetch()

def get_paid_noncompleted_transactions():
    subquery = TransactionRequest.query(
        TransactionRequest.incoming_money_status.IN([constants.INCOMING_MONEY_STATUS_PENDING_FULL,
                                                     constants.INCOMING_MONEY_STATUS_RECEIVED]))
    #return subquery.filter(TransactionRequest.remittance_status != constants.REMITTANCE_STATUS_FUNDS_PAID).fetch()
    transactions = subquery.fetch()
    for t in transactions:
        if t.remittance_status == constants.REMITTANCE_STATUS_FUNDS_PAID:
            transactions.remove(t)
    return transactions
            

def insert_and_return_dwolla_person(id, name, type):
    dp_key = ndb.Key(DwollaPerson, string.join((id, name, type), '|'))
    dp = dp_key.get()
    if (dp == None):
        dp = DwollaPerson(key=dp_key)
    dp.id = id
    dp.name = name
    dp.type = type
    dp.put()
    return dp

def get_dwolla_person_from_key(dp_key):
    dp = dp_key.get()
    return dp

def insert_or_update_dwolla_transaction(transaction_id, source_key, dest_key,
                                        amount, status, type, clearing_date,
                                        sent_date, notes, source_dp_key, dest_dp_key,
                                        trans_request_key=None):
    dt_key = ndb.Key(DwollaTransaction, str(transaction_id))
    dt = dt_key.get()
    if dt == None:
        dt = DwollaTransaction(key=dt_key)
        dt.id = transaction_id
        dt.amount = amount
    dt.type = type
    dt.status = status
    dt.sent_date = sent_date
    dt.clearing_date = clearing_date
    dt.notes = notes
    dt.source = source_dp_key
    dt.destination = dest_dp_key
    if trans_request_key != None and dt.transaction_request == None:
        dt.transaction_request = trans_request_key
    dt.put()
    return dt

def get_dwolla_transaction_from_dwolla_trans_id(dwolla_id):
    dt_key = ndb.Key(DwollaTransaction, str(dwolla_id))
    dt = dt_key.get()
    return dt

def get_unattached_dwolla_payments():
    return DwollaTransaction.query(DwollaTransaction.transaction_request == None).fetch()

def update_transaction_dwolla_join(trans_request_key, dwolla_trans_key):
    dt = dwolla_trans_key.get()
    if dt != None:
        dt.transaction_request = trans_request_key
        dt.put()

def insert_or_update_email_subscription(listname, email, do_subscribe):
    el_key = ndb.Key(EmailList, string.join((listname, email), '|'))
    el = el_key.get()
    if (el == None):
        el = EmailList(key=el_key)
        el.listname = listname
        el.email = email
    el.subscribed = do_subscribe
    el.put()
    return el

def get_increment_counter_value(counter_name):
    c_key = ndb.Key(IncrementCounter, counter_name)
    c = c_key.get()
    if (c == None):
        c = IncrementCounter(key=c_key)
        c.counter_name = counter_name
        c.increment_value = 0
    c.increment_value = c.increment_value + 1
    c.put()
    return c.increment_value