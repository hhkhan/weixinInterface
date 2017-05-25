# coding: UTF-8
import os
import sae
import web
#×Ô¼ºµÄtoken 7cc3aab213bc27302cf829bcde97829d app-id wxe8e8776ed21f376f
from weixinInterface import WeixinInterface

urls = (
'/','WeixinInterface'
)
#https://my.oschina.net/yangyanxing/blog/159215
app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)
web.config.debug = True

app = web.application(urls, globals()).wsgifunc()        
application = sae.create_wsgi_app(app)