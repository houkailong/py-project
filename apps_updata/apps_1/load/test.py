# encoding=UTF-8
__author__ = 'xuebaoku'

import os

from apps_1 import API_2


def test():
    BASE_DIR = os.path.dirname(__file__)
    if not BASE_DIR:
            BASE_DIR = './'
    if BASE_DIR != './':
            BASE_DIR = BASE_DIR + '/'
    logs= API_2.logs_install(BASE_DIR+'logs/test_all')
    HttpNet = API_2.HttpNetRobot('http://127.0.0.1:8000/',logs)
    data = {
    "caption": "haodai1212311k_unio23n_oms-ba2nk_union2_oms_sho2rttime-huml-2047-2200-201508131424.war",
    "Pull_user": "syspub",
    "Pull_port": "22",
    "Pull_server": "192.168.1.1",
    "Pull_path": "/home/git/haodaibao.com/bank_union_oms/",
    "message": "颍东农商银行上线后端修改，请在前端上线前执行以下sql",
    "code": 'unknown'
    }
    Package = HttpNet.send('api/Package/',post_data=data)
    return Package['url'].split('/')[-2]

if __name__ == '__main__':
    print test()