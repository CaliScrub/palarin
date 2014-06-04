'''
Created on Feb 17, 2014

@author: noskillz
'''
import webapp2

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from utilities import emailutil
from businesslayer import transaction
from businesslayer import dwolla
from utilities import constants

class AdminPage(webapp2.RequestHandler):
    def get(self, operation):
        self.response.headers['Content-Type'] = 'text/plain'
        respData = ''
        if operation=='testop':
            respData = 'This is only a test'
        elif operation=='send_completion_emails':
            trans_id = self.request.get('reference_number')
            if trans_id != None:
                t_dict = transaction.get_transaction_and_people_from_trans_id(trans_id)
                emailutil.send_palarin_completion_emails(t_dict['transaction'],
                                                         t_dict['sender'],
                                                         t_dict['recipient'])
                transaction.update_transaction_remittance_status(trans_id, constants.REMITTANCE_STATUS_FUNDS_PAID)
                respData = 'attempted sending deposit complete emails'
                self.response.status = 200
            else:
                respData = 'transaction does not exist for sending deposit complete emails'
                self.response.status = 500
        elif operation=='get_transaction_info':
            trans_id = self.request.get('reference_number')
            if trans_id != None:
                params = {}
                t_dict = transaction.get_transaction_and_people_from_trans_id(trans_id)
                sender = t_dict['sender']
                recipient = t_dict['recipient']
                t = t_dict['transaction']
                params = {}
                params['autoid'] = t.autoid
                params['remittance_amount_needed'] = t.remittance_amount_needed
                params['remittance_amount_from'] = t.remittance_amount_from
                params['remittance_amount_to'] = t.remittance_amount_to
                params['sender'] = '%s %s' % (sender.first_name, sender.last_name)
                params['recipient'] = '%s %s' % (recipient.first_name, recipient.last_name)
                params['created_date'] = t.created_date
                params['bank_name'] = t.recipient_bank_name
                params['bank_account'] = transaction.get_bank_account_from_transaction(t)
                respData = """
<html>
<head>
<style>
table, th, td
{
border: 1px solid black
}
</style>
</head>
<body>
<h2>Transaction Info</h2>
<table>
    <tr>
        <th>Transaction ID</th>
        <th>Total amount needed</th>
        <th>Remittance amount in dollars</th>
        <th>Pesos to be remitted</th>
        <th>Sender</th>
        <th>Recipient</th>
        <th>Created Date</th>
        <th>Bank name</th>
        <th>Bank Account</th>
    </tr>
    <tr>
        <td>%(autoid)s</td>
        <td>%(remittance_amount_needed)s</td>
        <td>%(remittance_amount_from)s</td>
        <td>%(remittance_amount_to)s</td>
        <td>%(sender)s</td>
        <td>%(recipient)s</td>
        <td>%(created_date)s</td>
        <td>%(bank_name)s</td>
        <td>%(bank_account)s</td>
    </tr>
</table>
</body>
</html>
""" % params
                self.response.headers['Content-Type'] = 'text/html'
                self.response.status = 200
            else:
                respData = 'transaction does not exist'
                self.response.status = 500
        else:
            respData = 'Hello, webapp World!'
        self.response.out.write(respData)

class UnpaidTransactionPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html>')
        self.response.out.write('<head>')
        self.response.out.write("""
<style>
table, th, td
{
border: 1px solid black
}
</style>
""")
        self.response.out.write('</head>')
        # headers
        self.response.out.write("""
<form name="link_transaction" method="post">
<h2>Unpaid Transactions</h2>
<table>
    <tr>
        <th>Transaction ID</th>
        <th>Total amount needed</th>
        <th>Remittance amount in dollars</th>
        <th>Pesos to be remitted</th>
        <th>Sender</th>
        <th>Recipient</th>
        <th>Created Date</th>
        <th>Choose</th>
    </tr>
""")
        for t in transaction.get_unpaid_transactions():
            t_dict = transaction.get_transaction_and_people_from_trans_id(t.autoid)
            sender = t_dict['sender']
            recipient = t_dict['recipient']
            params = {}
            params['autoid'] = t.autoid
            params['remittance_amount_needed'] = t.remittance_amount_needed
            params['remittance_amount_from'] = t.remittance_amount_from
            params['remittance_amount_to'] = t.remittance_amount_to
            params['sender'] = '%s %s' % (sender.first_name, sender.last_name)
            params['recipient'] = '%s %s' % (recipient.first_name, recipient.last_name)
            params['created_date'] = t.created_date
            self.response.out.write("""
<tr>
    <td>%(autoid)s</td>
    <td>%(remittance_amount_needed)s</td>
    <td>%(remittance_amount_from)s</td>
    <td>%(remittance_amount_to)s</td>
    <td>%(sender)s</td>
    <td>%(recipient)s</td>
    <td>%(created_date)s</td>
    <td><input type="radio" name="transaction" value="%(autoid)s"/></td>
</tr>
""" % params)
        self.response.out.write('</table>')
        self.response.out.write("""
<h2>Unattached Dwolla payments</h2>
<table>
    <tr>
        <th>Dwolla transaction ID</th>
        <th>Sender</th>
        <th>Recipient</th>
        <th>Amount</th>
        <th>Sent Date</th>
        <th>Status</th>
        <th>Choose</th>
    </tr>
""")
        for dt in dwolla.get_unattached_dwolla_payments():
            dt_dict = dwolla.get_transaction_and_people_from_trans_id(dt.id)
            source = dt_dict['source']
            destination = dt_dict['destination']
            params = {}
            params['id'] = dt.id
            params['source'] = source.name
            params['destination'] = destination.name
            params['amount'] = dt.amount
            params['sent_date'] = dt.sent_date
            params['status'] = dt.status
            self.response.out.write("""
<tr>
    <td>%(id)s</td>
    <td>%(source)s</td>
    <td>%(destination)s</td>
    <td>%(amount)s</td>
    <td>%(sent_date)s</td>
    <td>%(status)s</td>
    <td><input type="radio" name="dwolla_transaction" value="%(id)s"/></td>
</tr>
""" % params)
        self.response.out.write('</table>')
        self.response.out.write("""
<input type="submit" value="Link"/>
</form>
""")
        self.response.out.write('</body>')
        self.response.out.write('</html>')
    
    def post(self):
        params = {}
        params['trans_id'] = self.request.get('transaction')
        params['dwolla_trans_id'] = self.request.get('dwolla_transaction')
        success = False
        try:
            dwolla.link_dwolla_transaction_and_transaction_request(params['dwolla_trans_id'], params['trans_id'])
            success = True
        except:
            success = False
        params['success'] = str(success)
        self.response.out.write("""
<html>
<body>
Attempting to link transaction: %(trans_id)s with dwolla transaction: %(dwolla_trans_id)s
<br/><br/>
Success is %(success)s?
<br/><br/>
<form method="get" name="go_back">
    <input type="submit" value="Go back"/>
</form>
</body>
</html>
""" % params)

class MarkCompletedTransactionsPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html>')
        self.response.out.write('<head>')
        self.response.out.write("""
<style>
table, th, td
{
border: 1px solid black
}
</style>
""")
        self.response.out.write('</head>')
        # headers
        self.response.out.write("""
<form name="link_transaction" method="post">
<h2>Remittances not marked as complete but with payments attached</h2>
<table>
    <tr>
        <th>Transaction ID</th>
        <th>Total amount needed</th>
        <th>Remittance amount in dollars</th>
        <th>Pesos to be remitted</th>
        <th>Sender</th>
        <th>Recipient</th>
        <th>Created Date</th>
        <th>Choose</th>
    </tr>
""")
        for t in transaction.get_paid_noncompleted_transactions():
            t_dict = transaction.get_transaction_and_people_from_trans_id(t.autoid)
            sender = t_dict['sender']
            recipient = t_dict['recipient']
            params = {}
            params['autoid'] = t.autoid
            params['remittance_amount_needed'] = t.remittance_amount_needed
            params['remittance_amount_from'] = t.remittance_amount_from
            params['remittance_amount_to'] = t.remittance_amount_to
            params['sender'] = '%s %s' % (sender.first_name, sender.last_name)
            params['recipient'] = '%s %s' % (recipient.first_name, recipient.last_name)
            params['created_date'] = t.created_date
            self.response.out.write("""
<tr>
    <td>%(autoid)s</td>
    <td>%(remittance_amount_needed)s</td>
    <td>%(remittance_amount_from)s</td>
    <td>%(remittance_amount_to)s</td>
    <td>%(sender)s</td>
    <td>%(recipient)s</td>
    <td>%(created_date)s</td>
    <td><input type="radio" name="transaction" value="%(autoid)s"/></td>
</tr>
""" % params)
        self.response.out.write("""
<tr>
    <td><input type="text" name="custom_transaction_id" value=""/></td>
    <td>Choose your own transaction ID</td>
    <td><input type="radio" name="transaction" value="custom"/></td>
</tr>
""")
        self.response.out.write('</table>')
        self.response.out.write("""
<input type="submit" value="Mark Completed and Send Confirmation Emails"/>
</form>
""")
        self.response.out.write('</body>')
        self.response.out.write('</html>')
    
    def post(self):
        trans_id = self.request.get('transaction')
        if trans_id == 'custom':
            trans_id = self.request.get('custom_transaction_id')
        params = {}
        params['trans_id'] = trans_id
        success = False
        try:
            if trans_id != None:
                t_dict = transaction.get_transaction_and_people_from_trans_id(trans_id)
                emailutil.send_palarin_completion_emails(t_dict['transaction'],
                                                         t_dict['sender'],
                                                         t_dict['recipient'])
                transaction.update_transaction_remittance_status(trans_id, constants.REMITTANCE_STATUS_FUNDS_PAID)
                success = True
            else:
                success = False
        except:
            success = False
        params['success'] = str(success)
        self.response.out.write("""
<html>
<body>
Attempting to mark complete and send confirmation emails for: %(trans_id)s
<br/><br/>
Success is %(success)s?
<br/><br/>
<form method="get" name="go_back">
    <input type="submit" value="Go back"/>
</form>
</body>
</html>
""" % params)

app = webapp2.WSGIApplication([('/adminonly/etc/(.*)', AdminPage),
                               ('/adminonly/unpaidtransactions/', UnpaidTransactionPage),
                               ('/adminonly/markcompleted/', MarkCompletedTransactionsPage)], debug=True)