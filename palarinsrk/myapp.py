import webapp2

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from lbc_request_handler import LbcApiPage
from random_handlers import NdbTestPage
from random_handlers import EmailListPage
from order_handler import OrderPage


class MainPage(webapp2.RequestHandler):
    
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/lapi/(.*)', LbcApiPage),
                               ('/testndb/(.*)', NdbTestPage),
                               ('/email/(.*)', EmailListPage),
                               ('/order/(.*)', OrderPage)], debug=True)

"""
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
"""