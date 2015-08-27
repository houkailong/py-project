# encoding=UTF-8
__author__ = 'xuebaoku'
import time
import subprocess
import shlex
import select
import fcntl
import os
import errno
import contextlib

import conf


class ssh_clen():
    def __init__(self,logs):
        self.logs =logs
        pass
class apps():
    tomcat = False
    def __init__(self,logs,tomcat_dict):
        self.logs =logs
        self.tomcat_dict = tomcat_dict
        pass
    def up_rsync(self,data):
        self.__check_name(data['name'])
        self.logs.info("对项目%s 进行拉取代码"%data['name'])
        try:
            Pull_server = """ -e \'ssh -p %s\' %s@%s:%s"""%(data['Pull_port'],data['Pull_user'],data['Pull_server'],data['Pull_path'])
        except:
            pass
        cmdStr = '%s %s %s >%s'%(conf.rasync,Pull_server, conf.gitpath_dep, conf.tempfile)
        self.logs.info("执行命令:%s"%cmdStr)
        cmdStr = """grep "deleting" %s |awk -F"deleting " '{print $2}'"""%(conf.tempfile)
        self.logs.info("执行命令:%s"%cmdStr)
        dd=[0,'1 2 3 4']
        #data = commands.getoutput(cmdStr)
        #self.logs.indo('执行结果 :%s'%data)
        cmdStr = """for i in %s ;do cd %s/%s && git rm %s/%s/$i;done"""%(dd[1],self.tomcat['path'],data['name'],self.tomcat['path'],data['name'])
        self.logs.info("执行命令:%s"%cmdStr)
        cmdStr = """cd %s/%s && git add . && git commit -m "%s" && git push origin master"""%(self.tomcat['path'],data['name'],'123')
        self.logs.info("执行命令:%s"%cmdStr)
        #self.main(cmdStr)
        self.logs.info("对项目%s 进行拉取代码 成功"%data['name'])
        pass
    def updata(self,data):
        self.__check_name(data['name'])
        self.logs.info("对项目%s 进行更新"%data['name'])
        self.up_rsync(data)
        time.sleep(1)
        self.restart(data)
        self.logs.info("对项目%s 进行更新"%data['name'])
        pass
    def restart(self,data):
        self.__check_name(data['name'])
        self.logs.info("对项目%s 进行重启"%data['name'])
        self.stop(data)
        time.sleep(1)
        self.start(data)
        self.logs.info("对项目%s 重启完毕"%data['name'])
        pass
    def start(self,data):
        self.__check_name(data['name'])
        self.logs.info("对项目%s 进行启动 开始"%data['name'])
        cmdStr = '. ~/.bashrc && sudo su - appuser -c \"/bin/base %s/%s/%s start\" '%(self.tomcat['path'],data['name'],self.tomcat['shell'])
        self.logs.info("执行命令:%s"%cmdStr)
        #self.main(cmdStr)
        self.logs.info("对项目%s 进行启动 成功"%data['name'])
        return True
        pass
    def stop(self,data):
        self.__check_name(data['name'])
        self.logs.info("对项目%s 进行关闭 开始"%data['name'])
        cmdStr = """. ~/.bashrc && sudo su - appuser -c \"/bin/base %s/%s/%s stop\" """%(self.tomcat['path'],data['name'],self.tomcat['shell'])
        self.logs.info("执行命令:%s"%cmdStr)
        #self.main(cmdStr)
        self.logs.info("对项目%s 进行关闭 成功"%data['name'])
        return True
        pass
    def __check_name(self,data):
        if self.tomcat:
            return
        try:
            assert self.tomcat_dict[data]
            self.tomcat = self.tomcat_dict[data]
        except Exception as e:
            self.logs.error('获取tomcat相关信息失败 %s error:%s'%(data,e.message))
            pass
    def log_fds(self,fds):
        """log写入.并输出相关数据"""
        for fd in fds:
            out = self.__read_async(fd)
            if out:
                #对数据进行打印
                self.logs('>>>>>>>%s'%out)
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
    def main(self,cmdStr):
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