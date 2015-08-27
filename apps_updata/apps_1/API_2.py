# encoding=UTF-8
__author__ = 'xuebaoku'
import json
import urllib2
import urllib

import requests

import conf


def logs_install(file_name):
    """
    logs初始化进程.
    :param file_name: 需要传入file文件保存的绝对位置
    :return:logs模块
    """
    import logging
    #################################################################################################
    #定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s  %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=file_name,
                filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    return logging
#执行http请求



class HttpNetRobot:
    def __init__(self, baseurl,logs):
        self.logs = logs
        self.baseurl = baseurl
        self.headerdata = {'Content-Type':'application/text; charset=utf-8'}
    def getData(self,**data):
        """
        获取 cookie
        :param data:
        :return:
        """
        self.logs.info('origin data:%s'%data)
        #self.opener.open(self.baseurl)
        try:
            data['csrfmiddlewaretoken'] = [x.value for x in self.cj if "csrftoken"==x.name][0]
        except:
            pass
        return data
    def get(self,requrl):
        self.logs.debug("%s%s%s"%('='*25,'get','='*25))
        requrl = self.baseurl + requrl
        self.logs.debug("urllib2>>>>requrl:%s "%(requrl))
        try:
            res_data = urllib2.urlopen(requrl,timeout=conf.timeout)
            #获取http结果
            res = res_data.read()
            res_data = json.loads(res)
            self.logs.debug("urllib2>>>>data:%s"%json.dumps(res_data))
            self.logs.debug("%s%s%s"%('^'*25,'send success','^'*25))
            return res_data
        except Exception as e:
            self.logs.error("%s%s%s"%('!'*25,'send failure','!'*25))
            return '%s'%e
    def send(self,requrl,post_data):
        self.logs.debug("%s%s%s"%('='*25,'post','='*25))
        requrl = self.baseurl + requrl
        post_data_urlencode = urllib.urlencode(post_data)
        #req = urllib2.Request(url = requrl, data = post_data_urlencode, headers=self.headerdata)
        self.logs.info("urllib2>>>>requrl:%s data:%s headers:%s"%(requrl,post_data_urlencode,self.headerdata))
        try:
            res_data = urllib2.urlopen(requrl,post_data_urlencode,timeout=conf.timeout)
            #获取http结果
            res = res_data.read()
            res_data = json.loads(res)
            self.logs.debug("urllib2>>>>data:%s"%json.dumps(res_data))
            self.logs.debug("%s%s%s"%('^'*25,'send success','^'*25))
            return (True,res_data)
        except Exception as e:
            self.logs.error("%s%s%s"%('!'*25,'send failure','!'*25))
            return (False,'%s'%e)
    def OPTIONS(self,requrl):
        self.logs.debug("%s%s%s"%('='*25,'OPTIONS','='*25))
        requrl = self.baseurl + requrl
        self.logs.debug("urllib2>>>>requrl:%s"%(requrl))
        try:
            res_data = requests.options(requrl)
            #获取http结果
            res_data = res_data.json()
            self.logs.debug("urllib2>>>>data:%s"%json.dumps(res_data))
            self.logs.debug("%s%s%s"%('^'*25,'send success','^'*25))
            return (True,res_data)
        except Exception as e :
            self.logs.error("%s%s%s"%('!'*25,'send failure','!'*25))
            return (False,'%s'%e)
        pass
    def DELETE(self,requrl):
        self.logs.debug("%s%s%s"%('='*25,'DELETE','='*25))
        self.logs.debug("urllib2>>>>requrl:%s"%(requrl))
        try:
            res_data = requests.delete(requrl)
            #获取http结果
            res_data = res_data.json()
            self.logs.debug("urllib2>>>>data:%s"%json.dumps(res_data))
            self.logs.debug("%s%s%s"%('^'*25,'send success','^'*25))
            return (True,res_data)
        except Exception as e :
            self.logs.error("%s%s%s"%('!'*25,'send failure','!'*25))
            return (False,'%s'%e)
    def PUT(self,requrl,post_data,logs='debug'):
        getattr(self.logs,logs)("%sPUT=%s%s"%('='*25,requrl,'='*25))
        getattr(self.logs,logs)("urllib2>>>>requrl:%s data:%s headers:%s"%(requrl,post_data,self.headerdata))
        try:
            res_data = requests.put(requrl,post_data)
            getattr(self.logs,logs)("urllib2>>>>data:%s"%json.dumps(res_data.json()))
            getattr(self.logs,logs)("%s%s%s"%('^'*25,'send success','^'*25))
            return (True,res_data)
        except Exception as e:
            getattr(self.logs,'error')("%s%s%s"%('!'*25,'send failure','!'*25))
            return (False,'%s'%e)
def test():
    pass
if __name__ == '__main__':
    test()