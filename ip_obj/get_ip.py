#coding=utf-8
__author__ = 'houkailong'
import re
import sys
def __GetIP():
    re_ip = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    with file('message') as f:
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
    ALL_sub_IP = Ip_Subway(ip_sub)
    re_sub = re.compile(r'%s\.' % ip_sub)
    for i in __GetIP():
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
    if ip_sub:
        ip_sub = ip_sub[0].split('.')[0:3]
        ip_sub = '.'.join(ip_sub)
        __FreeIp(ip_sub)
    else:
        print u'执行时需指定ip段（样例：python get_ip.py 10.19.0）；'
