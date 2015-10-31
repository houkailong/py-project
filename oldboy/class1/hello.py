#!/usr/bin/env python
# -*- coding:utf-8 -*-

#捕获参数，并保存到集合

'''
    import getpass
    pwd = getpass.getpass(">>>")
    print pwd
'''

# if else

'''
name = raw_input("请输入用户名：")
if name == "alex":
    print "普通"
elif name == "tony":
    print "高级"
elif name == "eric":
    print "超神"
else:
    print "非法用户"
'''

import getpass
name = raw_input("请输入用户名：")
pwd = getpass.getpass("请输入密码：")
print pwd
if name == 'alex' and pwd == '123':
    print '登陆成功！'
else:
    print "登陆失败！"