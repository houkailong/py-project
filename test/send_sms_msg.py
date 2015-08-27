#!/usr/bin/env python
#coding=utf8



#code：c077a325b151c0369d8d497a7b06b993
#Content-Type : application/text; charset=utf-8
#其他参数
#phone:手机号
#content:短信内容
#appName:短信通道名称可以为(qb,hdb,pay,yw)


import urllib
import urllib2
import hashlib
import json


phone = '13301010642'
appName = 'yw'
secure_key = 'd8V>0_4K$c45khZ{FcqS'
sms_content = '验证码:123456'
#生成加密串
md = hashlib.md5()
md.update(appName + phone + secure_key)
md5_value =  md.hexdigest()
#http请求头封装
headerdata = {'code':md5_value, 'Content-Type':'application/text; charset=utf-8'}
post_data = {'phone':phone, 'content':sms_content, 'appName':appName}
#http post请求数据封装
post_data_urlencode = urllib.urlencode(post_data)
requrl = 'http://192.168.1.238:9878/api/sms/send'
req = urllib2.Request(url = requrl, data = post_data_urlencode, headers=headerdata)
#执行http请求
try:
    res_data = urllib2.urlopen(req)
    #获取http结果
    res = res_data.read()
    res_data = json.loads(res)
    status =  res_data['status']
    message = res_data['message']
    if status == '00000000' :
        print 'send sms msg success phone: %s, content: %s' % (phone, sms_content)
    else :
        print message
        print 'send sms msg error phone: %s, content: %s' % (phone, sms_content)
except Exception as e:
    print e
    print 'send sms msg error phone: %s, content: %s' % (phone, sms_content)





