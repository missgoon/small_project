import lxml.html
import requests

url="http://www.duia.com/course/lecturePlay/870/28003"
title="1"
html=lxml.html.fromstring(requests.get(url).content)
i,url_list,real_url_list=1,{},{}
for div in html.xpath("//div[@class='v-tab-one']")[0].xpath("./div[@class='part']"):
  chapter=div.xpath("./div[@class='t-title']/@title")[0].strip()
  j=1
  for a in div.xpath("./a"):
    url_list[str(i)+"."+str(j)]="http://www.duia.com"+a.xpath("./@href")[0].strip()
    j+=1
  i+=1

for key,item in url_list.items():
  html=lxml.html.fromstring(requests.get(item).content)
  vu=html.xpath("//input[@id='lsVideoId']/@value")[0].strip()
  real_url_list[title+"."+key]="http://yuntv.letv.com/bcloud.swf?uu=c2ygy4wf5p&vu="+vu+"&pu=67d53686dc"


with open(title,"w") as file:
  for key,item in real_url_list.items():
    file.write(item+"\n")

  for key,item in real_url_list.items():
    file.write(key+"\t"+item+"\n")