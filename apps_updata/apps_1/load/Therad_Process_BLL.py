# encoding=UTF-8
__author__ = 'xuebaoku'
# producer_consumer_queue
from Queue import Queue
import threading
import time
import socket
import json
import paramiko

class check_server(threading.Thread):
    #消费者
    def __init__(self,logs, t_name, queue):
        self.logs = logs
        threading.Thread.__init__(self, name=t_name)
        self.t_name = t_name
        self.data=queue
    def run(self):
        try:
            while True:
                qsize = self.data.qsize()
                if qsize <= 0:
                    break
                else:
                    val = self.data.get()
                    self.logs.debug('开始消费%s'%json.dumps(val))
                    commd = val['commd']
                    host = val['host']
                    name = val['name']
                    BASE_DIR = val['BASE_DIR']
                    try:
                        username = val['username']
                    except:
                        username = None
                    try:
                        groups = val['groups']
                    except:
                        groups = None
                    try:
                        prot = val['port']
                    except:
                        prot = 22
                    self.logs.debug('开始消费%s'%json.dumps(val))
                    if self.__check(host,prot):
                        self.ssh_cmd(groups,name,host,prot,BASE_DIR,username,cmd_list=commd)
                time.sleep(1)
            print "线程%s 结束======="%self.t_name
        except Exception as e :
            self.logs.warning('多线程错误信息 %s'%e)
            pass
    def ssh_cmd(self,groups,name,host,prot,BASE_DIR,username,cmd_list):
        address, port=host,prot
        self.logs.debug('初始化命令执行')
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if username == 'syspub':
            privatekeyfile = "%sssh_key/syspub_id_rsa"%(BASE_DIR)
        elif username == 'appuser':
            privatekeyfile = "%sssh_key/appuser_id_rsa"%(BASE_DIR)
        #privatekeyfile = './ssh_key/syspub_id_rsa'
        mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
        try:
            s.connect(address,port,username,pkey=mykey,timeout=5)
        except:
            self.logs.info('%s连接初始化失败'%address)
        if type(cmd_list) == list:
            try:
                for cmd in cmd_list:
                    #此处需要修改源代码来实现超时机制
                    stdin,stdout,stderr = s.exec_command(cmd,timeout=10)
                    read = [stdin.read(),stdout.read(),stderr.read()]
                    print "\n".join(stdin.read())
                    print "\n".join(stdout.read())
                    print "\n".join(stderr.read())
                    self.logs.debug("\n".join(read))
                s.close()
                return True
            except:
                self.logs.info('执行命令失败')
                return False
                pass
        else:
            pass
    def __check(self,host,prot):
        timeout = 2
        socket.setdefaulttimeout(timeout)
        address, port=host,prot
        s = socket.socket()
        self.logs.debug("开始检测 %s 端口 %s" %(address, port))
        try:
            s.connect((address, port))
            self.logs.debug("检测 %s 端口 %s 成功" % (address, port))
            return True
        except socket.error, e:
            self.logs.info("检测 %s 端口 %s 失败 %s" % (address, port, e))
            return False

def Daemon_t(logs,Queue,num=1):
    logs.debug('>>>>>开始线程执行')
    logs.debug('>>>>>>>>定义线程池 - 开始')#
    Producer_teds = []
    logs.debug('>>>>>>>>定义线程池 - 结束')#
    logs.debug('>>>>>>>>创建线程对象 - 开始')#
    for x in xrange(0, num):
        producer = check_server(logs,'test%s'%x,Queue)
        Producer_teds.append(producer)
    logs.debug('>>>>>>>>创建线程对象 - 结束')#
    logs.debug('>>>>>>>>启动所有线程 - 开始')#
    for t in Producer_teds:
        t.start()
    logs.debug('>>>>>>>>启动所有线程 - 结束')#
    logs.debug('>>>>>>>>主线程中等待所有子线程退出 - 开始')#
    for t in Producer_teds:
        t.join()
    logs.debug('>>>>>>>>主线程中等待所有子线程退出 - 结束')#
    logs.debug('>>>>>线程执行结束')


def Producer_host(logs,Host_dict,commd,num=1):
    logs.debug('>>>批量开始执行命令%s'%(commd))
    logs.debug('>>>>>开始初始化队列')
    Host_dict_Queue = Queue()
    for k,v in Host_dict.items():
        try:
            Host_dict_Queue.put({'host':k,'commd':commd,'name':v['name'],
                             'BASE_DIR':v['BASE_DIR'],"username":v['username'],
                             'groups':v['groups']
            })
        except :
            Host_dict_Queue.put({'host':k,'commd':commd,'name':v['name'],
                             'BASE_DIR':v['BASE_DIR'],"username":v['username']
            })
    logs.debug('>>>>>初始化队列完成')
    logs.debug('>>>>>开始线程执行')
    logs.debug('>>>>>>>>定义线程池 - 开始')#
    Producer_teds = []
    logs.debug('>>>>>>>>定义线程池 - 结束')#
    logs.debug('>>>>>>>>创建线程对象 - 开始')#
    for x in xrange(0, num):
        producer = check_server(logs,'test%s'%x,Host_dict_Queue)
        Producer_teds.append(producer)
    logs.debug('>>>>>>>>创建线程对象 - 结束')#
    logs.debug('>>>>>>>>启动所有线程 - 开始')#
    for t in Producer_teds:
        t.start()
    logs.debug('>>>>>>>>启动所有线程 - 结束')#
    logs.debug('>>>>>>>>主线程中等待所有子线程退出 - 开始')#
    for t in Producer_teds:
        t.join()
    logs.debug('>>>>>>>>主线程中等待所有子线程退出 - 结束')#
    logs.debug('>>>>>线程执行结束')
    logs.debug('>>>批量结束执行命令%s'%(commd))
def __logs():
        import logging
        from logging.handlers import RotatingFileHandler
        file_logs = 'logs.test'
        #################################################################################################
        #定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
        logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s  %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=file_logs,
                filemode='a')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        logs=logging
        return logs
        ################################################################################################
#Main thread
def main():
    logs = __logs()
    Host_dict = {'10.19.3.20':{'name':'wjsa-db20'}}
    Producer_host(logs,Host_dict,'ls')
    print 'All threads terminate!'
if __name__ == '__main__':
    main()
