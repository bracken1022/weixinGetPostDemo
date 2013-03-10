#!/usr/bin/python
#-*- coding:utf8 -*-

import sae
from bottle import Bottle,debug,request
from bottle import jinja2_view as view

import xml.etree.ElementTree as ET
import urllib2

import catch_web


debug(True)
app = Bottle()

xml_msg = ""


@app.route('/') 
@app.route('/index')
@view('static/template/index.html')
def main_page_show():
  return {}
  
  
@app.route('/weixin', method='GET')
def weixin_app():
  echostr = request.GET.get('echostr')
  return echostr
  
@app.route('/weixin', method='POST')
def weixin_app():
  ip = request.environ.get('REMOTE_ADDR')
  info = parse_xml( request.body.read() )
  
  if 'Content' in info:
    con = info['Content']
  
  
  
  
  global xml_msg
  
  
  
  data = tuan_show()
  
  #xml_msg = "%s" %(response_news_msg(info, data ))
  xml_msg = "xinxi:" + request.body.read()
  
  result = response_news_msg(info, data )
  
  return result
  


@app.route('/test')
def test_show():
  info = {'ToUserName':'wang','FromUserName':'liu','CreateTime':'2012'}
  
  data = tuan_show()
  
  return response_news_msg(info, data)
  
@app.route('/tuanshow')
def tuan_show():
  url = 'http://www.budejie.com/'
  data = catch_web.catch_url( url )
  
  text = ""
  img = ""
  
  soup = data.findAll('div',{'id':'entry-list'})
  data = []
  
  for con in soup:
    text = con.p.string
    img = con.img['src']
    data.append({'text':text, 'img':img})
  
  
  return data
  
  
@app.route('/weixinshow')
def weixin_show():
  xstr = ""
  global xml_msg
  
  return {'data':xml_msg}  


  
def make_single_item(text, img):
  itemTpl = u"""
  <item>
      <Title><![CDATA[%s]]></Title>
      <Description><![CDATA[%s]]></Description>
      <PicUrl><![CDATA[%s]]></PicUrl>
      <Url><![CDATA[%s]]></Url>
  </item>"""
  picUrl = img
  item = itemTpl % (u"百思不得其姐",text, img, 'http://www.budejie.com/')
  return item
  
def response_news_msg(recvmsg, data ):
  msgStartTpl = """<xml>
  <ToUserName><![CDATA[%s]]></ToUserName>
  <FromUserName><![CDATA[%s]]></FromUserName>
  <CreateTime>%s</CreateTime>
  <MsgType><![CDATA[news]]></MsgType>
  <Content><![CDATA[]]></Content>
  <ArticleCount>%d</ArticleCount>
  <Articles>
  """
  
  msgEnd = """
  </Articles>
  <FuncFlag>1</FuncFlag>
  </xml>
  """
  
  msgStart = msgStartTpl %(recvmsg['FromUserName'], recvmsg['ToUserName'], recvmsg['CreateTime'], len(data) )
  msg = msgStart
  
  for d in data:
    msg += make_single_item( d['text'], d['img'] )
      
  msg += msgEnd
  return msg

  
def parse_xml( xmlStr ):
  root_xml = ET.fromstring( xmlStr )
  msg = {}
  for child in root_xml:
    msg[child.tag] = child.text
  
  return msg
