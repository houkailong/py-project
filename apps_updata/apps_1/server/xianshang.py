# encoding=UTF-8
__author__ = 'xuebaoku'
import zmq
mode = {"onlinegray":"上线灰度",
"Update_package":"更新包",
"Forcibly_Project":'强制重启项目',
"restart_Project":"重启项目",
"start_Project":"启动项目",
"stop_Project":"停止项目",
"Inquire":"查询"}
onlinegray = {'mode':'onlinegray',
         'Package':{
            'uuid':None,#可以没有,但是当有的时候则不执行下面
            "caption": "ha1123111123112312312424.war",
            "Pull_user": "syspub",
            "Pull_port": "22",
            "Pull_server": "192.168.1.1",
            "Pull_path": "/home/git/haodaibao.com/bank_union_oms/",
            "message": "颍东农商银行上线后端修改，请在前端上线前执行以下sql",
         },
         'Project':{
             'uuid':None,#可以没有,但是当有的时候则更新下面
             'Duct':'tomcat-test_0001',
             'name':'123',
             "message": "颍东农商银行上线后端修改，请在前端上线前执行以下sql",
         }
    }
Update_package = {
    'mode':'Update_package',
    'Package':{
        "caption": "ha1l-2047-11341150813124324.war",
        "Pull_user": "syspub",
        "Pull_port": "22",
        "Pull_server": "192.168.1.1",
        "Pull_path": "/home/git/haodaibao.com/bank_union_oms/",
        "message": "颍东农商银行上线后端修改，请在前端上线前执行以下sql",
        },
    'Project':{
        'uuid':'a652b8459d0e4c2ebe55417ffb17fb04',#必须提供
        }
    }
Forcibly_Project = {
    'mode':'restart_Project',
    'Project':{
        'uuid':'a652b8459d0e4c2ebe55417ffb17fb04',#必须提供
        }
}
restart_Project = {
    'mode':'restart_Project',
    'Project':{
        'uuid':'a652b8459d0e4c2ebe55417ffb17fb04',#必须提供
        }
}
start_Project = {
    'mode':'start_Project',
    'Project':{
        'uuid':'a652b8459d0e4c2ebe55417ffb17fb04',#必须提供
        }
}
stop_Project = {
    'mode':'stop_Project',
    'Project':{
        'uuid':'a652b8459d0e4c2ebe55417ffb17fb04',#必须提供
        }
}
Inquire = {
    'mode':'Inquire',
    'Package':{
        'uuid':'aa925d2096b64df0b0e945c1d76c9a17',#必须提供
        },
    'Project':{
        'uuid':'a652b8459d0e4c2ebe55417ffb17fb04',#必须提供
        }
}

c = zmq.Context()
s = c.socket(zmq.REQ)
#s.connect('tcp://10.19.2.230:3333')
s.connect('tcp://127.0.0.1:11111')
#print data['data'].keys()
#data = {'data':{'password':'123456'},'mode':'exit'}
'''
for i in mode:
    print i
    s.send_json(eval(i))
    msg = s.recv_json()
    print msg
    print msg['data']['message']
'''
s.send_json(restart_Project)
msg = s.recv_json()
print msg['data']['message']
if msg['mode']:
    try:
        for i,v in msg['data']['msg']['Project'].items():
            print i,":",v
        for i,v in msg['data']['msg']['Package'].items():
            print i,":",v
    except:
        pass

#返回结果
"""
Connected to pydev debugger (build 139.781)
stop_Project
{'data': {'message': u'\u53c2\u6570\u6267\u884c\u6210\u529f'}, 'mode': True}
参数执行成功
Inquire
{'data': {'message': u'\u53c2\u6570\u6267\u884c\u6210\u529f'}, 'mode': True}
参数执行成功,返回查询结果
start_Project
{'data': {'message': u'\u53c2\u6570\u6267\u884c\u6210\u529f'}, 'mode': True}
参数执行成功
Forcibly_Project
{'data': {'message': u'\u53c2\u6570\u6267\u884c\u6210\u529f'}, 'mode': True}
参数执行成功
onlinegray
{'data': {'message': u'\u66f4\u65b0\u4fe1\u606f\u6210\u529f,\u5e76\u53d1\u5e03\u5f3a\u5236\u91cd\u542f\u547d\u4ee4', 'uuid': 123123}, 'mode': True}
更新信息成功,并发布强制重启命令
restart_Project
{'data': {'message': u'\u53c2\u6570\u6267\u884c\u6210\u529f'}, 'mode': True}
参数执行成功
Update_package
{'data': {'message': u'\u66f4\u65b0\u4fe1\u606f\u6210\u529f,\u5e76\u53d1\u5e03\u5f3a\u5236\u91cd\u542f\u547d\u4ee4', 'uuid': 123123}, 'mode': True}
更新信息成功,并发布强制重启命令"""