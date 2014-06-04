'''
Created on Feb 17, 2014

@author: noskillz
'''
from datetime import timedelta
from google.appengine.api import mail
from datalayer import ndb_operations
import businesslayer

def send_palarin_email(recipient_address, subject, body):
    sender_address = 'Palarin Customer Care <palarincustomercare@gmail.com>'
    mail.send_mail(sender_address, recipient_address, subject, body)
    
def send_palarin_email_message(message):
    message.send()
    
def send_palarin_transaction_key_email(recipient_address, urlsafekey):
    subject = 'Palarin transaction key'
    body = """
Thank you for beginning a Palarin transaction! Please save the following transaction key which you will need for the next step in the process.

Transaction key: %s

DO NOT reply to this email
Send any questions to customercare@palarin.com
""" % urlsafekey
    send_palarin_email(recipient_address, subject, body)

def send_palarin_transaction_email(transaction, sender, receiver):
    message = mail.EmailMessage()
    message.subject = 'Palarin Order Confirmation'
    params = {}
    params['sender_first_name'] = sender.first_name
    params['sender_last_name'] = sender.last_name
    params['sender_email'] = sender.email
    params['recipient_first_name'] = receiver.first_name
    params['recipient_last_name'] = receiver.last_name
    params['recipient_email'] = receiver.email
    params['bank'] = transaction.recipient_bank_name
    params['masked_account'] = businesslayer.transaction.get_masked_bank_account_from_transaction(transaction)
    params['from_amount'] = "{:.2f}".format(transaction.remittance_amount_from)
    params['to_amount'] = "{:.2f}".format(transaction.remittance_amount_to)
    params['exchange_rate'] = (transaction.remittance_amount_to / transaction.remittance_amount_from)
    params['total_from_amount'] = "{:.2f}".format(transaction.remittance_amount_needed)
    params['discount'] = "{:.2f}".format(transaction.remittance_amount_discount)
    params['fee'] = "{:.2f}".format(transaction.remittance_amount_fee)
    if transaction.autoid != None and transaction.autoid > 0:
        params['reference_number'] = transaction.autoid
    else:
        params['reference_number'] = transaction.key.urlsafe()
    params['status'] = businesslayer.transaction.remittance_status_to_string(transaction.remittance_status)
    params['funds_available_date'] = transaction.created_date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=2)
    email_template = ndb_operations.get_email_template('remittance_submission_notification')
    message.html = email_template.template_body % params
    message.body = email_template.template_text_body % params
    message.to = sender.email
    message.bcc = 'project.shoryuken@gmail.com'
    message.sender = 'Palarin Customer Care <palarincustomercare@gmail.com>'
    send_palarin_email_message(message)
    
def send_palarin_completion_emails(transaction, sender, receiver):
    params = {}
    params['sender_first_name'] = sender.first_name
    params['sender_last_name'] = sender.last_name
    params['sender_email'] = sender.email
    params['recipient_first_name'] = receiver.first_name
    params['recipient_last_name'] = receiver.last_name
    params['recipient_email'] = receiver.email
    params['bank'] = transaction.recipient_bank_name
    params['masked_account'] = businesslayer.transaction.get_masked_bank_account_from_transaction(transaction)
    params['from_amount'] = "{:.2f}".format(transaction.remittance_amount_from)
    params['to_amount'] = "{:.2f}".format(transaction.remittance_amount_to)
    params['exchange_rate'] = (transaction.remittance_amount_to / transaction.remittance_amount_from)
    params['total_from_amount'] = "{:.2f}".format(transaction.remittance_amount_needed)
    params['discount'] = "{:.2f}".format(transaction.remittance_amount_discount)
    params['fee'] = "{:.2f}".format(transaction.remittance_amount_fee)
    if transaction.autoid != None and transaction.autoid > 0:
        params['reference_number'] = transaction.autoid
    else:
        params['reference_number'] = transaction.key.urlsafe()
    # sender confirmation
    email_template = ndb_operations.get_email_template('remittance_completion_sender_notification')
    message = mail.EmailMessage()
    message.subject = 'Palarin Deposit Confirmation'
    message.html = email_template.template_body % params
    message.body = email_template.template_text_body % params
    message.to = sender.email
    message.bcc = 'project.shoryuken@gmail.com'
    message.sender = 'Palarin Customer Care <palarincustomercare@gmail.com>'
    send_palarin_email_message(message)
    # recipient confirmation
    email_template = ndb_operations.get_email_template('remittance_completion_recipient_notification')
    message = mail.EmailMessage()
    message.subject = 'Palarin Deposit Confirmation'
    message.html = email_template.template_body % params
    message.body = email_template.template_text_body % params
    message.to = receiver.email
    message.bcc = 'project.shoryuken@gmail.com'
    message.sender = 'Palarin Customer Care <palarincustomercare@gmail.com>'
    send_palarin_email_message(message)