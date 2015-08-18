#coding=utf-8
__author__ = 'houkl'

import upstream_info
import shutil
import sys,re
import commands

def show_list():
    item = upstream_nginx.Choice_item()
    item_list = [i for i in item]
    while True:
        print '*' * 40
        for b in range(len(item_list)):
            #按upstream_info.txt中的序列顺序依次显示
            b += 1
            order = re.compile(r'^%s\.' % b)
            for li in item_list:
                if order.findall(li[0]):
                    print li[0],li[1]
        print '*' * 40 + '\n'
        global Item_num
        try:
            Item_num = int(raw_input(u'请输入项目序号：'))
            break
        except ValueError as e:
            print u'\033[1;31;40m请输入数字！\033[0m'
            continue
    pass

def show_ser_static(f1):
    ups_name = upstream_nginx.Find_upstm(Item_num)
    global ser_upstm
    ser_upstm = upstream_nginx.Ser_upstm(ups_name,f1)
    upstream_nginx.Show_ser()
    pass

def modify_ser(f1,f2):
    while True:
        show_ser_static(f1)
        ser_num = raw_input(u'请输入提供服务的服务器编号：')
        if ser_num:
            upstream_nginx.Modify_ser(ser_num)
            upstream_nginx.Modify_nginx(f1)
            #新建nginx.conf 配置文件
            upstream_nginx.Write_nginx(f2)
            #替换原文件
            shutil.move(f2,f1)
            break
        else:
            print u'输入错误，请重新输入！'
    pass

def nginx_reload():
    ckng_cmd = '/usr/local/nginx/sbin/nginx -t'
    reload_ng_cmd = '/usr/local/nginx/sbin/nginx -s reload'
    (status,output) = commands.getstatusoutput(ckng_cmd)
    if status == 0:
        (status1,output1) = commands.getstatusoutput(reload_ng_cmd)
        if status1 == 0:
            print u'nginx.conf 已加载成功'
        else:
            print output1
    else:
        print output
    pass

def nginx_switch(f1,f2):
    switch_dist = {
        'show':(u'显示当前主机状态','show_ser_static(f1)'),
        'modify':(u'修改主机状态','modify_ser(f1,f2)'),
        'back':(u'返回上层','back'),
        'exit':(u'退出','exit'),
        'reload':(u'重新加载nginx配置文件','nginx_reload()')
    }
    return switch_dist
    pass

if __name__ == '__main__':
    upstream_nginx = upstream_info.Upstream_Nginx()
    f1 = 'conf/nginx.conf1'
    f2 = 'conf/nginx.conf2'
    while True:
        show_list()
        while True:
            switch = nginx_switch(f1,f2)
            print '*' * 40
            print u'可选功能如下：'
            for f,v in switch.items():
                print f,v[0]
            print '*' * 40 + '\n'
            Input_fun = raw_input(u'请选择功能：')
            if Input_fun == 'back':
                break
            elif Input_fun == 'exit':
                sys.exit(0)
            elif switch.has_key(Input_fun):
                eval(switch[Input_fun][1])
