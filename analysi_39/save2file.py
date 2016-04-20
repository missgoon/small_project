#-*- coding: utf-8 -*-
from pymongo import MongoClient
import json

client=MongoClient("139.129.45.40",27017)
db_news=client.data_for_39.news_sec
with open("data","ab") as file:
  for item in db_news.find():
    item.pop("_id")
    file.write("%s:%s\n"%("path",item["path"].encode("utf-8")))
    file.write("%s:%s\n"%("title",item["title"].encode("utf-8")))
    file.write("%s:%s\n"%("content",item["content"].encode("utf-8")))
    file.write("\n\n\n")
  