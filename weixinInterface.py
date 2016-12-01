# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import string
import urllib2,json
import urllib
from lxml import etree
from stockIta import is_stockcode, get_stock_info, StockInfo
from EmailComm import fetch_report_from_Email

class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
    def GET(self):
        data = web.input()  #获取输入参数
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="xxx"  #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法
        
        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            #print echostr
            return echostr

    def POST(self):
        str_xml = web.data()  #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text	
        msgType=xml.find("MsgType").text
        
        if msgType=='text':
            content=xml.find("Content").text  #获得用户所输入的内容
            if content.lower()=='help':
                replayText = '（1）输入6位股票代码可返回股票信息，股票代码后附“+”返回简洁即时信息。\n'+\
                '（2）输入110、119或120、121、140可获取股票筛选信息。\n'\
                '其他功能正在开发中，期望您的更多建议。\n\n'\
                '『可将我们的图标添加到桌面，便于您访问。』'
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
            elif content=='110':
                msg_subject110 = 'stockanalysis-110'
                replayText = fetch_report_from_Email(msg_subject110)
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
            elif content=='119':
                msg_subject119 = 'stockanalysis-119'
                replayText = fetch_report_from_Email(msg_subject119)
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
            elif content=='120':
                msg_subject120 = 'stockanalysis-120'
                replayText = fetch_report_from_Email(msg_subject120)
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
            elif content=='121':
                msg_subject121 = 'stockanalysis-121'
                replayText = fetch_report_from_Email(msg_subject121)
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
            elif content=='140':
                msg_subject140 = 'stockanalysis-140'
                replayText = fetch_report_from_Email(msg_subject140)
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
            elif len(content)==7 and content[6]=='+':
                stockcode = content[0:6]
                shinfo = StockInfo(stockcode)  #创建实例
                replayText = shinfo.output_plain_info()  #生成短消息回复信息
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
            elif len(content)==6:
                stockcode=content
                shinfo = StockInfo(stockcode)  #创建实例
                if shinfo.is_stockcode:
                    newspage_data = shinfo.output_news_data()
                    return self.render.reply_xp(fromUser,toUser,int(time.time()),newspage_data)  #多项图文输出
                else:
                    replayText = shinfo.output_plain_info()  #生成回复信息
                    return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
            else:
                replayText = '您的输入有误...未来将会输出你输入关键字的百度搜索结果。'
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
        elif msgType=='event':
            content = xml.find("Event").text
            if content=='subscribe':  #如果是用户订阅事件，回复欢迎信息
                replayText = u'感谢您关注 La Passione Italia！本公众号为您提供股票查询分析服务，回复“help”了解操作方法。\n\n'+\
                u'功能：（1）输入6位股票代码返回股票信息；（2）输入110、119或120、121、140返回股票筛选信息。'
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
