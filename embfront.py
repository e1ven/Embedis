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

class iframeHandler(tornado.web.RequestHandler):
    def get(self,x,y,url):
        url = url + "?" + self.request.query
        print(x)
        print(y)
        print(url)
        self.write("<iframe class='embedis' type='text/html' width='" + x + "' height='" + y  +"' src='http://embed.is/url/" +x + "/"+y+"/"+url +"' frameborder='0' marginheight='0' marginwidth='0' scrolling='no'></iframe>")
      
class URLHandler(tornado.web.RequestHandler):
    def get(self,x,y,url):
        url = url + "?" + self.request.query
        emb = embedis.embedis(x,y)
        self.write(emb.lookup(url))       

class ScramHandler(tornado.web.RequestHandler):
    def get(self,anything='whatever'):
        self.write("The services which run on this site are not for the general public at the current time.<br> Thanks for understanding!")

def main():
    print("Embedis is now listening.")
    application = tornado.web.Application([
        (r"/iframe/([0-9]+)/([0-9]+)/(.*)", iframeHandler),
        (r"/url/([0-9]+)/([0-9]+)/(.*)", URLHandler),
        (r"/(.*)", ScramHandler),
        (r"/", ScramHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
