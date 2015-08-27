# encoding=UTF-8
__author__ = 'xuebaoku'
import subprocess
import shlex
import select
import fcntl
import os
import errno
import contextlib
import time
class subprocess_logs():
    def __init__(self,logs):
        self.logs = logs#默认logs文件.
    def __deleting(self,logs):
        """
        按照行来进行分割.
        :param logs:
        :return:
        """
        self.tmp_file.write(logs)
    def __tmp_logs_read(self):
        tmp_file = open(self.tmp_file_name,'r+b')
        for i in tmp_file.readlines():
            yield i
        tmp_file.close()
        os.remove(self.tmp_file_name)
    def __log_fds(self,fds,logs_return):
        """
        从缓存中.读取相关数据.无返回值
        :param fds:
        """
        for fd in fds:
            out = self.__read_async(fd)
            if out:
                #对数据进行打印
                getattr(self.logs,'info')('%s'%(out))
                if logs_return:
                    self.__deleting(out)
    def cmd(self,cmdStr,logs_return=False):
        """
        cmd模块
        :param cmdStr:
        :return:
        """
        if logs_return:
            self.tmp_file_name = './tmp_%s.log'%time.time()
            self.tmp_file = open(self.tmp_file_name,'w+b')
        getattr(self.logs,'info')('^'*25)
        with self.__plain_logger():
            proc = subprocess.Popen(shlex.split(cmdStr),
                                    stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            # without `make_async`, `fd.read` in `read_async` blocks.
            self.__make_async(proc.stdout)
            self.__make_async(proc.stderr)
            while True:
                # 等待数据变得可用
                rlist, wlist, xlist = select.select([proc.stdout, proc.stderr], [], [])
                self.__log_fds(rlist,logs_return)
                if proc.poll() is not None:
                    # 检查是否已创建多个输出
                    # 如果输出则进行记录
                    self.__log_fds([proc.stdout, proc.stderr],logs_return)
                    break
        getattr(self.logs,'info')('^'*25)
        if logs_return:
            self.tmp_file.close()
            return self.__tmp_logs_read()
    def __make_async(self,fd):
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
    @contextlib.contextmanager
    def __plain_logger(self):
        yield

def rsync(source,target,logs,cmd='',arguments='-avz --progress --partial --delete',exclude_from='/home/syspub/bin/app/git',logs_return=False):
    '''
    调用系统的rsync命令进行python操作

    :param source: 目录
    :param target: 目录
    :param logs: logs函数.必须传入一个logs方法
    :param arguments: 默认参数命令
    :param exclude_from: 默认去除文件操作.必须是全路径
    :param logs_return: yield返回当前操作数据
    :return:
    '''
    if not cmd:
        rsync = "rsync"
        cmd = "%s %s %s %s %s"%(rsync,arguments,exclude_from,source,target)
    a = subprocess_logs(logs=logs)
    return a.cmd(cmd,logs_return=logs_return)
def demo():
    from API import logs
    logs2 = logs.logs_install('123213.log')
    logs2.info(1123)
    #a = bendi_cmd('203',logs=logs2)
    #a.cmd('ls')
    #a.cmd('ls')
    pass


if __name__ == '__main__':
    demo()