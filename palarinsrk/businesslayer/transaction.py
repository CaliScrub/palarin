'''
Created on Feb 16, 2014

@author: noskillz
''' 
from google.appengine.ext import ndb

from datalayer.entities import TransactionRequest
from datalayer.entities import Person
from datalayer import ndb_operations
from utilities import exchange_rate
from utilities import crypto
from utilities import constants

def create_transaction(receiver, sender, from_curr, to_curr, amount, exchange, fee, discount, bankname, bankaccount):
    receiver_key = receiver.key
    sender_key = sender.key
    from_amount = float(amount)
    fee_amount = float(fee)
    discount_amount = float(discount)
    exchange_rate = float(exchange)
    needed_amount = from_amount + fee_amount - discount_amount
    to_amount = exchange_rate * from_amount
    (account_enc, account_iv) = crypto.AES_encrypt_account(bankaccount)
    autoid = ndb_operations.get_increment_counter_value("TransactionRequestIdNext")
    return ndb_operations.create_transaction_request(receiver_key, sender_key, from_curr, to_curr,
                                                     needed_amount, from_amount, to_amount, exchange_rate,
                                                     bankname, account_enc, account_iv, fee_amount,
                                                     discount_amount, autoid)

def get_transaction_from_id(trans_id):
    return ndb_operations.get_transaction_request_from_id(trans_id)

def get_unpaid_transactions():
    return ndb_operations.get_unpaid_transactions()

def get_paid_noncompleted_transactions():
    return ndb_operations.get_paid_noncompleted_transactions()

def get_transaction_and_people_from_trans_id(trans_id):
    transaction = ndb_operations.get_transaction_request_from_id(trans_id)
    sender = ndb_operations.get_person_from_key(transaction.sender)
    recipient = ndb_operations.get_person_from_key(transaction.recipient)
    t_dict = {}
    t_dict['transaction'] = transaction
    t_dict['sender'] = sender
    t_dict['recipient'] = recipient
    return t_dict

def update_transaction_remittance_status(trans_id, status):
    transaction = ndb_operations.get_transaction_request_from_id(trans_id)
    transaction.remittance_status = status
    ndb_operations.update_transaction(transaction)

def update_transaction_incoming_money_status(trans_id, status):
    transaction = ndb_operations.get_transaction_request_from_id(trans_id)
    transaction.incoming_money_status = status
    ndb_operations.update_transaction(transaction)

def get_bank_account_from_transaction(transaction):
    ciphertext = transaction.recipient_bank_account_encrypted
    iv = transaction.recipient_bank_account_iv
    return crypto.AES_decrypt_account(ciphertext, iv)

def get_masked_bank_account_from_transaction(transaction):
    raw_account = get_bank_account_from_transaction(transaction)
    return raw_account[-4:].rjust(16, '*')

def remittance_status_to_string(remittance_status):
    remit_stat_strings = {}
    remit_stat_strings[constants.REMITTANCE_STATUS_CREATED] = 'Pending'
    remit_stat_strings[constants.REMITTANCE_STATUS_FUNDS_PAID] = 'Funds paid to recipient'
    if remit_stat_strings.has_key(remittance_status):
        return remit_stat_strings[remittance_status]
    else:
        return 'No status found'