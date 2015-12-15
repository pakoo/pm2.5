#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymongo
from pymongo import MongoClient
import requests
import json
import time


con = MongoClient('localhost',27017)

db2 = con.air.pic
db = con.air.pm

air_location = {
                'shanghai':340,
                'beijing':33,
                'chengdu':53,
                'guangzhou':126,
               }

         
def get_city_live_pic(city_id,city_name):

    url = "http://ugc.moji001.com/sns/json/liveview/timeline/city"
    
    headers = {
    'Host':'ugc.moji001.com',
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept_Language':'zh-Hans-CN, en-us',
    'Content-Type':'application/json; charset=utf-8',
    'Referer':'http://www.loreal-boutique.com/',
    'User-Agent':'%E5%A2%A8%E8%BF%B9%E5%A4%A9%E6%B0%94/5005070137 CFNetwork/758.1.6 Darwin/15.0.    0'
    }
    
        
    para ={
            "common" : {
            "unix" : "1448941933426.814",
            "uid" : 662936431,
            "app_version" : "50050701",
            "mcc" : "460",
            "width" : 640,
            "net" : "wifi",
            "mnc" : "01",
            "identifier" : "0C9346AC-B971-4F5B-8CC8-DCB49938F84E",
            "platform" : "iPhone",
            "token" : "<4cd00fba 1dcd12e3 41061fa6 4aaeff32 961a90c5 1ed9d1b2 cd61ce9b e054045b>    ",
            "language" : "CN",
            "height" : 1136,
            "os_version" : "9.1",
            "device" : "iPhone",
            "pid" : "9000"
            },
            "params" : {
            "city_id" :str(city_id),
            "page_past" : 0,
            "page_length" : 15
            }
    }
    r = requests.post(url,data=json.dumps(para),headers=headers)
    res =  r.json()['picture_list']
    db2.insert({
                'city_id':city_id,
                'create_time':time.time(),
                'pic_list':res,
                'city_name':city_name,
        })
    pm = db.find_one({'location':city_name},sort=[('create_time',-1)],limit=1)
    db.update({'_id':pm['_id']},{'$set':{'cover':'http://ugc.moji001.com/images/sthumb/'+res[0]['path']}})

for k,v in air_location.items():
    get_city_live_pic(v,k)
