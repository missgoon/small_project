# -*- coding: utf-8 -*-
import requests
import lxml.html
import redis
import multiprocessing  #多进程module
import thread
import time

# urls=[
#   "http://www.youdaili.net/Daili/http/4323.html",
#   "http://www.youdaili.net/Daili/http/4323_2.html",
#   "http://www.youdaili.net/Daili/http/4323_3.html",
# ]
urls=["4323","4323_2","4323_3","4319","4319_2","4319_3","4315","4315","4315","4313","4313","4309","4309","4309","4304","4304","4304","4300","4300","4300","4300","4295","4295","4328","4328_2","4328_3","4328_4","4332","4332_2","4332_3","4332_4","4337","4337_2","4337_3","4337_4","4342","4342_2","4342_3"]
test_url="http://news.39.net/"#"http://chaoyang.anjuke.com/"

r = redis.Redis(host="139.129.45.40",port=6379,db=0)
r.flushall()
def handle_item(item):
  try:
    if item.strip().count("@")!=0: item=item.strip().split("@")[0]
    elif item.strip().count("#")!=0: item=item.strip().split("#")[0]
    if not len(item)>0: raise
    proxies = {'http':"http://"+item}
    response=requests.get(test_url,proxies=proxies,timeout=1)
    print(proxies,response)
    if response.status_code!=200: raise
    r.lpush("ip_proxies",item)
    print("%s\t%d"%(item,r.llen("ip_proxies")))
  except Exception,e:
    print(e)

def run(url):
  html=lxml.html.fromstring(requests.get(url).content)
  if len(html.xpath("//span[@style='font-size:14px;']"))>=1:
    for item in html.xpath("//span[@style='font-size:14px;']/text()"):
      handle_item(item)
  elif len(html.xpath("//div[@class='cont_font']/p/text()"))>0:
    for item in html.xpath("//div[@class='cont_font']/p/text()"):
      handle_item(item)
  r.set("process_cnt",int(r.get("process_cnt"))-1)

r.set("process_cnt",0)
for url in urls:
  while True:
    if r.get("process_cnt")>=10: time.sleep(5)
    url="http://www.youdaili.net/Daili/http/"+url+".html"
    print("ok %s"%url)
    # thread.start_new_thread(run,(url,))
    p = multiprocessing.Process(target = run, args = (url,))
    p.start()
    r.incr("process_cnt")
    break