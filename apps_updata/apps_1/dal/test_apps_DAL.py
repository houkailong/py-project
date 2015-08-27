# encoding=UTF-8
__author__ = 'xuebaoku'
import subprocess
import shlex
import select
import fcntl
import os
import errno
import contextlib
import socket

import paramiko

import conf


class APPS_DAL():
    def __init__(self,data,logs):
        from apps_1.API_2 import HttpNetRobot
        self.logs = logs
        self.Http = HttpNetRobot('http://%s:%s/'%(conf.Url_ip, conf.Url_post),self.logs)
        self.data = self.__get_info(data)
        pass
    def onlinegray(self):
        """
        上线灰度
        :param msg:
        :return:
        """
        if self.__up_rsync():
            self.__restart()
            Task = self.__http_get('api/Task/%s'%(self.data['id']))
            Task['status'] = 'success'
            self.__http_Put(Task,logs='info')
            data={'mode':True,'data':{'message':'更新信息成功,并发布强制重启命令'}}
            return data
        else:
            data={'mode':False,'data':{'message':'更新失败'}}
            return data

    def __up_rsync(self):
        """
        rsync 更新 git库
        :param data:
        :return:
        """
        #self.__check_name(data['name'])
        self.logs.info("对 项目包 %s 进行拉取代码"%self.data['package']['caption'])
        try:
            Pull_server = """ -e \'ssh -p %s\' %s@%s:%s"""%(self.data['package']['Pull_port'],self.data['package']['Pull_user'],self.data['package']['Pull_server'],self.data['package']['Pull_path'])
        except:
            return False
        cmdStr = '%s %s %s >%s'%(conf.rasync,Pull_server, conf.gitpath_dep, conf.tempfile)
        #self.__cmd(cmdStr)
        self.__cmd('ls -l')
        #更改包状态
        data = True
        if data :
            Package = self.__http_get('api/Package/%s'%(self.data['package']['id']))
            Package['code'] = 'success'
            self.__http_Put(Package,logs='info')
            self.logs.info("对 项目包 %s 进行拉取代码 成功 "%self.data['package']['caption'])
            return True
        else:
            self.logs.info("对 项目包 %s 进行拉取代码 失败 "%self.data['package']['caption'])
            return False
        pass
    def __restart(self):
        """
        重启程序
        :param data:
        :return:
        """
        self.__stop()
        #time.sleep(5)
        self.__start()
        return False
    def __stop(self):
        """
        停止程序
        :param data:
        :return:
        """
        self.logs.info("对项目%s 进行关闭 开始"%self.data['Duct']['info']['name'])
        cmdStr = """. ~/.bashrc && sudo su - appuser -c \"/bin/base %s/%s/%s stop\" """%(self.data['Duct']['info']['path'],self.data['Duct']['info']['name'],self.data['Duct']['info']['shell'])
        self.logs.info("对项目%s 进行关闭 成功"%self.data['Duct']['info']['name'])
        return True
    def __start(self):
        """
        启动程序
        :param data:
        :return:
        """
        self.logs.info("对项目%s 进行启动 开始"%self.data['Duct']['info']['name'])
        cmdStr = '. ~/.bashrc && sudo su - appuser -c \"/bin/base %s/%s/%s start\" '%(self.data['Duct']['info']['path'],self.data['Duct']['info']['name'],self.data['Duct']['info']['shell'])
        self.logs.info("对项目%s 进行启动 成功"%self.data['Duct']['info']['name'])
        return True

    def __http_log(self,cmdStr,host_id=0,result='unknown',Duct_Group='Duct_One_Group'):
        try:
            post_data = {
                        "task": self.data['id'],
                        "Duct_group": Duct_Group,
                        "result": result,
                        "log": cmdStr,
                        "host_id": host_id
                    }
            self.logs.info("命令结果:%s"%post_data)
            self.Http.send('api/TaskLog/',post_data=post_data)
        except Exception as e :
            print e
            pass
    def __http_get(self,url,logs='debug'):
        try:
            Project = self.Http.get(url)
            getattr(self.logs,logs)("%s%s%s"%('='*25,url,'='*25))
            for i,v in Project.items():
                getattr(self.logs,logs)("%s:%s"%(i,v))
            getattr(self.logs,logs)("%s%s%s"%('*'*25,url,'*'*25))
            return Project
        except Exception as e:
            self.logs.error('获取 Project 信息失败 %s'%e.message)
            return False
    def __get_info(self,msg):
        #查询相关信息
        try:
            return self.__http_get('api/inquire/test_apps/uuid/%s/'%(msg['Project']['uuid']),logs='info')
        except Exception as e:
            self.logs.error('获取基础信息失败 \n%s'%e.message)
        return False
    def __http_Put(self,data,logs='debug'):
        #修改线上信息
        try:
            http,data  = self.Http.PUT(data['url'],data,logs)
            assert http
            return (True,data)
        except Exception as e :
            return (False,'修改信息失败 \n%s'%e.message)

    def __ssh_Client(self):
        address, port=host,prot
        self.logs.debug('初始化ssh客户端')
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
        try:
            #此处需要修改源代码来实现超时机制
            stdin,stdout,stderr = s.exec_command(cmd,timeout=10)
            read = ["======groups:%s==host:%s=====name:%s==========="%(groups,host,name),stdout.read(),"======groups:%s==host:%s=====name:%s==========="%(groups,host,name)]
            print "\n".join(read)
            self.logs.debug("\n".join(read))
            s.close()
            return True
        except:
            self.logs.info('执行命令失败')
            return False
            pass
    def __ssh_cmd(self):

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

    def log_fds(self,fds):
        """log写入.并输出相关数据"""
        for fd in fds:
            out = self.__read_async(fd)
            if out:
                #对数据进行打印
                self.__http_log('>>>>>>>%s'%out,result='success')
    def make_async(self,fd):
        '''添加 O_NONBLOCK 到文件描述符中'''
        fcntl.fcntl(fd, fcntl.F_SETFL, fcntl.fcntl(fd, fcntl.F_GETFL) | os.O_NONBLOCK)
    def __read_async(self,fd):
        '''读取文件描述符中的数据'''
        try:
            return fd.read()
        except IOError, e:
            if e.errno != errno.EAGAIN:
                raise e
            else:
                return ''
    def __cmd(self,cmdStr):
        with plain_logger():
            proc = subprocess.Popen(shlex.split(cmdStr),
                                    stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            # without `make_async`, `fd.read` in `read_async` blocks.
            self.make_async(proc.stdout)
            self.make_async(proc.stderr)
            while True:
                # 等待数据变得可用
                rlist, wlist, xlist = select.select([proc.stdout, proc.stderr], [], [])
                self.log_fds(rlist)
                if proc.poll() is not None:
                    # 检查是否已创建多个输出
                    # 如果输出则进行记录
                    self.log_fds([proc.stdout, proc.stderr])
                    break
@contextlib.contextmanager
def plain_logger():
    yield

def test():
    pass


if __name__ == '__main__':
    test()