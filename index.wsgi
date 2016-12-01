# coding: UTF-8

#def application(environ, start_response):
#    start_response('200 ok', [('content-type', 'text/plain')])
#    return ['Hello, SAE!']


import os
import sys
import sae
import web
 
from weixinInterface import WeixinInterface

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'email'))
 
urls = (
'/weixin','WeixinInterface'
)
 
app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)
 
app = web.application(urls, globals()).wsgifunc()        
application = sae.create_wsgi_app(app)
