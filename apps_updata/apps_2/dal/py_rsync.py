# encoding=UTF-8
__author__ = 'xuebaoku'
import dirsync
from API.cmd import rsync
from API import logs
def demo(source,target,arguments='-avz --progress --partial --delete'):
    logs2 = logs.logs_install('123213.log')
    data =  rsync(source,target,logs2,exclude_from='',logs_return=True)
    while 1 :
        try:
            print data.next(),
        except Exception as e :
            print e.message
            break

    #a.cmd('ls')
if __name__ == '__main__':
    demo(source='./',target='../123')
