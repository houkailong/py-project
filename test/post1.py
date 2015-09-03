__author__ = 'user'
import urllib2,urllib
import httplib
test_data = {'os_username':'houkl','os_password':'0624houkailong'}
test_data_urlencode = urllib.urlencode(test_data)
requrl = 'http://wiki.haodaibao.com/login.action?logout=true'
req = urllib2.Request(url=requrl,data=test_data_urlencode)
print req
res_data = urllib2.urlopen(req)
res = res_data.read()
print res
