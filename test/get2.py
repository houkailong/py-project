__author__ = 'user'
import httplib
url='http://10.19.2.68/cgi-bin/python_test/test.py?ServiceCode=aaaa'
conn = httplib.HTTPConnection('10.19.2.68')
conn.request(method='GET',url=url)
response = conn.getresponse()
res = response.read()
print res
