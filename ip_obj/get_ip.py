#coding=utf-8
__author__ = 'houkailong'
'''
添加自动下载硬件资产表信息，自动分析里面包含ip的情况
'''
import re
import sys
import urllib
import urllib2
import cookielib

def __Downzichan(downfile):
    '''
    :param downfile: 资产信息下载后保存的文件
    :return:
    '''
    cookiefile = 'cookie.txt'
    cookie = cookielib.MozillaCookieJar(cookiefile)
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
    with file(downfile,'wb') as code:
	code.write(result.read())
	result.close()
    

def __GetIP(zichanfile):
    re_ip = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    with file(zichanfile) as f:
        for line in f.readlines():
            for ip in  re_ip.findall(line):
                yield ip

def Ip_Subway(ip_sub):
    '''
    最终返回输入ip段可用ip
    :param ip_sub: ip段
    :return: 返回所输入ip段的全部ip list
    '''
    ALL_sub_IP = []
    for i in range(1,255):
        ip = '%s.' % ip_sub + str(i)
        ALL_sub_IP.append(ip)
    return ALL_sub_IP
    pass

def Sel_Ip(ip_sub):
    '''
    :param ip_sub: ip 段
    :return: 根据ip段 返回查询出的ip list
    '''
    pass

def __FreeIp(ip_sub):
    '''
    :param ip_sub: ip 段
    :return:
    '''
    __Downzichan(zichanfile)
    ALL_sub_IP = Ip_Subway(ip_sub)
    re_sub = re.compile(r'%s\.' % ip_sub)
    for i in __GetIP(zichanfile):
        if re_sub.findall(i):
            try:
                ALL_sub_IP.pop(ALL_sub_IP.index(i))
            except ValueError as e:
                pass
    print ALL_sub_IP
    '''
    for F_ip in ALL_sub_IP:
        print F_ip
    '''
    pass

if __name__ == '__main__':
    ip_sub = sys.argv[1:]
    zichanfile = 'zichan.txt'
    if ip_sub:
        ip_sub = ip_sub[0].split('.')[0:3]
        ip_sub = '.'.join(ip_sub)
        __FreeIp(ip_sub)
    else:
        print u'执行时需指定ip段（样例：python get_ip.py 10.19.0）'
