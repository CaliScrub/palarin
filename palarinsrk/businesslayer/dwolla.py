'''
Created on Mar 8, 2014

@author: noskillz
'''
import json
import logging
import datetime

from datalayer.entities import DwollaPerson
from datalayer.entities import DwollaTransaction
from datalayer import ndb_operations
from utilities import constants

def handle_dwolla_callback(body):
    logging.getLogger().setLevel(logging.DEBUG)
    result = False
    try:
        logging.debug('Handling Dwolla Callback with body: %s' % body)
        d_dict = json.loads(body)
        trans_dict = d_dict['Transaction']
        source_dict = trans_dict['Source']
        dest_dict = trans_dict['Destination']
        source_dp = ndb_operations.insert_and_return_dwolla_person(source_dict['Id'], source_dict['Name'], source_dict['Type'])
        dest_dp = ndb_operations.insert_and_return_dwolla_person(dest_dict['Id'], dest_dict['Name'], dest_dict['Type'])
        source_key = source_dp.key
        dest_key = dest_dp.key
        transaction_id = int(trans_dict['Id'])
        type = trans_dict['Type']
        amount = float(trans_dict['Amount'])
        status = trans_dict['Status']
        dwolla_datetime_format = '%Y-%m-%dT%H:%M:%SZ'
        try:
            sent_date = datetime.datetime.strptime(trans_dict['SentDate'], dwolla_datetime_format)
            clearing_date = datetime.datetime.strptime(trans_dict['ClearingDate'], dwolla_datetime_format)
        except Exception as e:
            logging.exception('Issue saving dates for dwolla callback; continuing on')
        notes = trans_dict['Notes']
        dt = ndb_operations.insert_or_update_dwolla_transaction(transaction_id, source_key, dest_key,
                                                                amount, status, type, clearing_date,
                                                                sent_date, notes, source_key, dest_key)
        if dt != None:
            result = True
    except Exception as e:
        logging.exception("Error handling Dwolla callback")
    return result

def get_unattached_dwolla_payments():
    return ndb_operations.get_unattached_dwolla_payments()

def get_transaction_and_people_from_trans_id(dwolla_id):
    dwolla_trans = ndb_operations.get_dwolla_transaction_from_dwolla_trans_id(dwolla_id)
    source = ndb_operations.get_dwolla_person_from_key(dwolla_trans.source)
    destination = ndb_operations.get_dwolla_person_from_key(dwolla_trans.destination)
    dt_dict = {}
    dt_dict['transaction'] = dwolla_trans
    dt_dict['source'] = source
    dt_dict['destination'] = destination
    return dt_dict

def link_dwolla_transaction_and_transaction_request(dwolla_id, trans_id):
    dwolla_trans = ndb_operations.get_dwolla_transaction_from_dwolla_trans_id(dwolla_id)
    transaction = ndb_operations.get_transaction_request_from_id(trans_id)
    ndb_operations.update_transaction_dwolla_join(transaction.key, dwolla_trans.key)
    transaction.incoming_money_status = constants.INCOMING_MONEY_STATUS_PENDING_FULL
    transaction.put()