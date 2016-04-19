#-*- coding: utf-8 -*-
import lxml.html
import os
import shutil
import requests
import re

path="/root/analysi_39/140324/"
url="http://news.39.net/26MIEE/140324/"
s_cnt,f_cnt=0,0
with open("log","ab") as log:
  for file_p in os.listdir(path):
    try:
      r=requests.get(url+file_p)
      html=lxml.html.fromstring(r.content.decode("gbk"))
      if re.search("utf",html.xpath("//meta/@charset")[0]): 
        html=lxml.html.fromstring(r.content.decode("utf-8"))
      div=html.xpath("//div[@class='art_left']")[0]
      title=div.xpath("./div[@class='art_box']/h1/text()")[0]
      print(title+"\n")
      log.write(title.encode("utf-8"))
      div1=html.xpath("//div[@id='contentText']")[0]
      for p in div1.xpath("./p"):
        try:
          print(p.xpath("text()")[0])
          log.write(p.xpath("text()")[0].encode("utf-8"))
        except: pass
      s_cnt+=1
    except Exception,e: 
      print(e)
      f_cnt+=1
      shutil.move(path+file_p,"/root/analysi_39/f_files")
    print("\n\n\n")
    log.write("\n\n\n")
print(s_cnt,f_cnt)