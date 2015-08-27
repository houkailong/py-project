__author__ = 'user'
import urllib2,urllib
import httplib
test_data = {'b':'aaaa','ServiceCode':'bbbb'}
test_data_urlencode = urllib.urlencode(test_data)
requrl = 'http://10.19.2.68/cgi-bin/python_test/test.py'
req = urllib2.Request(url=requrl,data=test_data_urlencode)
print req
res_data = urllib2.urlopen(req)
res = res_data.read()
print res
