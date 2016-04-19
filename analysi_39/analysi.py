#-*- coding: utf-8 -*-
import lxml.html
import os
import requests 
import re
from pymongo import MongoClient
import redis
from lxml.html.clean import Cleaner


def get_proxy():
  flag=True
  while flag:
    proxy_str=r1.lpop("ip_proxies")
    try:
      r1.incr("ip_proxies.times")
      if int(r1.get("ip_proxies.times"))>3: raise
      r1.lpush("ip_proxies",proxy_str)
      flag=False
    except Exception,e:
      r1.set("ip_proxies.times",0)
      r1.rpush("ip_proxies",proxy_str)
  print("use:%s"%proxy_str)
  return {'http':"http://"+proxy_str}

def handle_item(url):
  url="http://news.39.net/"+url.split("/root/39_data/news.39.net/")[1]
  flag,title,text=False,"",""
  try:
    request=requests.get(url,proxies=get_proxy(),timeout=5)
    if request.status_code!=200: raise
    html=lxml.html.fromstring(request.content.decode("gbk"))
    if re.search("utf",html.xpath("//meta/@charset")[0]): 
      html=lxml.html.fromstring(r.content.decode("utf-8"))
    try:
      div=html.xpath("//div[@class='art_left']")[0]
      title=div.xpath("./div[@class='art_box']/h1/text()")[0]
    except:
      title=""
    print("title:%s"%title)
    div1=html.xpath("//div[@id='contentText']")[0]
    cleaner = Cleaner(scripts = True)
    for p in div1.xpath("./p"):
      p=cleaner.clean_html(p)
      try:
        text+=p.xpath("text()")[0].strip()+"\n"
      except: pass
    print("text:%s"%text)
    flag=True
  except Exception,e:
    print(e)
  return [flag,title,text,url]

def handle_rst(item_rst):
  print("%s\t%s"%(r.get("s_cnt"),r.get("f_cnt")))
  print(item_rst)
  if (not item_rst[0]) or (len(item_rst[1])<=0) or (len(item_rst[2])<=0): 
    r.incr("f_cnt") 
    return False
  db_news.insert_one({"title":item_rst[1],"content":item_rst[2],"path":item_rst[3]})
  print(item_rst[3].split("http://news.39.net/"))
  print("begin delete file:%s"%("/root/39_data/news.39.net/"+item_rst[3].split("http://news.39.net/")[1]))
  os.remove("/root/39_data/news.39.net/"+item_rst[3].split("http://news.39.net/")[1])
  r.incr("s_cnt")
  return True

def get_item(path):
  try:
    for item in os.listdir(path):
      if re.search(".html",item):
        if re.search("index",item):
          print("begin delete file:%s"%(path+item))
          os.remove(path+item)
        item_rst=handle_item(path+item)
        handle_rst(item_rst)
      elif len(os.listdir(path+item+"/"))==0:
        os.rmdir(path+item+"/")  #删除空目录
      else:
        print("begin handle dir:%s\n"%(path+item+"/"))
        get_item(path+item+"/")
  except Exception,e: 
    print(e)

path="/root/39_data/news.39.net/"
r = redis.Redis(host="139.129.45.40",port=6379,db=1)
r.set("f_cnt",0)
r.set("s_cnt",0)
r1=redis.Redis(host="139.129.45.40",port=6379,db=0)
client=MongoClient("139.129.45.40",27017)
db_news=client.data_for_39.news
db_news.remove()

get_item(path)
# with open("log","ab") as log:
#   for file_p in os.listdir(path):
#     try:
#       r=requests.get(url+file_p)
#       html=lxml.html.fromstring(r.content.decode("gbk"))
#       if re.search("utf",html.xpath("//meta/@charset")[0]): 
#         html=lxml.html.fromstring(r.content.decode("utf-8"))
#       div=html.xpath("//div[@class='art_left']")[0]
#       title=div.xpath("./div[@class='art_box']/h1/text()")[0]
#       print(title+"\n")
#       log.write(title.encode("utf-8"))
#       div1=html.xpath("//div[@id='contentText']")[0]
#       for p in div1.xpath("./p"):
#         try:
#           print(p.xpath("text()")[0])
#           log.write(p.xpath("text()")[0].encode("utf-8"))
#         except: pass
#       s_cnt+=1
#     except Exception,e: 
#       print(e)
#       f_cnt+=1
#       shutil.move(path+file_p,"/root/analysi_39/f_files")
#     print("\n\n\n")
#     log.write("\n\n\n")
#   print(s_cnt,f_cnt)