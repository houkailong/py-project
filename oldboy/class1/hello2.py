#!/usr/bin/env python
# -*- coding:utf-8 -*-

import getpass
name = raw_input("�������û�����")
pwd = getpass.getpass("���������룺")
print pwd
if name == 'alex' and pwd == '123':
    print '��½�ɹ���'
else:
    print "��½ʧ�ܣ�"