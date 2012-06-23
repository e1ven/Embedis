#!/usr/bin/env python3
#
# Copyright 2011 Pluric
    
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import socket
import json
from collections import OrderedDict
from tornado.options import define, options
import urllib.request, urllib.parse, urllib.error
import embedis


import re
try:
   from hashlib import md5 as md5_func
except ImportError:
   from md5 import new as md5_func


define("port", default=8080, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        """
        Wrap the default RequestHandler with extra methods
        """    
        super(BaseHandler,self).__init__(*args,**kwargs)

class iframeHandler(BaseHandler):
    def get(self,x,y,url):
        if self.request.query is not "":
            # Normally, I'd do a check for 'not None' but this string represents the query, it is literally empty.
            url = url + "?" + self.request.query
            
        self.write("<iframe class='embedis' type='text/html' width='" + x + "' height='" + y  +"' src='http://embed.is/url/" +x + "/"+y+"/"+url +"' frameborder='0' marginheight='0' marginwidth='0' scrolling='no' sandbox='allow-scripts'></iframe>")
      
class URLHandler(BaseHandler):
    def get(self,x,y,url):
        url = url + "?" + self.request.query
        if url[:6] == 'http:/':
            if url[6] != '/':
                url = 'http://' + url[6:]
        if url[:7] == 'https:/':
            if url[7] != '/':
                url = 'https://' + url[7:]
        print(url)
        emb = embedis.embedis(x,y)
        result = emb.lookup(url)
        if result is None:
            self.set_status(204)
        else:
            self.set_status(200)
            self.write(result)       

class ScramHandler(BaseHandler):
    def get(self,anything='whatever'):
        self.write("The services which run on this site are not for the general public at the current time.<br> Thanks for understanding!")

def main():
    print("Embedis is now listening.")
    application = tornado.web.Application([
        (r"/iframe/([0-9]+)/([0-9]+)/(.*)", iframeHandler),
        (r"/url/([0-9]+)/([0-9]+)/(.*)", URLHandler),
        (r"/(.*)", ScramHandler),
        (r"/images/(.*)", tornado.web.StaticFileHandler, {"path": "images/")}),

        (r"/", ScramHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
