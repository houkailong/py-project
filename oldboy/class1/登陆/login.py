#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'houkl'
import getpass
f_user = file('user.txt','r')
#定义所有用户信息字典
user_dict = {}
for i in f_user.readlines():
    #定义用户密码及登陆次数list，以用户名当做key，加入到user_dict中
    fmt_i = i.split()
    user = fmt_i[0]
    del fmt_i[0]
    user_dict[user] = fmt_i
f_user.close()

#while True:
user_name = raw_input('请输入用户名：')
if user_dict.has_key(user_name):
    time = int(user_dict[user_name][1])
    while time < 3:
        password = raw_input('请输入密码：')
        right_password = user_dict[user_name][0]
        if right_password == password:
            print '欢迎%s登陆成功' % user_name
            user_dict[user_name][1] = str(0)
            break
        else:
            time += 1
            #获取 user_dict 中user 对应 list[passwd],增加次数
            user_dict[user_name][1] = str(time)
    else:
        print '已3次登陆失败，账户 %s 已禁用！' %  user_name
else:
    print '用户名输入错误，请正确输入！'

# 重新格式化，写入文件
f_user = file('user.txt','w+')
for k,v in user_dict.items():
    result = k + ' ' + ' '.join(v) + '\n'
    f_user.write(result)
f_user.close()
