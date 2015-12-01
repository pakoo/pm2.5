#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymongo
from pymongo import MongoClient
import tweepy
import time
from weibo import APIClient
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup as bs4,Tag
import requests

con = MongoClient('localhost',27017)
db = con.air.pm
db2 = con.air.pic
APP_KEY = '114109966' # app key 
APP_SECRET = 'efcee5fbe1becdd6d88934eba3e23ba4' # app secret 
CALLBACK_URL = 'http://www.oucena.com/' # callback url  
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
client.set_access_token('2.00manU9D01NniH10e6012bafqOoA4D',1359960034)


consumer_key = 'ymHb0VVPRGX8e6afmPBvyQ'
consumer_secret = 'VLKvFg1hkrI8Hu2N3ENpYh4hfL8YABjQ5L8QvSA'
access_token='75552666-26gnjg4BbyS1VqVkdIMnIXiHtbud614kitTlkeM2e'
access_token_secret = 'epbWhd52MeK34eVHfbOGnM09q6Kf8oWlAibI6D5ZFQU'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

shanghai = api.get_user('CGShanghaiAir')
beijing =api.get_user('BeijingAir')
chengdu = api.get_user('CGChengduAir')
guangzhou = api.get_user('Guangzhou_Air')

air_location = {
                'shanghai':shanghai,
                'beijing':beijing,
                'chengdu':chengdu,
                'guangzhou':guangzhou,
               }

def parserdata(tweet,place):
    """
    解析美领馆pm2.5的数据
    """
    create_time = tweet.created_at
    print 'text:',tweet.text
    text = tweet.text.split(';')
    if len(text) >=3:
        publish_time,data = text[0],text[3]
        res = db.find_one({'location':place,'create_time':create_time}) 
        if not res:
            print ">>>>>>>>发现一条 %s %s 的在 %s 的新数据 PM2.5=%s "%(place,str(create_time),data,publish_time)
            db.insert({
                       'location':place,
                       'create_time':create_time,
                       'data':data,
                       'publish_time':publish_time,
                      })        
            #client.statuses.update.post(status=u'%s 的在 %s 的新数据 PM2.5=%s '%(place,publish_time,data))
        else:
            print '>>>>>>>>>not found %s new data'%place

def get_shanghai_air_pic():
    html = requests.get("http://www.semc.gov.cn/aqi/home/Index.aspx")
    soup = BeautifulSoup(html)
    pass
         
def get_city_live_pic(city_id):

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
            "page_length" : 30
            }
    }
    r = requests.post(url,data=json.dumps(para),cookies=cookie,headers=headers)
    res =  r.json()['picture_list']

for place in air_location:
    tweet = air_location[place].timeline()[0]
    parserdata(tweet,place)
    time.sleep(2)


