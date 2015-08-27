# encoding=UTF-8
__author__ = 'xuebaoku'
import json
import requests
import conf
from API.logs import logs_install


class Http_data():
    def __init__(self,data):
        self.ok=data
class HttpNetRobot:
    def __init__(self, baseurl,logs):
        self.logs = logs
        self.baseurl = baseurl
        self.headerdata = {'Content-Type':'application/text; charset=utf-8'}
    def OPTIONS(self,requrl,logs='debug',mode=True):
        if mode:
            requrl = self.baseurl + requrl
        getattr(self.logs,logs)("%s%s%s%s%s%s"%('='*25,'OPTIONS','='*2,requrl,'='*2,'='*25))
        try:
            res_data = requests.options(requrl,timeout=conf.timeout)
            try:
                getattr(self.logs,logs)("urllib2>>>>status_code:%s data:%s"%(res_data.status_code,json.dumps(res_data.json())))
            except:
                getattr(self.logs,logs)("urllib2>>>>status_code:%s data:%s"%(res_data.status_code,json.dumps(res_data.text)))
            getattr(self.logs,logs)("%s%s%s%s%s%s"%('='*25,'OPTIONS','='*2,'success','='*2,'='*25))
            return res_data
        except Exception as e:
            getattr(self.logs,logs)("%s%s%s%s%s%s"%('='*25,'OPTIONS','='*2,'failure','='*2,'='*25))
            return Http_data(False)
    def POST(self,requrl,post_data,logs='debug',mode=True):
        if mode:
            requrl = self.baseurl + requrl
        getattr(self.logs,logs)("%s%s%s%s%s%s"%('='*25,'POST','='*2,requrl,'='*2,'='*25))
        try:
            res_data = requests.post(requrl,post_data,timeout=conf.timeout)
            try:
                getattr(self.logs,logs)("urllib2>>>>status_code:%s data:%s"%(res_data.status_code,json.dumps(res_data.json())))
            except:
                getattr(self.logs,logs)("urllib2>>>>status_code:%s data:%s"%(res_data.status_code,json.dumps(res_data.text)))
            getattr(self.logs,logs)("%s%s%s%s%s%s"%('='*25,'POST','='*2,'success','='*2,'='*25))
            return res_data
        except Exception as e:
            print e
            getattr(self.logs,logs)("%s%s%s%s%s%s"%('='*25,'POST','='*2,'failure','='*2,'='*25))
            return Http_data(False)
    def GET(self,requrl,logs='debug',mode=True):
        if mode:
            requrl = self.baseurl + requrl
        getattr(self.logs,logs)("%s%s%s%s%s%s"%('='*25,'GET','='*2,requrl,'='*2,'='*25))
        try:
            res_data = requests.get(requrl,timeout=conf.timeout)
            try:
                getattr(self.logs,logs)("urllib2>>>>status_code:%s data:%s"%(res_data.status_code,json.dumps(res_data.json())))
            except:
                getattr(self.logs,logs)("urllib2>>>>status_code:%s data:%s"%(res_data.status_code,json.dumps(res_data.text)))
            getattr(self.logs,logs)("%s%s%s%s%s%s"%('='*25,'GET','='*2,'success','='*2,'='*25))
            return res_data
        except Exception as e:
            print e.message
            getattr(self.logs,logs)("%s%s%s%s%s%s"%('='*25,'GET','='*2,'failure','='*2,'='*25))
            return Http_data(False)
    def DELETE(self,requrl,logs='debug',mode=True):
        if mode:
            requrl = self.baseurl + requrl
        getattr(self.logs,logs)("%s%s%s%s%s%s"%('='*25,'DELETE','='*2,requrl,'='*2,'='*25))
        try:
            res_data = requests.delete(requrl,timeout=conf.timeout)
            try:
                getattr(self.logs,logs)("urllib2>>>>status_code:%s data:%s"%(res_data.status_code,json.dumps(res_data.json())))
            except:
                getattr(self.logs,logs)("urllib2>>>>status_code:%s data:%s"%(res_data.status_code,json.dumps(res_data.text)))
            getattr(self.logs,logs)("%s%s%s%s%s%s"%('='*25,'DELETE','='*2,'success','='*2,'='*25))
            return res_data
        except Exception as e:
            getattr(self.logs,logs)("%s%s%s%s%s%s"%('='*25,'DELETE','='*2,'failure','='*2,'='*25))
            return Http_data(False)
    def PUT(self,requrl,post_data,logs='debug',mode=True):
        if mode:
            requrl = self.baseurl + requrl
        getattr(self.logs,logs)("%s%s%s%s%s%s"%('='*25,'PUT','='*2,requrl,'='*2,'='*25))
        try:
            res_data = requests.put(requrl,post_data,timeout=conf.timeout)
            try:
                getattr(self.logs,logs)("urllib2>>>>status_code:%s data:%s"%(res_data.status_code,json.dumps(res_data.json())))
            except:
                getattr(self.logs,logs)("urllib2>>>>status_code:%s data:%s"%(res_data.status_code,json.dumps(res_data.text)))
            getattr(self.logs,logs)("%s%s%s%s%s%s"%('='*25,'PUT','='*2,'success','='*2,'='*25))
            return res_data
        except Exception as e:
            getattr(self.logs,logs)("%s%s%s%s%s%s"%('='*25,'PUT','='*2,'failure','='*2,'='*25))
            return Http_data(False)

def test(logs='debug'):
    import time
    http = HttpNetRobot('http://127.0.0.1:8000/')
    data = http.OPTIONS('api/Package/',logs=logs)
    if not data.ok:
        return
    print data.json()
    post_data = {
    "caption": "syspub%s"%time.time(),
    "Pull_user": "syspub",
    "Pull_port": "22",
    "Pull_server": "192.168.1.23",
    "Pull_path": "/home/git/haodaibao.com/bank_union_oms/",
    "code": 'failed'
}
    data = http.POST('api/Package/',post_data,logs=logs)
    if not data.ok:
        return

    data = data.json()
    print data
    data['code']='success'
    data_http = http.PUT(data['url'],post_data=data,logs=logs,mode=False)
    data_http = http.GET(data['url'],logs=logs,mode=False)
    if not data_http.ok:
        return
    print data_http.json()
    data_http = http.DELETE(data['url'],logs='info',mode=False)
    if not data_http.ok:
        return



if __name__ == '__main__':
    test()