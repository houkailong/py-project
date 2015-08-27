# encoding=UTF-8
__author__ = 'xuebaoku'
import zmq
import time
mode = {"onlinegray":"上线灰度",
"Inquire":"查询"}



c = zmq.Context()
s = c.socket(zmq.REQ)
s.connect('tcp://127.0.0.1:11111')
'''
for i in mode:
    print i
    s.send_json(eval(i))
    msg = s.recv_json()
    print msg
    print msg['data']['message']
'''
for i in xrange(0,1):
    onlinegray = {'mode':'onlinegray',
         'Package':{
            "caption": "syspub%s.war"%time.time(),
            "Pull_user": "syspub",
            "Pull_port": "22",
            "Pull_server": "192.168.1.1",
            "Pull_path": "/home/git/haodaibao.com/bank_union_oms/",
         },
         'Project':{
             'Duct':'tomcat-test_0001',
             'name':'%s灰度测试上线'%time.time(),
             "message": "灰度测试上线%s"%time.time(),
         }
    }
    s.send_json(onlinegray)
    msg = s.recv_json()
    print msg['data']['message']
    if msg['mode']:
        try:
            for i,v in msg['data']['msg']['Project'].items():
                print i,":",v
        except:
            pass
    Inquire = {
    'mode':'Inquire',
    'Project':{
        'uuid':msg['data']['msg']['Project']['uuid'],#必须提供
        }
}
    print
    time.sleep(5)
    s.send_json(Inquire)
    msg = s.recv_json()
    print  msg['data']['message']

#返回结果