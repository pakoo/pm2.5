#/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo
from pymongo import MongoClinet
import tweepy

con = MongoClient('localhost',27017)
db = con.air.pm

shanghai = tweepy.api.get_user('CGShanghaiAir')
beijing = tweepy.api.get_user('BeijingAir')
chengdu = tweepy.api.get_user('CGChengduAir')
guangzhou = tweepy.api.get_user('Guangzhou_Air')

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
    data = tweet.text.split(';')[2]
    res = db.find_one({'location':place,'create_time':create_time}) 
    if not res:
        print ">>>>>>>>发现一条 %s %s 的新数据 PM2.5=%s "%(place,str(create_time),data)
        db.insert({
                   'location':place,
                   'create_time':create_time,
                   'data':data,
                  })
    else:
        print '>>>>>>>>>not found %s new data'%place
        
         
    

for place in air_location:
    tweet = air_location[place].timeline()[0]
    parserdata(tweet,place)

