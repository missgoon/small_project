#!/usr/bin/python
#coding=utf-8
import requests
import lxml.html
from lxml.html import parse
import pymongo
import time

while True:
  ISOTIMEFORMAT='%Y-%m-%d %X'
  print("~~~~~begin get data,now time is "+time.strftime(ISOTIMEFORMAT,time.localtime()))
  url="http://bwlc.net/bulletin/keno.html"
  c=pymongo.MongoClient("localhost",27017)
  db=c.lottery
  page=lxml.html.parse(url).getroot()
  lott_cont=page.find_class("lott_cont")[0].find_class("tb")[0]
  items=lott_cont.xpath("tr")[1:]
  for item in items:
    attrs=item.text_content().replace("\n"," ").replace("\t"," ").replace("\    u"," ").split(" ")
    cnt=attrs.count("")
    while cnt>0:
      attrs.remove("")
      cnt-=1
    if(db.happy8.find({"issue":attrs[0]}).count()==0): db.happy8.insert({"issue":attrs[0],"lottery_num":attrs[1],"firsbee_num":attrs[2],"lottery_datatime":attrs[3]+" "+attrs[4]})
    print("it's ok,issue:"+attrs[0])
  print("got data successfully!!!,now time is "+time.strftime(ISOTIMEFORMAT,time.localtime()))
  time.sleep(270)
