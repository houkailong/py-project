#!/usr/bin/env python
#coding=utf8
import urllib
import urllib2
import httplib
requrl = 'http://10.19.2.68/cgi-bin/python_test/test.py?ServiceCode=aaaa'
req = urllib2.Request(requrl)
res_data = urllib2.urlopen(req)
res = res_data.read()
print res