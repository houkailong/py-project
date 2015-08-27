# encoding=UTF-8
__author__ = 'xuebaoku'
from API.Http import HttpNetRobot
from API.ssh_Client import Ssh_Host,Ssh_cmd
import conf
import time


class APPS_DAL():
    def __init__(self,data,logs):
        self.logs = logs
        self.Http = HttpNetRobot('http://%s:%s/'%(conf.Url_ip, conf.Url_post),self.logs)
        #self.data = self.__get_info(data)
        self.data = {"status": "success",
                     "Duct": {"info": {"path": "/apps", "shell": "restart.sh", "port": "8080", "jmxport": "8580", "name": "tomcat-test_0001"},
                              "One_group": [{"ip": "10.19.2.101", "id": 52}],
                              "Two_Group": [{"ip": "10.19.2.112", "id": 1},
                                            {"ip": "10.19.2.113", "id": 2},
                                            {"ip": "10.19.2.111", "id": 3},
                                            {"ip": "10.19.2.83", "id": 4}],
                              "thr_Group": [{'ip':'127.0.0.1','id':0}]},
                     "package": {"Pull_port": "22", "code": "success", "Pull_path": "/home/git/haodaibao.com/bank_union_oms/",
                                 "Pull_user": "syspub", "caption": "syspub1440136201.65.war",
                                 "Pull_server": "192.168.1.1", "id": 205},
                     "id": 204,
                     "uuid": "830dad46eb6048d08a9b09c368f154db"}
        self.group = 'thr_Group'

        self.Hosts = Ssh_Host(host_list=[{'host':'127.0.0.1',
                  'user':'xuebaoku',
                  'password':'123456',
                  'port':22,
                  'task':2,
                  'Duct_group':3,
                  "host_id":4}],logs=self.logs)
    def online_updata(self):
        """
        更新线上项目
        :param msg:
        :return:
        """
        self.logs.info('更新项目')
        #if self.__check_version():
        #    return "已经是最新版本跳过更新"
        self.__updata()
        self.__restart()
    def restart(self):
        """
        重启
        :return:
        """
        self.__restart()
    def online(self):
        """
        上线新项目
        :param msg:
        :return:
        """
        self.logs.info('上线新项目')
        if self.__check_():#检测项目是否存在.
            self.__del_()
        self.__deploy_()#部署新项目
        self.__restart()#启动项目

    def __updata(self):
        """
        更新项目
        :return:
        """
        Duct = self.data['Duct']['info']
        data = [
            'cd %s/%s/webapps/%s'%(Duct['path'],Duct['name'],Duct['name']),
            '/usr/bin/git pull origin master',
        ]
        self.logs.info('开始部署当前项目')
        Ssh_cmd(self.Hosts,data,self.logs)
        pass
    def __check_(self):
        """
        检测当前项目是否存在
        :return: 存在返回Ture 不存在放回False
        """

        return True
    def __check_version(self):
        """
        检测当前项目是否存在
        :return: 存在返回Ture 不存在放回False
        """

        return True
    def __deploy_(self):
        """
        部署当前项目
        :return:
        """
        Duct = self.data['Duct']['info']
        data = [
            'sudo su - ',
            'cd %s'%(Duct['path']),
            'git clone git@git.haodaibao.com:tomcat-default.git ./%s'%(Duct['name']),
            'mkdir -p ./webapps/',
            'cd webapps',
            """echo "git clone git@git.haodaibao.com:%s.git %s">./git.sh"""%(Duct['name'],Duct['name']),
            'sh ./git.sh',
            'cd %s'%(Duct['path']),
            'chown appuser.appuser ./%s'%(Duct['name']),
            'chown deploy.deploy ./%s/webapps/'%(Duct['name']),
            'sudo su - appuser',
            'cd %s/%s'%(Duct['path'],Duct['name']),
            'python ./tomcat_install.py -s %s -p %s -d webapps -jp %s  -hostname %s'%(int(Duct['port'])-10,Duct['port'],Duct['jmxport'],Duct['jmxport']),
            """python discovery.py -A %s --pn %s --pw %s --lf 'catcatn' --lg '500.jsp' --lt 1000 --uf '/' --ug '123'"""%(Duct['name'],Duct['jmxport'],Duct['port']),
        ]
        self.logs.info('开始部署当前项目')
        Ssh_cmd(self.Hosts,data,self.logs)
        pass
    def __del_(self):
        """
        删除当前项目所有内容
        :return:
        """
        Duct = self.data['Duct']['info']
        data = [
            'sudo su - ',
            'cd %s'%(Duct['path']),
            '''mv ./%s ./%s.%s'''%(Duct['name'],Duct['name'],time.time()),
        ]
        self.logs.info('开始删除当前项目')
        Ssh_cmd(self.Hosts,data,self.logs)
    def __restart(self):
        """
        重启程序
        :param data:
        :return:
        """
        data = ''
        self.__stop()
        #time.sleep(5)
        self.__start()
    def __stop(self):
        """
        停止程序
        :param data:
        :return:
        """
        Duct = self.data['Duct']['info']
        data = [
            'su - appuser',
            'cd %s/%s'%(Duct['path'],Duct['name']),
            './%s stop'%(Duct['shell'])
        ]
        Ssh_cmd(self.Hosts,data,self.logs)
    def __start(self):
        """
        启动程序
        :param data:
        :return:
        """

        Duct = self.data['Duct']['info']
        data = [
            'su - appuser',
            'cd %s/%s'%(Duct['path'],Duct['name']),
            './%s start'%(Duct['shell'])
        ]
        Ssh_cmd(self.Hosts,data,self.logs)

    def __get_info(self,msg):
        #查询相关信息830dad46eb6048d08a9b09c368f154db
        try:
            return self.Http.GET('api/inquire/test_apps/uuid/%s/'%(msg['Project']['uuid']),logs='info')
        except Exception as e:
            self.logs.error('获取基础信息失败 \n%s'%e.message)
        return False
def test():
    import API.logs
    logs2 = API.logs.logs_install('123213.log')
    a = APPS_DAL('1',logs2)
    a.online()
    pass


if __name__ == '__main__':
    test()