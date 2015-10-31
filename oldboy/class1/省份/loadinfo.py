#/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'houkl'
import sys
f_info = file('info.txt','r')
'''
转化为 info_dict ={河北省:{邯郸市:"涉县,磁山,邯郸县",石家庄市:"平山县,井陉县,栾城县"}}
'''
info_dict = {}
for i in   f_info.readlines():
    info = i.split(':')
    #提取省信息
    province = info[0]
    #收集市、县对应字典
    city_dict = {}
    #提取市信息
    city = info[1]
    #提取县信息
    county = info[2]
    city_dict[city] = county
    #将市县和省对应，添加到info_dict，并判断info_dict 中是否已经存在省
    if province in info_dict:
        info_dict[province][city] = county
    else:
        info_dict[province] = city_dict
f_info.close()

while True:
    #省字典 eg:province_list = {1:HB,2:HN}
    province_dict = {}
    Pn  = 1
    for P in info_dict:
        province_dict[Pn] = P
        Pn += 1
    print '*' * 40
    print '省份列表：'
    for Pk,Pv in province_dict.items():
        print str(Pk) + '.' +  Pv
    print '''
功能列表：
exit.退出'''

    input_Pn = raw_input('请输入省份所对应的编号，以显现下属市区：')
    if input_Pn == 'exit':
        sys.exit(0)
    elif input_Pn == '':
        continue
    while True:
        '''
        所选省对应下属市 list
        P_name 所选省名字
        '''
        P_name = province_dict[int(input_Pn)]
        '''选出 字典 info_dict 省对应市字典
        定义 字典 Cn_dict 存  市对应编号'''
        Cn_dict = {}
        Cn = 1
        for c in  info_dict[P_name]:
            Cn_dict[Cn] = c
            Cn += 1
        print '*' * 40
        print '%s下属市列表：' % P_name
        for Ck,Cv in Cn_dict.items():
            print '''   %s''' % str(Ck) + '.' + Cv
        print '''
功能选项：
back.返回上级菜单
exit.退出'''
        input_Cn = raw_input('请输入所选市或功能对应编号：')
        if input_Cn == 'back':
            break
        elif input_Cn == 'exit':
            sys.exit(0)
        elif input_Cn == '':
            continue
        while True:
            '''
            列出所选 市 对应的下属县乡 list
            City_name 所选市名
            '''
            City_name = Cn_dict[int(input_Cn)]
            print '*' * 40
            print '%s 下属县乡列表：' % City_name
            for x in info_dict[P_name][City_name].split(','):
                print '''       %s'''% x
            print '''终极功能项：
back.返回上级菜单
exit.退出'''
            Xn = raw_input('请选择功能：')
            if Xn == 'back':
                break
            elif Xn == 'exit':
                sys.exit(0)
            else:
                continue
