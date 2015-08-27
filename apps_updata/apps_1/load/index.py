# encoding=UTF-8
__author__ = 'xuebaoku'
import time
import os

import zmq

from apps_1.load import DAL



#加载本地配置文件
import conf
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#用守护进程的方式启动客户端
def deamonize(logs):
    """
    目前已经传入logs参数.进行.守护进行的启动
    :param logs: logs参数.需要提前进行启动
    :return:没有返回.默认已经进行后台启动
    """
    try:
        pid = os.fork()
        logs.info("进程#1 fork_pid:%s" %(pid))
        if pid > 0:
            logs.warning("进程 #1 fork_pid:%s 大于0  执行退出"%(pid))
            sys.exit(0)
    except OSError,e:
        logs.warning("进程#1 errno:%s strerror:%s  执行退出" %(e.errno,e.strerror))
        sys.exit(1)
    os.chdir("./logs")
    os.umask(0)
    os.setsid()
    try:
        pid = os.fork()
        logs.info("进程#1 fork_pid:%s" %(pid))
        if pid > 0:
            logs.warning("进程 #2 fork_pid:%s 大于0 执行退出"%(pid))
            sys.exit(0)
    except OSError,e:
        logs.warning("进程#1 errno:%s strerror:%s 执行退出" %(e.errno,e.strerror))
        sys.exit(1)
    #这里是保存日志的地方.
    '''for f in sys.stdout,sys.stderr:
        f.flush()
        si = file(stdin,'r')
        so = file(stdout,'a+')
        se = file(stderr,'a+',0)
        os.dup2(si.fileno(),sys.stdin.fileno())
        os.dup2(so.fileno(),sys.stdout.fileno())
        os.dup2(se.fileno(),sys.stderr.fileno())'''

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


def apps_local(logs):
    def recv(s):
        try:
            msg = s.recv_json()
            logs.debug('接收信息成功:%s' %(msg))
            return msg
        except Exception as e:
            logs.warning("接收信息失败error :%s"%(e.message))
            return {'Mode':None,'data':{'message':e.message}}
    logs.debug('守护进程开始 pid %d' % os.getpid())
    Counter = 0
    try:
        c = zmq.Context(1)
        s = c.socket(zmq.REP)
        s.bind('tcp://%s:%s'%(conf.IP, conf.PORT))
        logs.info('%s:%s 启动成功'%(conf.IP, conf.PORT))
    except Exception as e:
        logs.error('%s:%s 启动失败 失败原因:%s'%(conf.IP, conf.PORT,e.message))
    while True:
        logs.debug('开始接受第%s次' %(Counter))
        msg = recv(s)
        apps = DAL.apps(logs,tomcat_dict=conf.tomcat_dict)
        try:
            if msg['mode']  == None:
                s.send(msg)
            elif msg['mode'] == 'exit':
                logs.info("接收到客户端发来退出信息.开始退出声明")
                if msg['data']['data'] == '123456':
                    msg['data']['message']  = '关闭密码正确.开始关闭'
                    logs.warning(msg['data']['message'])
                    s.send_json(msg)
                    break
                else:
                    msg['data']['message']  = '关闭密码错误'
                    logs.error(msg['data']['message'])
                    s.send_json(msg)
        except Exception as e:
            logs.error("服务端未知错误 %s"%(e.message))
        try:
            getattr(apps, msg['mode'])(data=msg['data'])
            msg['data']['message'] = '%s操作成功'%(msg['data']['name'])
            s.send_json(msg)
        except Exception as e:
            msg['data']['message'] = e.message
            logs.error(msg['data']['message'])
            s.send_json(msg)
            pass

        try:
            reload(DAL)
            reload(conf)
            logs.debug('载入操作类成功')
        except Exception as e:
            logs.error('载入操作类失败 %s'%e.message)
            break
            pass


        '''if msg:
            args_array = msg.split('|')
            reposName = args_array[0]
            auth = args_array[1]
            userName = args_array[2]
            branchesName = args_array[3]
            if reposName == 'it' or reposName == 'trade' or reposName == 'tech-arch':
                pass
                #javaAuthChange(reposName,auth,userName,branchesName)
            if reposName == 'php':
                pass
                #svnAuthChange(reposName,auth,userName,branchesName)'''
        #s.send(msg)
        Counter += 1
        time.sleep(1)
    logs.debug('守护进程退出 pid %d' % os.getpid())
