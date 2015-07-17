#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import os
import requests
from urllib import urlencode
import json

BASE_URL = 'http://access.alchemyapi.com/calls'
ENDPOINT = '/image/ImageGetRankedImageKeywords'
APIKEY = '<YOUR API KEY>'
PORT = int(os.getenv('VCAP_APP_PORT', 8080))

class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.s = requests.Session()

    def get(self):
        self.render("index.html", kwords = {}, s = "")

    def post(self):
    	print "In POST"
        options = {}
        imgfile = self.request.files['imgfile'][0]
        print imgfile['filename']
        options['apikey'] = APIKEY
        options['imagePostMode'] = 'raw'
        options['outputMode'] = 'json'
        image = imgfile['body']

        try:
            post_url = BASE_URL + ENDPOINT + '?' + urlencode(options).encode('utf-8')
        except TypeError:
            post_url = BASE_URL + ENDPOINT + '?' + urlencode(options)

        try:
            results = self.s.post(url=post_url, data=image)
        except Exception as e:
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'network-error'}

        r = results.json()

        # print json.dumps(r, default=json_util.default)

        self.write(json.dumps(r))






settings = {
'template_path': 'templates',
'static_path': 'static',
"xsrf_cookies": False
}

handlers = [(r"/", MainHandler)]

application = tornado.web.Application(handlers, debug=True, **settings)

if __name__ == "__main__":

    application.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
