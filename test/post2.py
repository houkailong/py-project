__author__ = 'user'
import urllib
import httplib
requrl = 'http://10.19.2.68/cgi-bin/python_test/test.py'
test_data = {'ServiceCode':'aaaa','b':'bbbb'}
test_data_urlencode = urllib.urlencode(test_data)
Headerdata = {'Host':'10.19.2.68'}
conn = httplib.HTTPConnection('10.19.2.68')
conn.request(method='POST',url=requrl,body=test_data_urlencode,headers=Headerdata)
response = conn.getresponse()
res = response.read()
print res
data=response.getheader('data')
print data
resheader = ''
resheader = response.getheaders()
print resheader