def demo(BASE_DIR):
    """
    系统初始化参数
    :param BASE_DIR: 本文件夹位置
    :return:默认直接启动
    """
    if not BASE_DIR:
        BASE_DIR='./'
    logs_file = BASE_DIR + "/" + conf.logs_file
    logs = logs_install(logs_file)
    #deamonize(logs)
    apps_local(logs)
    pass

def zmq_Initialization(logs):
    try:
        c = zmq.Context(1)
        s = c.socket(zmq.REP)
        s.bind('tcp://%s:%s'%(conf.IP, conf.PORT))
        logs.info('%s:%s 启动成功'%(conf.IP, conf.PORT))
        return s
    except Exception as e:
        logs.error('%s:%s 启动失败 失败原因:%s'%(conf.IP, conf.PORT,e.message))
def recv(s,logs):
    try:
        msg = s.recv_json()
        logs.debug('接收信息成功:%s' %(msg))
        return msg
    except Exception as e:
        logs.warning("接收信息失败error :%s"%(e.message))
        return {'Mode':None,'data':{'message':e.message}}
def appOverload(s,logs):
    try:
        reload(DAL)
        reload(conf)
        logs.debug('载入操作类成功')
        apps = DAL.apps(logs,tomcat_dict=conf.tomcat_dict)
        return apps
    except Exception as e:
        logs.error('载入操作类失败 %s'%e.message)
        s.send_json({'data':{'message':'载入操作类失败 %s'%e.message},'mode':False})
        return False
        pass
def mode_Verification(s,msg,logs):
    try:
        if msg['mode']  == None:
            s.send(msg)
        elif msg['mode'] == 'exit':
            logs.info("接收到客户端发来退出信息.开始退出声明")
        try:
            assert msg['data']['password']
        except:
            return
        if msg['data']['password'] == conf.password:
            msg['data']['message']  = '关闭密码正确.开始关闭'
            logs.warning(msg['data']['message'])
            s.send_json(msg)
            return True
        else:
            msg['data']['message']  = '关闭密码错误'
            logs.error(msg['data']['message'])
            s.send_json(msg)
    except Exception as e:
        logs.error("服务端未知错误 %s"%(e.message))
def Apps_T(logs):
    logs.debug('守护进程开始 pid %d' % os.getpid())
    Counter = 0
    s = zmq_Initialization(logs)
    while True:
        logs.debug('开始接受第%s次' %(Counter))
        msg = recv(s,logs)
        apps = appOverload(s,logs)
        if not apps:
            continue
        if mode_Verification(s,msg,logs):
            break
        try:
            getattr(apps, msg['mode'])(data=msg['data'])
            msg['data']['message'] = '%s 操作成功'%(msg['data']['name'])
            msg['mode'] = True
            s.send_json(msg)
        except Exception as e:
            msg['data']['message'] = e.message
            msg['mode'] = False
            logs.error(msg['data']['message'])
            s.send_json(msg)
            pass
        Counter += 1
        time.sleep(1)
    logs.debug('守护进程退出 pid %d' % os.getpid())
def demo2(BASE_DIR):
    """
    系统初始化参数
    :param BASE_DIR: 本文件夹位置
    :return:默认直接启动
    """
    logs_file = BASE_DIR + conf.logs_file
    print logs_file
    logs = logs_install(logs_file)
    #deamonize(logs)
    Apps_T(logs)
    pass
if __name__=="__main__":
    BASE_DIR = os.path.dirname(__file__)
    if not BASE_DIR:
        BASE_DIR = './'
    if BASE_DIR != './':
        BASE_DIR = BASE_DIR + '/'
    demo2(BASE_DIR)
    #deamonize('/dev/null','%s/logs/svnDeamon.log'%BASE_DIR,'%s/logs/svnDeamon.log'%BASE_DIR)
    #svnMain()