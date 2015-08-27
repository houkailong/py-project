# encoding=UTF-8
__author__ = 'xuebaoku'
import socket
import threading
from Queue import Queue
import os
import time
import paramiko
from API import logs
from API import Http
import conf
def __check(address,port,logs):
    """
    检测端口是否存活
    :param address: ip地址
    :param port: 端口
    :param logs: 传入logs接口.
    :return: 成功返回True 不成功返回False
    """
    socket.setdefaulttimeout(conf.timeout)
    s = socket.socket()
    logs.info("%s开始检测 %s 端口 %s" %('>'*10,address, port))
    try:
        s.connect((address, port))
        logs.info("%s检测 %s 端口 %s 成功" % ('>'*10,address, port))
        return True
    except socket.error, e:
        logs.info("%s检测 %s 端口 %s 失败 %s" % ('>'*10,address, port, e.message))
        return False
def ssh_Initialize(data,Host_list,logs):
    """
    ssh初始化连接程序
    :param data: host相关队列
    :param Host_list: host成功队列
    :param logs: logs: logs接口.
    :return: 没有任何返回
    """
    try:
        while True:
            if Host_list.qsize() == 0:#队列为空的时候.跳出
                break
            msg = Host_list.get()#取出队列内容
            logs.info('开始消费%s\n初始化ssh连接'%msg)
            host,port,user,password = msg['host'],msg['port'],msg['user'],msg['password']
            try:
                assert __check(msg['host'],msg['port'],logs)#检测22端口是否存在
                #ssh超链初始化
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host,port,user,password,timeout=5)
                data.put({'ssh':ssh,'ip':msg['host'],
                          'task':msg['task'],
                          'Duct_group':msg['Duct_group'],
                          "host_id":msg['host_id']})#相关内容加入队列
            except Exception as e :
                logs.error('ssh_Initialize错误信息\n%s'%e.message)
                pass
            time.sleep(1)
        logs.info('线程.结束执行  pid %d ' % (os.getppid()))
    except Exception as e :
        print e
        logs.warning('多线程错误信息 %s'%e)
        pass
def ssh_cmd(data,cmd_list,logs):
    """

    :param data: 队列
    :param cmd_list:命令列表
    :param logs: logs接口.
    :return:无返回
    """
    try:
        http_logs = Http.HttpNetRobot('http://127.0.0.1:8000/',logs)
        while True:
            if data.qsize() == 0:#队列为空的时候.跳出
                break
            Data = data.get()#取出内容
            try:
                ssh,ip = Data['ssh'],Data['ip']#分离内容
                task,Duct_group,host_id = Data['task'],Data['Duct_group'],Data['host_id']
            except Exception as e :
                logs.error('解析数据失败哦!\n%s'%e.message)
            logs.info('开始消费命令队列')
            logs.info('%s%s%s\n'%("^"*25,ip,"^"*25))
            for i in cmd_list:#对命令进行循环
                try:
                    logs.info('%s%s%s'%("<"*5,i,">"*5))
                    '''for dd in ssh.exec_command(i):#对操作列表进行循环
                        try:
                            a = dd.read()
                            assert int(len(a)) != 0
                            logs.info('%s%s%s\n%s\n%s%s%s\n'%("^"*25,ip,"^"*25,a,"^"*25,ip,"^"*25))
                            post_data = {
                                        "task": task,
                                        "Duct_group": Duct_group,
                                        "result": 'OK',
                                        "log": data,
                                        "host_id": host_id
                                    }
                            http_logs.POST('api/TaskLog/',post_data,logs='info',mode=True)
                        except:
                            pass'''
                except Exception as e :
                    logs.error('错误信息\n%s'%e.message)
                    pass
            logs.info('\n%s%s%s\n'%("^"*25,ip,"^"*25))
            ssh.close()
            time.sleep(1)
        logs.info('线程.结束执行  pid %d ' % (os.getppid()))
    except Exception as e :
        print e
        logs.warning('多线程错误信息 %s'%e)
        pass
def Ssh_Host(host_list,logs,num=5):
    if len(host_list) <= num:
        num = 1
    #初始化队列
    Host_list = Queue()
    for i in host_list:
        Host_list.put(i)
    Host_Queue = Queue()
    Producer_teds = []
    for x in xrange(0, num):
        producer = threading.Thread(target=ssh_Initialize, args=(Host_Queue,Host_list,logs,))
        Producer_teds.append(producer)
    for t in Producer_teds:
        t.start()
    for t in Producer_teds:
        t.join()
    Host = []
    while True:
            if Host_Queue.qsize() == 0:#队列为空的时候.跳出
                break
            Host.append(Host_Queue.get())
    return Host
def Ssh_cmd(host_list,cmd_list,logs,num=5):
    if len(host_list) <= num:
        num = 1
    Host_Queue = Queue()
    for i in host_list:
        Host_Queue.put(i)
    Producer_teds = []
    for x in xrange(0, num):
        producer = threading.Thread(target=ssh_cmd, args=(Host_Queue,cmd_list,logs,))
        Producer_teds.append(producer)
    for t in Producer_teds:
        t.start()
    for t in Producer_teds:
        t.join()
def demo(host_list,cmd_list,logs,num=5):
    """
    对外接口
    :param host_list: 主机列表
    [{'host':'127.0.0.1','user':'xuebaoku','password':'123456','port':22}]
    :param cmd_list: 命令列表
    :param logs: logs接口
    :param num: 线程数量
    :return:无返回
    """
    host_list = Ssh_Host(host_list,logs,num=num)

    #初始化队列
    Ssh_cmd(host_list,cmd_list,logs,num=num)


if __name__ == '__main__':
    #标准程序接口方式
    host_list = [{'host':'127.0.0.1',
                  'user':'xuebaoku',
                  'password':'123456',
                  'port':22,
                  'task':2,
                  'Duct_group':3,
                  "host_id":4}]
    cmd_list = ['cd Downloads','ls -l','cat a.py']
    logs2 = logs.logs_install('123213.log')
    logs2.info(123)
    demo(host_list,cmd_list,logs2)