#coding=utf-8
import urllib
import urllib2
import cookielib
import zlib

filename = 'cookie.txt'
#cookie = cookielib.CookieJar()
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

postdata = urllib.urlencode({
    'os_username':'houkl',
    'os_password':'0624houkailong',
    'login':'登陆',
    'os_destination':'/index.action'
})
req = urllib2.Request(
    url = 'http://wiki.haodaibao.com/dologin.action',
    data = postdata
)
result = opener.open(req)
cookie.save(ignore_discard=True,ignore_expires=True)
gradeUrl = 'http://wiki.haodaibao.com/pages/viewpage.action?pageId=2523729'
result = opener.open(gradeUrl)
with file('zichan.txt','wb') as code:
    code.write(result.read())
    result.close()

