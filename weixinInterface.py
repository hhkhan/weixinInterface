# -*- coding: utf-8 -*-
import hashlib
import web
#import lxml
import time
import os
import urllib2,json
from lxml import etree

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="hello_dobes_here_we_go" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法        

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr
        
    def get_token():
        payload_access_token={
            'grant_type':'client_credential',
            'appid':'wxe8e8776ed21f376f',
            'secret':'7cc3aab213bc27302cf829bcde97829d'
        }
        token_url='https://api.weixin.qq.com/cgi-bin/token'
        r=requests.get(token_url,params=payload_access_token)
        dict_result= (r.json())
        return dict_result['access_token']
    
    def get_media_ID(path):
        img_url='https://api.weixin.qq.com/cgi-bin/material/add_material'
        payload_img={
            'access_token':get_token(),
            'type':'image'
        }
        data ={'media':open(path,'rb')}
        r=requests.post(url=img_url,params=payload_img,files=data)
        dict =r.json()
        return dict['media_id']
    
    def POST(self):        
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        if msgType == "text":
			content=xml.find("Content").text#获得用户所输入的内容
			return self.render.reply_text(fromUser,toUser,int(time.time()),u"我现在还在开发中，还没有什么功能，您刚才说的是："+ content)
        elif msgType == "image":
			picId = xml.find("MediaId").text
			return self.render.reply_image(fromUser,toUser,int(time.time()), picId)
        elif msgType == "voice":
			voiceId = xml.find("MediaId").text   
			return self.render.reply_voice(fromUser,toUser,int(time.time()), voiceId)
        elif msgType == "video":
			videoId = xml.find("MediaId").text
			#return self.render.reply_vedio(fromUser,toUser,int(time.time()), videoId)
			return self.render.reply_text(fromUser,toUser,int(time.time()), u"暂时还不支持小视频")
        elif msgType == "location": #读取发来的位置信息
			location_x = xml.find("Location_X").text
			location_y = xml.find("Location_Y").text
			location_text = xml.find("Label").text
			return self.render.reply_text(fromUser,toUser,int(time.time()),u"经纬度为x = " + location_x + " y = " + location_y + u" 位置为：" + location_text)
        elif msgType == "shortvideo":
			svideoId = xml.find("MediaId").text
            #return self.render.reply_vedio(fromUser,toUser,int(time.time()), svideoId, "title", u"描述")
			return self.render.reply_text(fromUser,toUser,int(time.time()),svideoId)
        else:
			return self.render.reply_text(fromUser,toUser,int(time.time()), u"类型为" + msgType +u"sorry, unsupported types")