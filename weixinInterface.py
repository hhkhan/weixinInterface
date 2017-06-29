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
        #��ȡ�������
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #�Լ���token
        token="hello_dobes_here_we_go" #�����д����΢�Ź���ƽ̨�������token
        #�ֵ�������
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1�����㷨        

        #���������΢�ŵ�������ظ�echostr
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
        str_xml = web.data() #���post��������
        xml = etree.fromstring(str_xml)#����XML����
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        if msgType == "text":
			content=xml.find("Content").text#����û������������
			return self.render.reply_text(fromUser,toUser,int(time.time()),u"�����ڻ��ڿ����У���û��ʲô���ܣ����ղ�˵���ǣ�"+ content)
        elif msgType == "image":
			picId = xml.find("MediaId").text
			return self.render.reply_image(fromUser,toUser,int(time.time()), picId)
        elif msgType == "voice":
			voiceId = xml.find("MediaId").text   
			return self.render.reply_voice(fromUser,toUser,int(time.time()), voiceId)
        elif msgType == "video":
			videoId = xml.find("MediaId").text
			#return self.render.reply_vedio(fromUser,toUser,int(time.time()), videoId)
			return self.render.reply_text(fromUser,toUser,int(time.time()), u"��ʱ����֧��С��Ƶ")
        elif msgType == "location": #��ȡ������λ����Ϣ
			location_x = xml.find("Location_X").text
			location_y = xml.find("Location_Y").text
			location_text = xml.find("Label").text
			return self.render.reply_text(fromUser,toUser,int(time.time()),u"��γ��Ϊx = " + location_x + " y = " + location_y + u" λ��Ϊ��" + location_text)
        elif msgType == "shortvideo":
			svideoId = xml.find("MediaId").text
            #return self.render.reply_vedio(fromUser,toUser,int(time.time()), svideoId, "title", u"����")
			return self.render.reply_text(fromUser,toUser,int(time.time()),svideoId)
        else:
			return self.render.reply_text(fromUser,toUser,int(time.time()), u"����Ϊ" + msgType +u"sorry, unsupported types")