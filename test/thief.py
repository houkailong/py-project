#coding=utf-8
__author__ = 'houkl'
import urllib
import urllib2
import cookielib
filename = '51cookie.txt'
#cookie = cookielib.CookieJar()
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

postdata = urllib.urlencode({
    'email':'kaolonghou',
    'passwd':'0624hou',
    'reback':'http%3A%2F%2Fwww.51cto.com%2F'
})
url = 'http://home.51cto.com/index.php?s=/Index/doLogin'

req = urllib2.Request(url=url,data=postdata)
result = opener.open(req)
cookie.save(ignore_discard=True,ignore_expires=True)
jump_url = ''
result =
print result.read()
result.close()


