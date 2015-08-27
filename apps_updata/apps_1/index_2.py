# encoding=UTF-8
__author__ = 'xuebaoku'
from Queue import Queue
import threading
import os
import time
import sys

import zmq

from API_2 import logs_install
import conf
from apps_1.dal import test_zmq_DAL, test_apps_DAL


reload(sys)
sys.setdefaultencoding('utf-8')

class Zmq_Thread(threading.Thread):
    #生产者
    Counter = 0
    def __init__(self,logs, t_name, queue):
        self.logs = logs
        threading.Thread.__init__(self, name=t_name)
        self.t_name = t_name
        self.data=queue
    def run(self):
        self.logs.debug('线程.开始执行 name %s  pid %d ' % (self.t_name,os.getppid()))
        if self.__zmq_Initialization():
            return
        try:
            while True:
                self.logs.info('开始等待接收信息 - 第%s次' %(self.Counter))
                msg = self.__recv()
                #if self.__mode_Verification(msg):
                #    break
                ass,apps = self.__Overload()
                if ass:
                    if hasattr(apps, '%s'%msg['mode']):
                        data = getattr(apps, '%s'%msg['mode'])(msg)
                    else:
                        data={'mode':False,'data':{'message':'没有这个参数'}}
                else:
                    data={'mode':False,'data':{'message':'系统发生异常错误.请提交管理员后进行确认'}}
                self.s.send_json(data)
                self.Counter += 1
                time.sleep(1)
            self.logs.debug('线程.结束执行 name %s  pid %d ' % (self.t_name,os.getppid()))
        except Exception as e :
            print e
            self.logs.warning('多线程错误信息 %s'%e)
            pass
    def __zmq_Initialization(self):
        try:
            c = zmq.Context(1)
            self.s = c.socket(zmq.REP)
            self.s.bind('tcp://%s:%s'%(conf.IP, conf.PORT))
            self.logs.info('%s:%s 启动成功'%(conf.IP, conf.PORT))
            return False
        except Exception as e:
            self.logs.error('%s:%s 启动失败 失败原因:%s'%(conf.IP, conf.PORT,e.message))
            return True
    def __recv(self):
        try:
            msg = self.s.recv_json()
            self.logs.debug('线程:%s 接收信息成功:%s' %(self.t_name,msg))
            return msg
        except Exception as e:
            self.logs.warning("线程:%s 接收信息失败error :%s"%(self.t_name,e.message))
            return {'Mode':None,'data':{'message':e.message}}
    def __mode_Verification(self,msg):
        """
        管理模块.
        验证接收到得数据.是否是空.
        另验证.程序.是否要被退出
        :param msg:
        :return:
        """
        try:
            if msg['mode']  == None:
                self.s.send(msg)
                return False
            elif msg['mode'] == 'exit':
                self.logs.info("接收到客户端发来退出信息.开始退出声明")
            try:
                assert msg['data']['password']
            except:
                return False
            if msg['data']['password'] == conf.password:
                msg['data']['message']  = '关闭密码正确.开始关闭'
                self.logs.warning(msg['data']['message'])
                self.s.send_json(msg)
                return True
            else:
                msg['data']['message']  = '关闭密码错误'
                self.logs.error(msg['data']['message'])
                self.s.send_json(msg)
        except Exception as e:
            self.logs.error("服务端未知错误 %s"%(e.message))
    def __Overload(self):
        """
        重载模块.每次接收到信息后 重新载入相关类
        :return:
        """
        try:
            reload(test_zmq_DAL)
            self.logs.debug('载入操作类成功')
            apps = test_zmq_DAL.ZMQ_DAL(self.data,self.logs)
            return (True,apps)
        except Exception as e:
            self.logs.error('载入操作类失败 %s'%e.message)
            return (False,None)

class apps_Thread(threading.Thread):
    #消费者
    Counter = 0
    def __init__(self,logs, t_name, queue):
        self.logs = logs
        threading.Thread.__init__(self, name=t_name)
        self.t_name = t_name
        self.data=queue
    def run(self):
        self.logs.debug('线程.开始执行 name %s  pid %d ' % (self.t_name,os.getppid()))
        try:
            while True:
                msg = self.data.get()
                self.logs.info('开始消费%s'%msg)
                ass,apps = self.__Overload(msg)
                if ass:
                    if hasattr(apps, '%s'%msg['mode']):
                        data = getattr(apps, '%s'%msg['mode'])()
                    else:
                        data={'mode':False,'data':{'message':'没有这个参数'}}
                else:
                    data={'mode':False,'data':{'message':'系统发生异常错误.请提交管理员后进行确认'}}
                self.logs.info(data)
                self.Counter += 1
                time.sleep(1)
            self.logs.debug('线程.结束执行 name %s  pid %d ' % (self.t_name,os.getppid()))
        except Exception as e :
            self.logs.warning('多线程错误信息 %s'%e)
            pass
    def __Overload(self,msg):
        """
        重载模块.每次接收到信息后 重新载入相关类
        :return:
        """
        try:
            reload(test_apps_DAL)
            self.logs.debug('载入操作类成功')
            apps = test_apps_DAL.APPS_DAL(msg,self.logs)
            return (True,apps)
        except Exception as e:
            self.logs.error('载入操作类失败 %s'%e.message)
            return (False,None)


def demo():
    BASE_DIR = os.path.abspath('.')
    zmq_Queue = Queue()
    if not BASE_DIR:
            BASE_DIR = './'
    if BASE_DIR != './':
            BASE_DIR = BASE_DIR + '/'
    logs= logs_install(BASE_DIR+ conf.logs_file)
    producer_1 = apps_Thread(logs,'Apps_Thread_1',zmq_Queue)
    producer_1.start()
    producer_2 = apps_Thread(logs,'Apps_Thread_2',zmq_Queue)
    producer_2.start()
    producer_3 = apps_Thread(logs,'Apps_Thread_3',zmq_Queue)
    producer_3.start()
    producer = Zmq_Thread(logs,'Zmq_Thread',zmq_Queue)
    producer.start()


if __name__ == '__main__':
    demo()